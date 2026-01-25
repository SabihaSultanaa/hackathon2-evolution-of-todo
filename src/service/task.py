"""Task entity model for the todo application."""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a todo task."""

    title: str
    description: str = ""
    completed: bool = False
    id: int = 0  # Set by TaskStore

    def __post_init__(self):
        """Validate task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        self.title = self.title.strip()
        self.description = self.description.strip()
