"""Unit tests for the Task dataclass."""

import pytest
from src.service.task import Task


class TestTask:
    """Test cases for Task initialization and behavior."""

    def test_task_creation_with_title_only(self):
        """Test creating a task with just a title."""
        task = Task(title="Buy milk")
        assert task.title == "Buy milk"
        assert task.description == ""
        assert task.completed is False
        assert task.id == 0

    def test_task_creation_with_all_fields(self):
        """Test creating a task with all fields."""
        task = Task(
            title="Buy milk",
            description="Get 2% from store",
            completed=True,
            id=1,
        )
        assert task.title == "Buy milk"
        assert task.description == "Get 2% from store"
        assert task.completed is True
        assert task.id == 1

    def test_task_title_stripped(self):
        """Test that title whitespace is stripped."""
        task = Task(title="  Buy milk  ")
        assert task.title == "Buy milk"

    def test_task_description_stripped(self):
        """Test that description whitespace is stripped."""
        task = Task(title="Buy milk", description="  Get 2% from store  ")
        assert task.description == "Get 2% from store"

    def test_task_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="")

    def test_task_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="   ")

    def test_task_completed_defaults_to_false(self):
        """Test that completed defaults to False."""
        task = Task(title="Test task")
        assert task.completed is False

    def test_task_id_defaults_to_zero(self):
        """Test that id defaults to 0."""
        task = Task(title="Test task")
        assert task.id == 0

    def test_task_equality(self):
        """Test that two tasks with same values are equal."""
        task1 = Task(title="Buy milk", id=1)
        task2 = Task(title="Buy milk", id=1)
        assert task1 == task2

    def test_task_inequality(self):
        """Test that tasks with different values are not equal."""
        task1 = Task(title="Buy milk", id=1)
        task2 = Task(title="Buy eggs", id=1)
        assert task1 != task2

    def test_task_repr(self):
        """Test task string representation."""
        task = Task(title="Buy milk", id=1)
        assert "Buy milk" in repr(task)
        assert "1" in repr(task)
