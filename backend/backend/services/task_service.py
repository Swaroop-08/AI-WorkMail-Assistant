"""
Task Service — CRUD operations for tasks extracted from emails.
"""
from sqlalchemy.orm import Session
from models import Task, Email
from typing import List, Optional


def create_task(db: Session, email_id: int, task_data: dict) -> Task:
    """Create a new task linked to an email."""
    task = Task(
        email_id=email_id,
        task_type=task_data.get("task_type", "General"),
        description=task_data.get("description", ""),
        deadline=task_data.get("deadline", ""),
        people_involved=task_data.get("people_involved", ""),
        priority=task_data.get("priority", "medium"),
        status=task_data.get("status", "todo"),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_all_tasks(
    db: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
) -> List[Task]:
    """Get all tasks, optionally filtered by status or priority."""
    query = db.query(Task)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    return query.order_by(Task.created_at.desc()).all()


def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    """Get a single task by ID."""
    return db.query(Task).filter(Task.id == task_id).first()


def update_task_status(db: Session, task_id: int, new_status: str) -> Optional[Task]:
    """Update a task's status (todo, in_progress, done)."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = new_status
        db.commit()
        db.refresh(task)
    return task


def get_tasks_for_email(db: Session, email_id: int) -> List[Task]:
    """Get all tasks associated with an email."""
    return db.query(Task).filter(Task.email_id == email_id).all()


def get_task_stats(db: Session) -> dict:
    """Get task statistics."""
    total = db.query(Task).count()
    todo = db.query(Task).filter(Task.status == "todo").count()
    in_progress = db.query(Task).filter(Task.status == "in_progress").count()
    done = db.query(Task).filter(Task.status == "done").count()
    high_priority = db.query(Task).filter(Task.priority == "high").count()

    return {
        "total": total,
        "todo": todo,
        "in_progress": in_progress,
        "done": done,
        "high_priority": high_priority,
    }
