"""Service layer exceptions for the todo application."""


class TaskNotFoundError(Exception):
    """Raised when a task with the given ID is not found."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found")
