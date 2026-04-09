"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ────────────────── Email ──────────────────

class EmailBase(BaseModel):
    gmail_id: str
    sender: str
    sender_name: str = ""
    subject: str
    body: str
    snippet: str = ""
    received_at: Optional[datetime] = None
    is_read: bool = False


class EmailResponse(EmailBase):
    id: int
    classification: str = ""
    intent: str = ""
    priority: str = "medium"
    processed: bool = False
    tasks: List["TaskResponse"] = []
    suggestions: List["SuggestionResponse"] = []

    class Config:
        from_attributes = True


class EmailListItem(BaseModel):
    id: int
    gmail_id: str
    sender: str
    sender_name: str
    subject: str
    snippet: str
    received_at: Optional[datetime]
    is_read: bool
    classification: str
    intent: str
    priority: str
    processed: bool
    suggestion_count: int = 0
    task_count: int = 0

    class Config:
        from_attributes = True


# ────────────────── Task ──────────────────

class TaskBase(BaseModel):
    task_type: str
    description: str
    deadline: str = ""
    people_involved: str = ""
    priority: str = "medium"
    status: str = "todo"


class TaskCreate(TaskBase):
    email_id: int


class TaskResponse(TaskBase):
    id: int
    email_id: int
    created_at: Optional[datetime] = None
    email_subject: str = ""
    email_sender: str = ""

    class Config:
        from_attributes = True


class TaskStatusUpdate(BaseModel):
    status: str


# ────────────────── Suggestion ──────────────────

class SuggestionBase(BaseModel):
    suggestion_type: str
    title: str
    content: str
    status: str = "pending"


class SuggestionResponse(SuggestionBase):
    id: int
    email_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SuggestionStatusUpdate(BaseModel):
    status: str  # "approved" or "dismissed"


# ────────────────── FollowUp ──────────────────

class FollowUpBase(BaseModel):
    suggested_message: str
    reason: str = "No reply received within 24 hours"
    status: str = "pending"
    hours_elapsed: int = 24


class FollowUpResponse(FollowUpBase):
    id: int
    email_id: int
    detected_at: Optional[datetime] = None
    email_subject: str = ""
    email_sender: str = ""

    class Config:
        from_attributes = True


# ────────────────── Stats ──────────────────

class DashboardStats(BaseModel):
    total_emails: int = 0
    actionable_emails: int = 0
    informational_emails: int = 0
    total_tasks: int = 0
    pending_tasks: int = 0
    completed_tasks: int = 0
    pending_followups: int = 0
    pending_suggestions: int = 0


# ────────────────── API Responses ──────────────────

class FetchEmailsResponse(BaseModel):
    message: str
    emails_fetched: int = 0
    emails_processed: int = 0


class ActionResponse(BaseModel):
    message: str
    success: bool = True
