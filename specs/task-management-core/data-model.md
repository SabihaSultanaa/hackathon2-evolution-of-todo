# Data Model: Task Management Core

## Task Entity

Represents a todo item stored in memory.

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | int | Yes | Auto-generated | Unique identifier (auto-incrementing) |
| `title` | str | Yes | N/A | Task title (non-empty string) |
| `description` | str | No | "" | Optional task description |
| `completed` | bool | No | False | Completion status |

### Validation Rules

- `title`: Must be a non-empty string after stripping whitespace
- `id`: Must be a positive integer, unique across all tasks

### State Transitions

```
Pending (completed=False) <--toggle--> Completed (completed=True)
```

### Python Implementation

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    """Represents a todo task."""
    title: str
    description: str = ""
    completed: bool = False
    id: int = 0  # Set by TaskStore
```

## TaskStore Entity

In-memory storage for all tasks.

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `_tasks` | dict[int, Task] | Maps task ID to Task instance |
| `_next_id` | int | Counter for next auto-increment ID |

### Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `add_task(title, description)` | title: str, description: str | int (new task ID) | Creates task with auto-ID |
| `list_tasks()` | None | list[Task] | Returns all tasks |
| `get_task(id)` | id: int | Optional[Task] | Returns task or None |
| `update_task(id, title, description)` | id: int, title: Optional[str], description: Optional[str] | bool | Updates if exists |
| `delete_task(id)` | id: int | bool | Removes task, returns success |
| `toggle_task(id)` | id: int | bool | Toggles completed status |

### Constraints

- IDs are never reused after deletion (per Constitution Principle V)
- Auto-increment counter continues even after deletions
- Operations are atomic within the single Python process
