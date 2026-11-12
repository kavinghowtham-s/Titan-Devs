import json
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.app.core.exceptions import ResourceNotFoundException
from backend.app.models.message import DraftReply, InboundMessage
from backend.app.models.audit import AuditLog
from backend.app.adapters.simulated_email import SimulatedEmailAdapter
from backend.app.llm.client import llm_client

class DraftService:
    @classmethod
    def get_pending_drafts(cls, db: Session, limit: int = 50) -> List[DraftReply]:
        drafts = db.query(DraftReply).filter(DraftReply.status == "pending").order_by(DraftReply.auto_approve_deadline.asc()).limit(limit).all()
        now = datetime.now(timezone.utc)
        for d in drafts:
            # Calculate remaining seconds for UI countdown
            if d.auto_approve_deadline:
                # SQLite datetimes may be naive
                deadline = d.auto_approve_deadline.replace(tzinfo=timezone.utc) if d.auto_approve_deadline.tzinfo is None else d.auto_approve_deadline
                diff = int((deadline - now).total_seconds())
                d.seconds_remaining = max(0, diff)
            else:
                d.seconds_remaining = 0
        return drafts

    @classmethod
    async def approve_draft(cls, db: Session, draft_id: int, actor_id: str = "MANAGER_RAJESH") -> DraftReply:
        draft = db.query(DraftReply).filter(DraftReply.id == draft_id).first()
        if not draft:
            raise ResourceNotFoundException("DraftReply", draft_id)

        inbound = db.query(InboundMessage).filter(InboundMessage.id == draft.inbound_message_id).first()

        now = datetime.now(timezone.utc)
        draft.status = "sent"
        draft.reviewed_at = now
        draft.reviewed_by = actor_id
        draft.sent_at = now

        # Send outbound via simulated email adapter
        email_adapter = SimulatedEmailAdapter(db)
        outbound_content = draft.edited_text if draft.edited_text else draft.draft_text
        subject = f"Re: {inbound.subject}" if inbound and inbound.subject else "Response from Trentar Pvt Ltd"
        recipient = inbound.sender_address if inbound else "customer@client.in"

        await email_adapter.send_outbound(
            recipient_address=recipient,
            subject=subject,
            body_text=outbound_content,
            reply_to_id=draft.id
        )

        db.add(AuditLog(
            entity_type="DRAFT",
            entity_id=draft.id,
            action="MANUAL_APPROVED",
            actor_type="MANAGER",
            actor_id=actor_id,
            details_json=f'{{"recipient": "{recipient}", "action": "sent"}}',
            timestamp=now
        ))

        db.commit()
        db.refresh(draft)
        return draft

    @classmethod
    def edit_draft(cls, db: Session, draft_id: int, edited_text: str, actor_id: str = "MANAGER_RAJESH") -> DraftReply:
        draft = db.query(DraftReply).filter(DraftReply.id == draft_id).first()
        if not draft:
            raise ResourceNotFoundException("DraftReply", draft_id)

        draft.edited_text = edited_text
        now = datetime.now(timezone.utc)

        db.add(AuditLog(
            entity_type="DRAFT",
            entity_id=draft.id,
            action="EDITED",
            actor_type="MANAGER",
            actor_id=actor_id,
            details_json=f'{{"edited_length": {len(edited_text)}}}',
            timestamp=now
        ))

        db.commit()
        db.refresh(draft)
        return draft

    @classmethod
    def reject_draft(cls, db: Session, draft_id: int, rejection_reason: Optional[str] = None, actor_id: str = "MANAGER_RAJESH") -> DraftReply:
        draft = db.query(DraftReply).filter(DraftReply.id == draft_id).first()
        if not draft:
            raise ResourceNotFoundException("DraftReply", draft_id)

        now = datetime.now(timezone.utc)
        draft.status = "rejected"
        draft.reviewed_at = now
        draft.reviewed_by = actor_id
        draft.safety_evaluation_notes = f"Rejected by manager: {rejection_reason or 'No reason provided'}"

        db.add(AuditLog(
            entity_type="DRAFT",
            entity_id=draft.id,
            action="REJECTED",
            actor_type="MANAGER",
            actor_id=actor_id,
            details_json=f'{{"reason": "{rejection_reason or "manual rejection"}"}}',
            timestamp=now
        ))

        db.commit()
        db.refresh(draft)
        return draft

    @classmethod
    async def process_expired_drafts(cls, db: Session) -> List[DraftReply]:
        now = datetime.now(timezone.utc)
        pending = db.query(DraftReply).filter(DraftReply.status == "pending").all()
        processed = []
        for d in pending:
            if not d.auto_approve_deadline:
                continue
            deadline = d.auto_approve_deadline.replace(tzinfo=timezone.utc) if d.auto_approve_deadline.tzinfo is None else d.auto_approve_deadline
            if deadline <= now:
                inbound = db.query(InboundMessage).filter(InboundMessage.id == d.inbound_message_id).first()
                sentiment = inbound.detected_sentiment if inbound and hasattr(inbound, "detected_sentiment") else "neutral"
                intent = inbound.detected_intent if inbound and hasattr(inbound, "detected_intent") else "general_query"
                raw_text = inbound.raw_text if inbound else ""

                try:
                    eval_result = await llm_client.evaluate_safety(
                        original_message=raw_text,
                        draft_text=d.draft_text,
                        sentiment=sentiment,
                        intent=intent
                    )
                except Exception:
                    eval_result = None

                d.reviewed_at = now
                if eval_result and eval_result.safe_for_auto_approval and eval_result.recommended_action == "auto_approve_and_send":
                    d.status = "sent"
                    d.reviewed_by = "ORCHESTRATOR_AGENT"
                    d.sent_at = now
                    d.safety_evaluation_notes = f"Auto-approved by Orchestrator: {eval_result.reasoning}"

                    email_adapter = SimulatedEmailAdapter(db)
                    subject = f"Re: {inbound.subject}" if inbound and inbound.subject else "Response from Trentar Pvt Ltd"
                    recipient = inbound.sender_address if inbound else "customer@client.in"
                    await email_adapter.send_outbound(
                        recipient_address=recipient,
                        subject=subject,
                        body_text=d.draft_text,
                        reply_to_id=d.id
                    )

                    db.add(AuditLog(
                        entity_type="DRAFT",
                        entity_id=d.id,
                        action="AUTO_APPROVED",
                        actor_type="SYSTEM_ORCHESTRATOR",
                        actor_id="MODEL_ORCHESTRATOR",
                        details_json=json.dumps({"recipient": recipient, "safety_score": eval_result.safety_score, "action": "sent"}),
                        timestamp=now
                    ))
                else:
                    d.status = "escalated"
                    d.reviewed_by = "ORCHESTRATOR_AGENT"
                    reason = eval_result.reasoning if eval_result else "Safety review threshold flagged mandatory human sign-off"
                    d.safety_evaluation_notes = f"Escalated to human manager: {reason}"

                    db.add(AuditLog(
                        entity_type="DRAFT",
                        entity_id=d.id,
                        action="ESCALATED",
                        actor_type="SYSTEM_ORCHESTRATOR",
                        actor_id="MODEL_ORCHESTRATOR",
                        details_json=json.dumps({"reasons": eval_result.reasons if eval_result else ["Manual human manager sign-off required"]}),
                        timestamp=now
                    ))
                processed.append(d)
        if processed:
            db.commit()
        return processed

