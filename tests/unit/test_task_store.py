"""Unit tests for the TaskStore class."""

import pytest
from src.service.task_store import TaskStore
from src.service.task import Task


class TestTaskStore:
    """Test cases for TaskStore operations."""

    def setup_method(self):
        """Create a fresh TaskStore for each test."""
        self.store = TaskStore()

    def test_add_task_returns_id(self):
        """Test that add_task returns the new task's ID."""
        task_id = self.store.add_task("Buy milk")
        assert task_id == 1

    def test_add_multiple_tasks_increments_id(self):
        """Test that each new task gets a unique auto-incremented ID."""
        id1 = self.store.add_task("Buy milk")
        id2 = self.store.add_task("Buy eggs")
        id3 = self.store.add_task("Buy bread")
        assert (id1, id2, id3) == (1, 2, 3)

    def test_add_task_with_description(self):
        """Test adding a task with description."""
        task_id = self.store.add_task("Buy milk", "Get 2% from store")
        task = self.store.get_task(task_id)
        assert task is not None
        assert task.description == "Get 2% from store"

    def test_list_tasks_empty(self):
        """Test that list_tasks returns empty list when no tasks."""
        assert self.store.list_tasks() == []

    def test_list_tasks_returns_all_tasks(self):
        """Test that list_tasks returns all tasks."""
        self.store.add_task("Buy milk")
        self.store.add_task("Buy eggs")
        tasks = self.store.list_tasks()
        assert len(tasks) == 2

    def test_list_tasks_ordered_by_id(self):
        """Test that list_tasks returns tasks ordered by ID."""
        self.store.add_task("Buy eggs")
        self.store.add_task("Buy milk")
        self.store.add_task("Buy bread")
        tasks = self.store.list_tasks()
        assert [t.title for t in tasks] == ["Buy eggs", "Buy milk", "Buy bread"]

    def test_get_task_exists(self):
        """Test getting an existing task."""
        task_id = self.store.add_task("Buy milk")
        task = self.store.get_task(task_id)
        assert task is not None
        assert task.title == "Buy milk"

    def test_get_task_not_exists(self):
        """Test getting a non-existent task returns None."""
        task = self.store.get_task(999)
        assert task is None

    def test_update_task_title(self):
        """Test updating a task's title."""
        task_id = self.store.add_task("Buy milk")
        result = self.store.update_task(task_id, title="Buy almond milk")
        assert result is True
        task = self.store.get_task(task_id)
        assert task.title == "Buy almond milk"

    def test_update_task_description(self):
        """Test updating a task's description."""
        task_id = self.store.add_task("Buy milk", "Original description")
        self.store.update_task(task_id, description="Updated description")
        task = self.store.get_task(task_id)
        assert task.description == "Updated description"

    def test_update_task_both_fields(self):
        """Test updating both title and description."""
        task_id = self.store.add_task("Buy milk")
        self.store.update_task(task_id, title="Buy eggs", description="Get cage-free")
        task = self.store.get_task(task_id)
        assert task.title == "Buy eggs"
        assert task.description == "Get cage-free"

    def test_update_task_not_exists(self):
        """Test updating a non-existent task returns False."""
        result = self.store.update_task(999, title="New title")
        assert result is False

    def test_update_task_completed_status_unchanged(self):
        """Test that update does not change completed status."""
        task_id = self.store.add_task("Buy milk")
        # Manually set completed to True
        task = self.store.get_task(task_id)
        task.completed = True

        self.store.update_task(task_id, title="New title")
        updated_task = self.store.get_task(task_id)
        assert updated_task.completed is True

    def test_delete_task_exists(self):
        """Test deleting an existing task."""
        task_id = self.store.add_task("Buy milk")
        result = self.store.delete_task(task_id)
        assert result is True
        assert self.store.get_task(task_id) is None

    def test_delete_task_not_exists(self):
        """Test deleting a non-existent task returns False."""
        result = self.store.delete_task(999)
        assert result is False

    def test_delete_task_removed_from_list(self):
        """Test that deleted task is not in list_tasks."""
        self.store.add_task("Buy milk")
        self.store.add_task("Buy eggs")
        self.store.delete_task(1)
        tasks = self.store.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Buy eggs"

    def test_toggle_task_pending_to_completed(self):
        """Test toggling a pending task to completed."""
        task_id = self.store.add_task("Buy milk")
        result = self.store.toggle_task(task_id)
        assert result is True
        task = self.store.get_task(task_id)
        assert task.completed is True

    def test_toggle_task_completed_to_pending(self):
        """Test toggling a completed task back to pending."""
        task_id = self.store.add_task("Buy milk")
        # Complete the task
        self.store.toggle_task(task_id)
        # Toggle back to pending
        result = self.store.toggle_task(task_id)
        assert result is True
        task = self.store.get_task(task_id)
        assert task.completed is False

    def test_toggle_task_not_exists(self):
        """Test toggling a non-existent task returns False."""
        result = self.store.toggle_task(999)
        assert result is False

    def test_id_not_reused_after_deletion(self):
        """Test that IDs are not reused after task deletion (Constitution Principle V)."""
        self.store.add_task("Task 1")
        self.store.add_task("Task 2")
        self.store.delete_task(1)
        self.store.add_task("Task 3")
        tasks = self.store.list_tasks()
        assert len(tasks) == 2
        assert [t.id for t in tasks] == [2, 3]

    def test_get_next_id_after_operations(self):
        """Test that get_next_id returns correct next ID."""
        assert self.store.get_next_id() == 1
        self.store.add_task("Task 1")
        assert self.store.get_next_id() == 2
        self.store.add_task("Task 2")
        assert self.store.get_next_id() == 3
