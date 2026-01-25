# Feature Specification: Task Management Core (Phase I)

**Feature Branch**: `task-management-core`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description: "Feature Specification: Task Management Core (Phase I)...

## 1. Overview

This feature implements the foundational "Evolution of Todo" application. It provides
a command-line interface for managing a list of tasks in-memory.

## 2. User Scenarios & Testing

### User Story 1 - Add Task (Priority: P1)

As a user, I want to create a new task with a title and optional description so that
I can track things I need to do.

**Why this priority**: Core functionality required for any todo application.

**Independent Test**: Can be tested by adding a task and verifying it appears in the list.

**Acceptance Scenarios**:

1. **Given** no tasks exist, **When** user adds a task with title "Buy milk", **Then** task with ID 1 and title "Buy milk" is created with completed=False.
2. **Given** tasks exist, **When** user adds a task "Buy eggs", **Then** new task with auto-incremented ID is created.
3. **Given** a task is added, **When** user lists tasks, **Then** the new task appears in the output.

---

### User Story 2 - List Tasks (Priority: P1)

As a user, I want to see all my tasks with their status so that I can review what needs to be done.

**Why this priority**: Essential for understanding current state of todo list.

**Independent Test**: Can be tested by adding tasks and verifying the list output shows all tasks correctly.

**Acceptance Scenarios**:

1. **Given** no tasks exist, **When** user lists tasks, **Then** empty list message is displayed.
2. **Given** multiple tasks exist (some completed, some pending), **When** user lists tasks, **Then** all tasks are displayed with ID, title, description, and completion status.
3. **Given** tasks exist, **When** user lists tasks, **Then** clear formatting shows completed vs pending tasks.

---

### User Story 3 - Update Task (Priority: P1)

As a user, I want to modify an existing task's title or description so that I can correct or refine my tasks.

**Why this priority**: Core functionality for task maintenance.

**Independent Test**: Can be tested by updating a task and verifying the changes persist.

**Acceptance Scenarios**:

1. **Given** task with ID 1 exists with title "Buy milk", **When** user updates task 1 title to "Buy almond milk", **Then** task 1 title is updated.
2. **Given** task with ID 1 exists, **When** user updates task 1 with new description, **Then** task 1 description is updated.
3. **Given** no task with ID 99 exists, **When** user updates task 99, **Then** error message "Task 99 not found" is displayed.
4. **Given** task exists, **When** user updates task, **Then** completed status remains unchanged.

---

### User Story 4 - Delete Task (Priority: P1)

As a user, I want to remove a task from my list so that I can keep my todo list focused.

**Why this priority**: Core functionality for task cleanup.

**Independent Test**: Can be tested by deleting a task and verifying it's removed from the list.

**Acceptance Scenarios**:

1. **Given** task with ID 1 exists, **When** user deletes task 1, **Then** task 1 is removed from the system.
2. **Given** task with ID 1 is deleted, **When** user lists tasks, **Then** task 1 does not appear.
3. **Given** no task with ID 99 exists, **When** user deletes task 99, **Then** error message "Task 99 not found" is displayed.

---

### User Story 5 - Toggle Completion (Priority: P1)

As a user, I want to mark a task as complete or incomplete so that I can track my progress.

**Why this priority**: Core functionality for workflow management.

**Independent Test**: Can be tested by toggling a task's status and verifying the change.

**Acceptance Scenarios**:

1. **Given** task with ID 1 is pending, **When** user toggles task 1, **Then** task 1 completed status becomes True.
2. **Given** task with ID 1 is completed, **When** user toggles task 1, **Then** task 1 completed status becomes False.
3. **Given** no task with ID 99 exists, **When** user toggles task 99, **Then** error message "Task 99 not found" is displayed.

---

### Edge Cases

- What happens when updating a task with empty title? -> Reject with validation error.
- How does system handle rapid successive operations? -> All operations complete in order.
- What happens after deleting task ID 1 and adding new task? -> New task gets ID 2 (auto-increment continues).

## 3. Functional Requirements

- **FR-001**: System MUST allow user to create a task with a title and description.
- **FR-002**: System MUST assign unique auto-incrementing integer IDs to each task.
- **FR-003**: System MUST display all tasks with ID, title, description, and completion status.
- **FR-004**: System MUST allow user to modify task title and/or description by ID.
- **FR-005**: System MUST allow user to remove a task by ID.
- **FR-006**: System MUST toggle task completion status between True and False by ID.
- **FR-007**: System MUST display error when attempting operations on non-existent task ID.
- **FR-008**: System MUST persist tasks in memory for the application session duration.

## 4. Key Entities

- **Task**: Represents a todo item
  - `id`: Unique auto-incrementing integer
  - `title`: String (required, non-empty)
  - `description`: String (optional, defaults to empty string)
  - `completed`: Boolean (defaults to False)

## 5. Success Criteria

- **SC-001**: Users can add tasks via CLI and see them in the list.
- **SC-002**: Tasks persist in memory throughout the session.
- **SC-003**: All 5 operations (add, list, update, delete, toggle) work correctly.
- **SC-004**: Clear error messages display for invalid operations.
- **SC-005**: Application starts via `uv run src/main.py`.
