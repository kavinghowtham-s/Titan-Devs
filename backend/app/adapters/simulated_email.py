from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from backend.app.adapters.base import ChannelAdapter
from backend.app.models.message import OutboxMessage

class SimulatedEmailAdapter(ChannelAdapter):
    """Logs sent emails directly to the outbox database table for live demonstration."""

    def __init__(self, db: Session):
        self.db = db

    async def send_outbound(
        self,
        recipient_address: str,
        subject: Optional[str],
        body_text: str,
        reply_to_id: Optional[int] = None
    ) -> bool:
        outbox_entry = OutboxMessage(
            draft_reply_id=reply_to_id,
            channel="email",
            recipient_address=recipient_address,
            subject=subject or "Response from Trentar Pvt Ltd",
            body_text=body_text,
            dispatched_at=datetime.now(timezone.utc),
            delivery_status="DELIVERED"
        )
        self.db.add(outbox_entry)
        self.db.commit()
        return True

