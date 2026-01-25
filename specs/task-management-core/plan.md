# Implementation Plan: Task Management Core (Phase I)

**Branch**: `task-management-core` | **Date**: 2026-01-01 | **Spec**: [spec.md](spec.md)

## Summary

This plan implements the foundational Todo CLI application with 5 core features:
Add, List, Update, Delete, and Toggle Completion. The application will use Python
3.13+ with the `uv` package manager, in-memory storage per constitution, and clear
separation between CLI (presentation) and Service (business logic) layers.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: argparse (stdlib) or click (optional), dataclasses (stdlib)
**Storage**: In-memory dictionary/list per constitution (Principle IV)
**Testing**: pytest (standard Python testing)
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single CLI application
**Performance Goals**: N/A (single-user CLI, session duration)
**Constraints**: In-memory only (no persistence), CLI-based interaction
**Scale/Scope**: Single user, session-duration persistence

## Constitution Check

*GATE: Must pass before implementation. Re-check after design.*

| Principle | Requirement | Status | Notes |
|-----------|-------------|--------|-------|
| I. SDD | Spec before code | ✅ PASS | spec.md exists |
| II. Separation of Concerns | CLI/Service layers | ✅ PASS | Designed with src/cli/ and src/service/ |
| III. Atomic Implementation | One feature at a time | ✅ PASS | Tasks organized by user story |
| IV. In-Memory Storage | No databases | ✅ PASS | Using dict for TaskStore |
| V. Unique IDs | Stable identifiers | ✅ PASS | Auto-increment with next_id counter |
| VI. Spec-First Bug Resolution | Update spec first | ✅ PASS | Documented in tasks |

## Project Structure

### Documentation (this feature)

```text
specs/task-management-core/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (N/A - no unknowns)
├── data-model.md        # Task entity definition
├── quickstart.md        # User guide
└── tasks.md             # Phase 2 output (/sp.tasks)
```

### Source Code (repository root)

```text
src/
├── main.py              # Entry point
├── cli/
│   └── __init__.py      # CLI interface layer
└── service/
    ├── __init__.py      # Business logic layer
    └── task_store.py    # In-memory task storage

tests/
├── unit/
│   └── test_task_store.py
└── integration/
    └── test_cli.py
```

**Structure Decision**: Single project with CLI and Service modules separated.
This aligns with Constitution Principle II (Separation of Concerns) while keeping
the project simple for Phase I.

## Complexity Tracking

> Not applicable - no constitution violations requiring justification.

## Phase 0: Research (Completed)

No unknowns required research. All technical choices are defined in the constitution:
- Python 3.13+ (stdlib only for Phase I)
- In-memory storage (dict-based TaskStore)
- argparse for CLI (stdlib, no additional dependencies)

## Phase 1: Design

### Data Model

See [data-model.md](data-model.md) for full entity definitions.

### Quickstart

See [quickstart.md](quickstart.md) for user instructions.

### CLI Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `add` | Add a new task | `--title` (required), `--description` (optional) |
| `list` | List all tasks | None |
| `update` | Update a task | `--id` (required), `--title`, `--description` |
| `delete` | Delete a task | `--id` (required) |
| `toggle` | Toggle completion | `--id` (required) |

## Phase 2: Tasks

See [tasks.md](tasks.md) for implementation task breakdown.
