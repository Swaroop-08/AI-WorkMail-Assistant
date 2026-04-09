"""
SQLAlchemy ORM models for the AI Inbox Executive.
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timezone
import enum


class ClassificationType(str, enum.Enum):
    ACTIONABLE = "actionable"
    INFORMATIONAL = "informational"


class IntentType(str, enum.Enum):
    REPLY_REQUIRED = "reply_required"
    SCHEDULE_MEETING = "schedule_meeting"
    SEND_DOCUMENT = "send_document"
    FOLLOW_UP_NEEDED = "follow_up_needed"
    GENERAL = "general"


class PriorityLevel(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class SuggestionType(str, enum.Enum):
    REPLY_DRAFT = "reply_draft"
    CALENDAR_EVENT = "calendar_event"
    TASK_CREATION = "task_creation"
    FOLLOW_UP = "follow_up"


class SuggestionStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DISMISSED = "dismissed"


class FollowUpStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DISMISSED = "dismissed"
    SENT = "sent"


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    gmail_id = Column(String(255), unique=True, index=True)
    sender = Column(String(500))
    sender_name = Column(String(255), default="")
    subject = Column(String(1000))
    body = Column(Text)
    snippet = Column(String(500))
    received_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_read = Column(Boolean, default=False)
    classification = Column(String(50), default="")
    intent = Column(String(50), default="")
    priority = Column(String(20), default="medium")
    processed = Column(Boolean, default=False)

    tasks = relationship("Task", back_populates="email", cascade="all, delete-orphan")
    suggestions = relationship("Suggestion", back_populates="email", cascade="all, delete-orphan")
    follow_ups = relationship("FollowUp", back_populates="email", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"))
    task_type = Column(String(100))
    description = Column(Text)
    deadline = Column(String(100), default="")
    people_involved = Column(String(500), default="")
    priority = Column(String(20), default="medium")
    status = Column(String(20), default="todo")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    email = relationship("Email", back_populates="tasks")


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"))
    suggestion_type = Column(String(50))
    title = Column(String(255))
    content = Column(Text)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    email = relationship("Email", back_populates="suggestions")


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(Integer, ForeignKey("emails.id"))
    suggested_message = Column(Text)
    reason = Column(String(500), default="No reply received within 24 hours")
    status = Column(String(20), default="pending")
    detected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    hours_elapsed = Column(Integer, default=24)

    email = relationship("Email", back_populates="follow_ups")
