from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.schemas.draft_dto import DraftReplyResponse, DraftReplyEdit
from backend.app.services.draft_service import DraftService

router = APIRouter(prefix="/drafts", tags=["Drafts & Approvals"])

@router.get("/pending", response_model=List[DraftReplyResponse])
def get_pending_drafts(
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieve all drafts awaiting manager review with active countdown seconds."""
    return DraftService.get_pending_drafts(db, limit=limit)

@router.post("/{draft_id}/approve", response_model=DraftReplyResponse)
async def approve_draft(
    draft_id: int,
    db: Session = Depends(get_db)
):
    """Manager 1-click Approve: marks draft sent and dispatches outbound email."""
    try:
        return await DraftService.approve_draft(db, draft_id, actor_id="MANAGER_RAJESH")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/process-expirations", response_model=List[DraftReplyResponse])
async def process_expirations(
    db: Session = Depends(get_db)
):
    """Trigger Orchestrator safety check on all drafts exceeding auto-approval SLA."""
    try:
        return await DraftService.process_expired_drafts(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{draft_id}/edit", response_model=DraftReplyResponse)
def edit_draft(
    draft_id: int,
    payload: DraftReplyEdit,
    db: Session = Depends(get_db)
):
    """Modify draft response text before manager approval."""
    try:
        return DraftService.edit_draft(db, draft_id, payload.edited_text, actor_id="MANAGER_RAJESH")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{draft_id}/reject", response_model=DraftReplyResponse)
def reject_draft(
    draft_id: int,
    reason: str = Query("Rejected by manager"),
    db: Session = Depends(get_db)
):
    """Reject AI draft reply and halt outbound dispatch."""
    try:
        return DraftService.reject_draft(db, draft_id, reason, actor_id="MANAGER_RAJESH")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

