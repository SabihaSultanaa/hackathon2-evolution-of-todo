"""Tests for task endpoints."""

import pytest
from sqlmodel import select
from app.models.user import User
from app.models.task import Task
from app.auth.security import hash_password, create_access_token


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        hashed_password=hash_password("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    """Create authorization headers for test user."""
    token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def other_user(db_session):
    """Create another test user."""
    user = User(
        email="other@example.com",
        hashed_password=hash_password("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def other_auth_headers(other_user):
    """Create authorization headers for other user."""
    token = create_access_token(data={"sub": str(other_user.id)})
    return {"Authorization": f"Bearer {token}"}


def test_create_task(client, auth_headers):
    """Test creating a task."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["description"] == "Test description"
    assert data["completed"] == False


def test_create_task_empty_title(client, auth_headers):
    """Test creating a task with empty title fails."""
    response = client.post(
        "/api/v1/tasks",
        json={"title": "", "description": "Test description"},
        headers=auth_headers
    )
    assert response.status_code == 422  # Validation error


def test_list_tasks_empty(client, auth_headers):
    """Test listing tasks when user has none."""
    response = client.get("/api/v1/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["tasks"] == []


def test_list_tasks(client, auth_headers, db_session, test_user):
    """Test listing user's tasks."""
    # Create tasks for user
    task1 = Task(title="Task 1", user_id=test_user.id)
    task2 = Task(title="Task 2", description="Description", user_id=test_user.id)
    db_session.add_all([task1, task2])
    db_session.commit()

    response = client.get("/api/v1/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 2


def test_list_tasks_user_isolation(client, auth_headers, db_session, test_user, other_user):
    """Test that user only sees their own tasks."""
    # Create task for test_user
    task = Task(title="My task", user_id=test_user.id)
    db_session.add(task)
    db_session.commit()

    # Create task for other_user
    other_task = Task(title="Other task", user_id=other_user.id)
    db_session.add(other_task)
    db_session.commit()

    # Test user should only see their own task
    response = client.get("/api/v1/tasks", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["tasks"]) == 1
    assert data["tasks"][0]["title"] == "My task"


def test_update_task(client, auth_headers, db_session, test_user):
    """Test updating a task."""
    task = Task(title="Original title", user_id=test_user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    response = client.put(
        f"/api/v1/tasks/{task.id}",
        json={"title": "Updated title", "description": "Updated description"},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["description"] == "Updated description"


def test_update_task_not_found(client, auth_headers):
    """Test updating a nonexistent task."""
    response = client.put(
        "/api/v1/tasks/99999",
        json={"title": "Updated title"},
        headers=auth_headers
    )
    assert response.status_code == 404


def test_update_task_not_owned(client, auth_headers, db_session, other_user):
    """Test updating another user's task fails."""
    task = Task(title="Other's task", user_id=other_user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    response = client.put(
        f"/api/v1/tasks/{task.id}",
        json={"title": "Hacked title"},
        headers=auth_headers
    )
    assert response.status_code == 404  # Not found (user isolation)


def test_toggle_task(client, auth_headers, db_session, test_user):
    """Test toggling task completion."""
    task = Task(title="Task to toggle", user_id=test_user.id, completed=False)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    response = client.patch(
        f"/api/v1/tasks/{task.id}/toggle",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == True

    # Toggle again
    response = client.patch(
        f"/api/v1/tasks/{task.id}/toggle",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == False


def test_delete_task(client, auth_headers, db_session, test_user):
    """Test deleting a task."""
    task = Task(title="Task to delete", user_id=test_user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    task_id = task.id

    response = client.delete(
        f"/api/v1/tasks/{task_id}",
        headers=auth_headers
    )
    assert response.status_code == 204

    # Verify task is deleted
    deleted_task = db_session.get(Task, task_id)
    assert deleted_task is None


def test_delete_task_not_found(client, auth_headers):
    """Test deleting a nonexistent task."""
    response = client.delete(
        "/api/v1/tasks/99999",
        headers=auth_headers
    )
    assert response.status_code == 404


def test_delete_task_not_owned(client, auth_headers, db_session, other_user):
    """Test deleting another user's task fails."""
    task = Task(title="Other's task", user_id=other_user.id)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    response = client.delete(
        f"/api/v1/tasks/{task.id}",
        headers=auth_headers
    )
    assert response.status_code == 404


def test_access_without_token(client):
    """Test accessing protected endpoint without token."""
    response = client.get("/api/v1/tasks")
    assert response.status_code == 401


def test_access_with_invalid_token(client):
    """Test accessing protected endpoint with invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/tasks", headers=headers)
    assert response.status_code == 401
