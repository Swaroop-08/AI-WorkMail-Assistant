"""
AI Inbox Executive — FastAPI Backend
Main application entry point.
"""
import os
from dotenv import load_dotenv

# Load environment variables BEFORE importing anything else
load_dotenv()

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_db
from routers import emails, tasks, followups
from sqlalchemy.orm import Session
from models import Email, Task, Suggestion, FollowUp

app = FastAPI(
    title="AI Inbox Executive",
    description="AI-powered email assistant that detects intent and converts emails into actionable tasks",
    version="1.0.0",
)

# CORS — allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(emails.router)
app.include_router(tasks.router)
app.include_router(followups.router)


@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    init_db()
    print("✅ Database initialized")
    print(f"📧 Demo Mode: {os.getenv('DEMO_MODE', 'true')}")
    print(f"🤖 OpenAI Key: {'configured' if os.getenv('OPENAI_API_KEY') else 'not set (using mock AI)'}")


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "app": "AI Inbox Executive",
        "version": "1.0.0",
        "status": "running",
        "demo_mode": os.getenv("DEMO_MODE", "true").lower() == "true",
    }


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics."""
    total_emails = db.query(Email).count()
    actionable = db.query(Email).filter(Email.classification == "actionable").count()
    informational = db.query(Email).filter(Email.classification == "informational").count()
    total_tasks = db.query(Task).count()
    pending_tasks = db.query(Task).filter(Task.status.in_(["todo", "in_progress"])).count()
    completed_tasks = db.query(Task).filter(Task.status == "done").count()
    pending_followups = db.query(FollowUp).filter(FollowUp.status == "pending").count()
    pending_suggestions = db.query(Suggestion).filter(Suggestion.status == "pending").count()

    return {
        "total_emails": total_emails,
        "actionable_emails": actionable,
        "informational_emails": informational,
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "completed_tasks": completed_tasks,
        "pending_followups": pending_followups,
        "pending_suggestions": pending_suggestions,
    }


@app.delete("/api/reset")
def reset_data(db: Session = Depends(get_db)):
    """Reset all data (development only)."""
    db.query(FollowUp).delete()
    db.query(Suggestion).delete()
    db.query(Task).delete()
    db.query(Email).delete()
    db.commit()
    return {"message": "All data reset successfully"}
