"""
Tasks Router — endpoints for listing and managing extracted tasks.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task, Email
from schemas import TaskResponse, TaskStatusUpdate, ActionResponse
from services.task_service import get_all_tasks, get_task_by_id, update_task_status, get_task_stats
from typing import List, Optional

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[TaskResponse])
def list_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """List all tasks with optional filters."""
    tasks = get_all_tasks(db, status=status, priority=priority)
    result = []
    for task in tasks:
        email = db.query(Email).filter(Email.id == task.email_id).first()
        task_resp = TaskResponse(
            id=task.id,
            email_id=task.email_id,
            task_type=task.task_type,
            description=task.description,
            deadline=task.deadline,
            people_involved=task.people_involved,
            priority=task.priority,
            status=task.status,
            created_at=task.created_at,
            email_subject=email.subject if email else "",
            email_sender=email.sender_name or email.sender if email else "",
        )
        result.append(task_resp)
    return result


@router.get("/stats")
def task_stats(db: Session = Depends(get_db)):
    """Get task statistics."""
    return get_task_stats(db)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a single task by ID."""
    task = get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    email = db.query(Email).filter(Email.id == task.email_id).first()
    return TaskResponse(
        id=task.id,
        email_id=task.email_id,
        task_type=task.task_type,
        description=task.description,
        deadline=task.deadline,
        people_involved=task.people_involved,
        priority=task.priority,
        status=task.status,
        created_at=task.created_at,
        email_subject=email.subject if email else "",
        email_sender=email.sender_name or email.sender if email else "",
    )


@router.patch("/{task_id}/status", response_model=ActionResponse)
def change_task_status(
    task_id: int,
    update: TaskStatusUpdate,
    db: Session = Depends(get_db),
):
    """Update a task's status (todo, in_progress, done)."""
    if update.status not in ("todo", "in_progress", "done"):
        raise HTTPException(
            status_code=400,
            detail="Status must be one of: todo, in_progress, done"
        )

    task = update_task_status(db, task_id, update.status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return ActionResponse(
        message=f"Task status updated to {update.status}",
        success=True,
    )
