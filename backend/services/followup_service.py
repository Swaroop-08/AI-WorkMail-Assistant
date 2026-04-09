"""
Follow-Up Service — detects stale emails and generates follow-up suggestions.
"""
import os
from sqlalchemy.orm import Session
from models import Email, FollowUp
from datetime import datetime, timezone, timedelta
from typing import List, Optional

DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"


def detect_stale_emails(db: Session, hours: int = 24) -> List[Email]:
    """
    Find emails that are actionable and have no follow-up created yet,
    and were received more than `hours` hours ago.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)

    stale_emails = (
        db.query(Email)
        .filter(
            Email.classification == "actionable",
            Email.received_at <= cutoff,
            Email.processed == True,  # noqa
        )
        .all()
    )

    # Filter out emails that already have active follow-ups
    result = []
    for email in stale_emails:
        existing = (
            db.query(FollowUp)
            .filter(
                FollowUp.email_id == email.id,
                FollowUp.status.in_(["pending", "approved", "sent"]),
            )
            .first()
        )
        if not existing:
            result.append(email)

    return result


def create_follow_up(
    db: Session,
    email_id: int,
    suggested_message: str,
    reason: str = "No reply received within 24 hours",
    hours_elapsed: int = 24,
) -> FollowUp:
    """Create a follow-up suggestion for an email."""
    follow_up = FollowUp(
        email_id=email_id,
        suggested_message=suggested_message,
        reason=reason,
        status="pending",
        hours_elapsed=hours_elapsed,
    )
    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)
    return follow_up


def get_pending_followups(db: Session) -> List[FollowUp]:
    """Get all pending follow-ups."""
    return (
        db.query(FollowUp)
        .filter(FollowUp.status == "pending")
        .order_by(FollowUp.detected_at.desc())
        .all()
    )


def get_all_followups(db: Session) -> List[FollowUp]:
    """Get all follow-ups."""
    return db.query(FollowUp).order_by(FollowUp.detected_at.desc()).all()


def update_followup_status(db: Session, followup_id: int, new_status: str) -> Optional[FollowUp]:
    """Update follow-up status (approved, dismissed)."""
    followup = db.query(FollowUp).filter(FollowUp.id == followup_id).first()
    if followup:
        followup.status = new_status
        db.commit()
        db.refresh(followup)
    return followup


def scan_and_create_followups(db: Session) -> List[FollowUp]:
    """Scan for stale emails and create follow-up suggestions."""
    from services.ai_service import generate_follow_up_message

    stale_emails = detect_stale_emails(db, hours=24)
    created = []

    for email in stale_emails:
        hours_since = int(
            (datetime.now(timezone.utc) - email.received_at).total_seconds() / 3600
        )

        message = generate_follow_up_message(email.subject, email.body, email.sender)

        follow_up = create_follow_up(
            db=db,
            email_id=email.id,
            suggested_message=message,
            reason=f"No reply received — {hours_since} hours since original email",
            hours_elapsed=hours_since,
        )
        created.append(follow_up)

    return created
