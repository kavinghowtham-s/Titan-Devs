from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.message_dto import InboundMessageCreate, InboundMessageResponse
from backend.app.services.message_service import MessageService

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/webhook", response_model=InboundMessageResponse)
async def ingest_webhook_message(
    payload: InboundMessageCreate,
    db: Session = Depends(get_db)
):
    """Ingest a live inbound customer message from Email, WhatsApp, or Webhook."""
    try:
        message = await MessageService.ingest_message(
            db=db,
            channel=payload.channel,
            sender_address=payload.sender_address,
            raw_text=payload.raw_text,
            subject=payload.subject
        )
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/simulate-batch")
async def simulate_batch_messages(
    scenario_ids: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db)
):
    """Bulk loads pre-configured demo scenarios into the pipeline for judging walkthrough."""
    try:
        created_ids = await MessageService.simulate_batch(db, scenario_ids or [])
        return {"success": True, "ingested_count": len(created_ids), "message_ids": created_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=List[InboundMessageResponse])
def list_messages(
    status: Optional[str] = Query(None),
    intent: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Retrieve filtered inbound customer messages."""
    return MessageService.get_messages(db, status=status, intent=intent, priority=priority, limit=limit, offset=offset)

@router.get("/{message_id}")
def get_message_detail(
    message_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve full context for an inquiry including draft and stock status."""
    detail = MessageService.get_message_detail(db, message_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Message not found")
    return detail

