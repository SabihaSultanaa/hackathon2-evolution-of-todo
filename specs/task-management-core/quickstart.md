# Quickstart: Todo CLI

## Prerequisites

- Python 3.13+
- `uv` package manager

## Installation

```bash
# Install dependencies (if any added in future)
uv sync
```

## Running the Application

```bash
uv run src/main.py --help
```

## Usage

### Add a Task

```bash
uv run src/main.py add --title "Buy milk" --description "Get 2% milk from store"
```

### List All Tasks

```bash
uv run src/main.py list
```

Output example:
```
ID | Title          | Description       | Status
1  | Buy milk       | Get 2% milk...    | Pending
2  | Call dentist   |                   | Completed
```

### Update a Task

```bash
uv run src/main.py update --id 1 --title "Buy almond milk"
```

### Toggle Completion

```bash
uv run src/main.py toggle --id 1
```

### Delete a Task

```bash
uv run src/main.py delete --id 1
```

## Error Handling

If you attempt an operation on a non-existent ID:
```
Error: Task 99 not found
```

## Session Behavior

- Tasks persist in memory for the duration of your session
- Closing and reopening the application resets the task list (Phase I)
