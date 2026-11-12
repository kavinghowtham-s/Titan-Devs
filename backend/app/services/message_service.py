from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.app.config import settings
from backend.app.core.security import sanitize_input_text, inspect_prompt_injection
from backend.app.models.customer import Customer
from backend.app.models.product import Product
from backend.app.models.message import InboundMessage, DraftReply
from backend.app.models.stock import StockOrder, StockOrderItem
from backend.app.models.audit import AuditLog
from backend.app.llm.client import llm_client
from backend.app.seeds.sample_messages import SAMPLE_MESSAGES

class MessageService:
    @classmethod
    async def ingest_message(
        cls,
        db: Session,
        channel: str,
        sender_address: str,
        raw_text: str,
        subject: Optional[str] = None
    ) -> InboundMessage:
        sanitized_text = sanitize_input_text(raw_text)
        has_injection = inspect_prompt_injection(sanitized_text)

        # Run Intake LLM Agent
        classification = await llm_client.classify_intake(sanitized_text, channel=channel)
        if has_injection or classification.is_prompt_injection:
            classification.is_prompt_injection = True
            classification.priority = "urgent"

        # Match customer or associate
        customer = db.query(Customer).filter(Customer.email == sender_address).first()
        customer_id = customer.id if customer else None

        now = datetime.now(timezone.utc)
        inbound = InboundMessage(
            customer_id=customer_id,
            channel=channel,
            sender_address=sender_address,
            subject=subject or "Inquiry for Trentar Pvt Ltd",
            raw_text=sanitized_text,
            language=classification.language,
            detected_intent=classification.detected_intent,
            detected_sentiment=classification.sentiment,
            priority=classification.priority,
            prompt_injection_detected=classification.is_prompt_injection,
            processing_status="flagged" if classification.is_prompt_injection else "received",
            received_at=now
        )
        db.add(inbound)
        db.flush()

        # Audit log for ingestion
        db.add(AuditLog(
            entity_type="MESSAGE",
            entity_id=inbound.id,
            action="INGESTED" if not classification.is_prompt_injection else "SECURITY_BLOCKED",
            actor_type="INTAKE_AGENT",
            actor_id="MODEL_INTAKE",
            details_json=f'{{"intent": "{classification.detected_intent}", "priority": "{classification.priority}", "language": "{classification.language}"}}',
            timestamp=now
        ))

        # If injection detected, stop processing and do not call drafter
        if classification.is_prompt_injection:
            db.commit()
            return inbound

        # Check stock requirements & shortfalls (E2 integration)
        catalog_context_lines = []
        stock_context_lines = []
        for req in classification.requirements:
            if req.sku:
                prod = db.query(Product).filter(Product.sku == req.sku).first()
                if prod:
                    catalog_context_lines.append(f"SKU: {prod.sku} | Name: {prod.name} | Price: Rs. {prod.unit_selling_price:.2f}")
                    stock_context_lines.append(f"SKU: {prod.sku} | In-Hand: {prod.current_stock} | Requested: {req.quantity}")

                    if req.quantity > prod.current_stock:
                        shortfall = req.quantity - prod.current_stock
                        po_cost = round(shortfall * prod.unit_cost_price, 2)

                        stock_order = StockOrder(
                            order_number=f"PO-2026-{1000 + inbound.id}",
                            inbound_message_id=inbound.id,
                            supplier_id=prod.supplier_id,
                            status="draft",
                            total_estimated_cost=po_cost,
                            manager_notes=f"Auto-generated shortfall PO for {sender_address}"
                        )
                        db.add(stock_order)
                        db.flush()

                        db.add(StockOrderItem(
                            stock_order_id=stock_order.id,
                            product_id=prod.id,
                            requested_quantity=req.quantity,
                            in_hand_stock=prod.current_stock,
                            shortfall_quantity=shortfall,
                            estimated_unit_cost=prod.unit_cost_price,
                            subtotal=po_cost
                        ))

                        db.add(AuditLog(
                            entity_type="STOCK_ORDER",
                            entity_id=stock_order.id,
                            action="CREATED",
                            actor_type="SYSTEM",
                            actor_id="SHORTFALL_ENGINE",
                            details_json=f'{{"po": "{stock_order.order_number}", "shortfall": {shortfall}}}',
                            timestamp=now
                        ))

        catalog_ctx = "\n".join(catalog_context_lines) if catalog_context_lines else "General Trentar drone parts catalog."
        stock_ctx = "\n".join(stock_context_lines) if stock_context_lines else "Warehouse stock available."

        # Drafter Agent generates contextual response
        cust_name = customer.name if customer else sender_address.split("@")[0].title()
        draft_response = await llm_client.generate_draft(
            customer_name=cust_name,
            language=classification.language,
            message_text=sanitized_text,
            catalog_context=catalog_ctx,
            stock_context=stock_ctx
        )

        # Set deadline based on configured setting
        deadline = now + timedelta(minutes=settings.AUTO_APPROVE_DELAY_MINUTES)
        draft = DraftReply(
            inbound_message_id=inbound.id,
            draft_text=draft_response.body,
            status="pending",
            confidence_score=0.96,
            auto_approve_deadline=deadline,
            created_at=now
        )
        db.add(draft)
        inbound.processing_status = "drafted"

        db.add(AuditLog(
            entity_type="DRAFT",
            entity_id=inbound.id,
            action="CREATED",
            actor_type="MANAGER",
            actor_id="MODEL_DRAFTER",
            details_json=f'{{"subject": "{draft_response.subject}"}}',
            timestamp=now
        ))

        db.commit()
        db.refresh(inbound)
        return inbound

    @classmethod
    async def simulate_batch(cls, db: Session, scenario_ids: List[str]) -> List[int]:
        created_ids = []
        for scenario in SAMPLE_MESSAGES:
            if not scenario_ids or scenario["scenario_id"] in scenario_ids:
                msg = await cls.ingest_message(
                    db=db,
                    channel=scenario["channel"],
                    sender_address=scenario["sender_address"],
                    raw_text=scenario["raw_text"],
                    subject=scenario["subject"]
                )
                created_ids.append(msg.id)
        return created_ids

    @classmethod
    def get_messages(
        cls,
        db: Session,
        status: Optional[str] = None,
        intent: Optional[str] = None,
        priority: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[InboundMessage]:
        query = db.query(InboundMessage)
        if status:
            query = query.filter(InboundMessage.processing_status == status)
        if intent:
            query = query.filter(InboundMessage.detected_intent == intent)
        if priority:
            query = query.filter(InboundMessage.priority == priority)
        return query.order_by(InboundMessage.received_at.desc()).offset(offset).limit(limit).all()

    @classmethod
    def get_message_detail(cls, db: Session, message_id: int) -> Optional[Dict[str, Any]]:
        msg = db.query(InboundMessage).filter(InboundMessage.id == message_id).first()
        if not msg:
            return None
        
        draft = db.query(DraftReply).filter(DraftReply.inbound_message_id == msg.id).first()
        stock_order = db.query(StockOrder).filter(StockOrder.inbound_message_id == msg.id).first()
        customer = db.query(Customer).filter(Customer.id == msg.customer_id).first() if msg.customer_id else None

        return {
            "message": msg,
            "draft": draft,
            "stock_order": stock_order,
            "customer": customer
        }

