"""In-memory task storage for the todo application."""

from typing import Optional

from .task import Task
from .exceptions import TaskNotFoundError


class TaskStore:
    """Manages tasks in memory with auto-incrementing IDs."""

    def __init__(self):
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str = "") -> int:
        """Create a new task with an auto-generated ID.

        Args:
            title: The task title (required, non-empty).
            description: Optional task description.

        Returns:
            The ID of the newly created task.
        """
        task = Task(
            title=title,
            description=description,
            completed=False,
            id=self._next_id,
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task.id

    def list_tasks(self) -> list[Task]:
        """Return all tasks ordered by ID.

        Returns:
            List of all tasks in the store.
        """
        return sorted(self._tasks.values(), key=lambda t: t.id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by its ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The task if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> bool:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update.
            title: New title (if provided).
            description: New description (if provided).

        Returns:
            True if task was updated, False if not found.
        """
        task = self._tasks.get(task_id)
        if task is None:
            return False

        if title is not None:
            task.title = title.strip()
        if description is not None:
            task.description = description.strip()
        return True

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if task was deleted, False if not found.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def toggle_task(self, task_id: int) -> bool:
        """Toggle a task's completion status.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            True if task was toggled, False if not found.
        """
        task = self._tasks.get(task_id)
        if task is None:
            return False
        task.completed = not task.completed
        return True

    def get_next_id(self) -> int:
        """Return the next ID that would be assigned to a new task.

        Useful for testing and debugging.
        """
        return self._next_id
