"""
Email Router — endpoints for fetching, listing, and processing emails.
"""
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Email, Suggestion
from schemas import (
    EmailResponse,
    EmailListItem,
    SuggestionResponse,
    SuggestionStatusUpdate,
    FetchEmailsResponse,
    ActionResponse,
)
from services.gmail_service import fetch_latest_emails
from services.ai_service import classify_email, extract_tasks, generate_suggestions
from services.task_service import create_task
from typing import List

router = APIRouter(prefix="/api/emails", tags=["emails"])

DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"


@router.post("/fetch")
def fetch_emails(db: Session = Depends(get_db)):
    """Fetch latest emails from Gmail (or demo data) and process with AI."""
    import traceback
    try:
        print("[ROUTER] Starting email fetch...")
        raw_emails = fetch_latest_emails(max_results=20)
        print(f"[ROUTER] Got {len(raw_emails)} raw emails")
    except Exception as e:
        error_msg = f"Failed to fetch emails: {str(e)}"
        print(f"[ROUTER] ERROR: {error_msg}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)

    fetched = 0
    processed = 0

    for email_data in raw_emails:
        # Skip if already in DB
        existing = db.query(Email).filter(Email.gmail_id == email_data["gmail_id"]).first()
        if existing:
            continue

        # Create email record
        email = Email(
            gmail_id=email_data["gmail_id"],
            sender=email_data["sender"],
            sender_name=email_data.get("sender_name", ""),
            subject=email_data["subject"],
            body=email_data["body"],
            snippet=email_data.get("snippet", ""),
            received_at=email_data.get("received_at"),
            is_read=email_data.get("is_read", False),
        )
        db.add(email)
        db.flush()  # Get the ID without committing
        fetched += 1

        # If demo data has pre-computed classifications, use them
        if email_data.get("classification"):
            email.classification = email_data["classification"]
            email.intent = email_data.get("intent", "general")
            email.priority = email_data.get("priority", "medium")
        else:
            # Classify with AI
            classification = classify_email(email.subject, email.body)
            email.classification = classification["classification"]
            email.intent = classification["intent"]
            email.priority = classification["priority"]

        email.processed = True
        processed += 1

        # Extract tasks
        if email.classification == "actionable":
            if DEMO_MODE:
                from demo_data import DEMO_TASKS
                email_idx = next(
                    (i for i, e in enumerate(raw_emails) if e["gmail_id"] == email_data["gmail_id"]),
                    -1,
                )
                demo_tasks = [t for t in DEMO_TASKS if t["email_index"] == email_idx]
                for task_data in demo_tasks:
                    create_task(db, email.id, task_data)
            else:
                tasks = extract_tasks(email.subject, email.body, email.sender)
                for task_data in tasks:
                    create_task(db, email.id, task_data)

        # Generate suggestions
        if DEMO_MODE:
            from demo_data import DEMO_SUGGESTIONS
            email_idx = next(
                (i for i, e in enumerate(raw_emails) if e["gmail_id"] == email_data["gmail_id"]),
                -1,
            )
            demo_suggestions = [s for s in DEMO_SUGGESTIONS if s["email_index"] == email_idx]
            for sug_data in demo_suggestions:
                suggestion = Suggestion(
                    email_id=email.id,
                    suggestion_type=sug_data["suggestion_type"],
                    title=sug_data["title"],
                    content=sug_data["content"],
                    status="pending",
                )
                db.add(suggestion)
        else:
            suggestions = generate_suggestions(
                email.subject, email.body, email.sender, email.intent
            )
            for sug_data in suggestions:
                suggestion = Suggestion(
                    email_id=email.id,
                    suggestion_type=sug_data["suggestion_type"],
                    title=sug_data["title"],
                    content=sug_data["content"],
                    status="pending",
                )
                db.add(suggestion)

    db.commit()

    # In demo mode, also create follow-ups
    if DEMO_MODE and fetched > 0:
        from demo_data import DEMO_FOLLOWUPS
        from models import FollowUp

        for fu_data in DEMO_FOLLOWUPS:
            email_idx = fu_data["email_index"]
            if email_idx < len(raw_emails):
                email = (
                    db.query(Email)
                    .filter(Email.gmail_id == raw_emails[email_idx]["gmail_id"])
                    .first()
                )
                if email:
                    existing_fu = (
                        db.query(FollowUp).filter(FollowUp.email_id == email.id).first()
                    )
                    if not existing_fu:
                        fu = FollowUp(
                            email_id=email.id,
                            suggested_message=fu_data["suggested_message"],
                            reason=fu_data["reason"],
                            status="pending",
                            hours_elapsed=fu_data.get("hours_elapsed", 24),
                        )
                        db.add(fu)
        db.commit()

    return FetchEmailsResponse(
        message=f"Fetched {fetched} emails, processed {processed} with AI",
        emails_fetched=fetched,
        emails_processed=processed,
    )


@router.get("", response_model=List[EmailListItem])
def list_emails(
    classification: str = None,
    intent: str = None,
    db: Session = Depends(get_db),
):
    """List all processed emails with optional filters."""
    query = db.query(Email)
    if classification:
        query = query.filter(Email.classification == classification)
    if intent:
        query = query.filter(Email.intent == intent)

    emails = query.order_by(Email.received_at.desc()).all()

    result = []
    for email in emails:
        item = EmailListItem(
            id=email.id,
            gmail_id=email.gmail_id,
            sender=email.sender,
            sender_name=email.sender_name,
            subject=email.subject,
            snippet=email.snippet,
            received_at=email.received_at,
            is_read=email.is_read,
            classification=email.classification,
            intent=email.intent,
            priority=email.priority,
            processed=email.processed,
            suggestion_count=len(email.suggestions),
            task_count=len(email.tasks),
        )
        result.append(item)

    return result


@router.get("/{email_id}", response_model=EmailResponse)
def get_email(email_id: int, db: Session = Depends(get_db)):
    """Get a single email with its tasks and suggestions."""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email


@router.get("/{email_id}/suggestions", response_model=List[SuggestionResponse])
def get_email_suggestions(email_id: int, db: Session = Depends(get_db)):
    """Get AI suggestions for a specific email."""
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Email not found")
    return email.suggestions


@router.post("/{email_id}/suggestions/{suggestion_id}/approve", response_model=ActionResponse)
def approve_suggestion(
    email_id: int,
    suggestion_id: int,
    db: Session = Depends(get_db),
):
    """Approve an AI suggestion."""
    suggestion = (
        db.query(Suggestion)
        .filter(Suggestion.id == suggestion_id, Suggestion.email_id == email_id)
        .first()
    )
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    suggestion.status = "approved"
    db.commit()
    return ActionResponse(message="Suggestion approved successfully", success=True)


@router.post("/{email_id}/suggestions/{suggestion_id}/dismiss", response_model=ActionResponse)
def dismiss_suggestion(
    email_id: int,
    suggestion_id: int,
    db: Session = Depends(get_db),
):
    """Dismiss an AI suggestion."""
    suggestion = (
        db.query(Suggestion)
        .filter(Suggestion.id == suggestion_id, Suggestion.email_id == email_id)
        .first()
    )
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    suggestion.status = "dismissed"
    db.commit()
    return ActionResponse(message="Suggestion dismissed", success=True)
