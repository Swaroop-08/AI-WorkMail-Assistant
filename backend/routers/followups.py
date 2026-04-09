"""
Follow-Up Router — endpoints for managing follow-up suggestions.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import FollowUp, Email
from schemas import FollowUpResponse, ActionResponse
from services.followup_service import (
    get_pending_followups,
    get_all_followups,
    update_followup_status,
    scan_and_create_followups,
)
from typing import List

router = APIRouter(prefix="/api/followups", tags=["followups"])


@router.get("", response_model=List[FollowUpResponse])
def list_followups(status: str = None, db: Session = Depends(get_db)):
    """List all follow-ups, optionally filtered by status."""
    if status == "pending":
        followups = get_pending_followups(db)
    else:
        followups = get_all_followups(db)

    result = []
    for fu in followups:
        email = db.query(Email).filter(Email.id == fu.email_id).first()
        result.append(
            FollowUpResponse(
                id=fu.id,
                email_id=fu.email_id,
                suggested_message=fu.suggested_message,
                reason=fu.reason,
                status=fu.status,
                detected_at=fu.detected_at,
                hours_elapsed=fu.hours_elapsed,
                email_subject=email.subject if email else "",
                email_sender=email.sender_name or email.sender if email else "",
            )
        )
    return result


@router.post("/scan", response_model=ActionResponse)
def scan_followups(db: Session = Depends(get_db)):
    """Scan for stale emails and create follow-up suggestions."""
    created = scan_and_create_followups(db)
    return ActionResponse(
        message=f"Scan complete. Created {len(created)} new follow-up suggestions.",
        success=True,
    )


@router.post("/{followup_id}/approve", response_model=ActionResponse)
def approve_followup(followup_id: int, db: Session = Depends(get_db)):
    """Approve a follow-up suggestion (marks as approved, doesn't auto-send)."""
    followup = update_followup_status(db, followup_id, "approved")
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return ActionResponse(message="Follow-up approved", success=True)


@router.post("/{followup_id}/dismiss", response_model=ActionResponse)
def dismiss_followup(followup_id: int, db: Session = Depends(get_db)):
    """Dismiss a follow-up suggestion."""
    followup = update_followup_status(db, followup_id, "dismissed")
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return ActionResponse(message="Follow-up dismissed", success=True)
