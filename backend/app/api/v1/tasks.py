"""Task CRUD endpoints with user isolation."""

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import select
from app.database import get_db
from app.models.user import User
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.auth.security import decode_access_token
from sqlalchemy.orm import Session

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    db: Session = Depends(get_db)
) -> User:
    """Dependency to get the current authenticated user from JWT token."""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization[7:]  # Remove "Bearer " prefix

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: int | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.get(User, int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


@router.get("", response_model=TaskListResponse)
def list_tasks(
    category: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all tasks for the current user."""
    query = select(Task).where(Task.user_id == current_user.id)

    if category:
        query = query.where(Task.category == category)

    tasks = db.execute(
        query.order_by(Task.created_at.desc())
    ).scalars().all()

    return TaskListResponse(tasks=tasks)


@router.post("/validate-token")
def validate_token(
    token: str,
    db: Session = Depends(get_db)
):
    """Validate a JWT token and return user information.

    Used by MCP server to verify session tokens before executing operations.
    """
    try:
        payload = decode_access_token(token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = db.get(User, int(user_id))
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "valid": True,
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }

    except Exception as e:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired session token",
                headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task for the current user."""
    task = Task(
        title=task_data.title,
        description=task_data.description,
        category=task_data.category,
        user_id=current_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a task (full update)."""
    task = db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).scalars().first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle task completion status."""
    task = db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).scalars().first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion status
    task.completed = not task.completed
    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task."""
    task = db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).scalars().first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()
