---

description: "Task list template for feature implementation"
---

# Tasks: Task Management Core (Phase I)

**Input**: Design documents from `/specs/task-management-core/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md (required)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single project: `src/`, `tests/` at repository root
- Paths shown below assume single project structure per plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in src/
- [ ] T002 Create tests/ directory with unit/ and integration/ subdirectories
- [ ] T003 Create pyproject.toml with Python 3.13+ and pytest dependency
- [ ] T004 [P] Create src/__init__.py (empty marker file)
- [ ] T005 [P] Create src/cli/__init__.py (empty marker file)
- [ ] T006 [P] Create src/service/__init__.py (empty marker file)
- [ ] T007 [P] Create tests/__init__.py (empty marker file)
- [ ] T008 [P] Create tests/unit/__init__.py (empty marker file)
- [ ] T009 [P] Create tests/integration/__init__.py (empty marker file)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 Create Task dataclass in src/service/task.py
- [ ] T011 [P] Create TaskStore class in src/service/task_store.py
- [ ] T012 Create exceptions module src/service/exceptions.py with TaskNotFoundError
- [ ] T013 [P] Create src/service/__init__.py exporting Task and TaskStore
- [ ] T014 Create unit tests for Task dataclass in tests/unit/test_task.py
- [ ] T015 Create unit tests for TaskStore in tests/unit/test_task_store.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) MVP

**Goal**: User can create a task with title and optional description

**Independent Test**: Can be tested by adding a task and verifying it appears in the list

- [ ] T016 [US1] Create add command parser in src/cli/add_command.py
- [ ] T017 [US1] Implement add command handler in src/cli/add_command.py
- [ ] T018 [US1] Integrate add command into main CLI in src/main.py
- [ ] T019 [US1] Create integration test for add command in tests/integration/test_add.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - List Tasks (Priority: P1)

**Goal**: User can see all tasks with their status

**Independent Test**: Can be tested by adding tasks and verifying the list output shows all correctly

- [ ] T020 [US2] Create list command parser in src/cli/list_command.py
- [ ] T021 [US2] Implement list command handler in src/cli/list_command.py
- [ ] T022 [US2] Integrate list command into main CLI in src/main.py
- [ ] T023 [US2] Create integration test for list command in tests/integration/test_list.py

**Checkpoint**: User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task (Priority: P1)

**Goal**: User can modify task title and/or description by ID

**Independent Test**: Can be tested by updating a task and verifying changes persist

- [ ] T024 [US3] Create update command parser in src/cli/update_command.py
- [ ] T025 [US3] Implement update command handler in src/cli/update_command.py
- [ ] T026 [US3] Integrate update command into main CLI in src/main.py
- [ ] T027 [US3] Create integration test for update command in tests/integration/test_update.py

**Checkpoint**: User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Task (Priority: P1)

**Goal**: User can remove a task by ID

**Independent Test**: Can be tested by deleting a task and verifying it's removed from the list

- [ ] T028 [US4] Create delete command parser in src/cli/delete_command.py
- [ ] T029 [US4] Implement delete command handler in src/cli/delete_command.py
- [ ] T030 [US4] Integrate delete command into main CLI in src/main.py
- [ ] T031 [US4] Create integration test for delete command in tests/integration/test_delete.py

**Checkpoint**: User Stories 1-4 should all work independently

---

## Phase 7: User Story 5 - Toggle Completion (Priority: P1)

**Goal**: User can mark task as complete or incomplete

**Independent Test**: Can be tested by toggling a task's status and verifying the change

- [ ] T032 [US5] Create toggle command parser in src/cli/toggle_command.py
- [ ] T033 [US5] Implement toggle command handler in src/cli/toggle_command.py
- [ ] T034 [US5] Integrate toggle command into main CLI in src/main.py
- [ ] T035 [US5] Create integration test for toggle command in tests/integration/test_toggle.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T036 Create CLI help and usage information in src/main.py
- [ ] T037 Add error handling for non-existent task IDs in all commands
- [ ] T038 Add input validation for empty titles
- [ ] T039 Update pyproject.toml with proper project metadata
- [ ] T040 [P] Run all tests and verify SC-001 through SC-005 pass
- [ ] T041 Verify quickstart.md instructions work correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staff available)
  - Or sequentially in priority order
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (Add)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (List)**: Can start after Foundational - No dependencies on other stories
- **User Story 3 (Update)**: Can start after Foundational - No dependencies on other stories
- **User Story 4 (Delete)**: Can start after Foundational - No dependencies on other stories
- **User Story 5 (Toggle)**: Can start after Foundational - No dependencies on other stories

### Within Each User Story

- CLI parser → CLI handler → Main integration → Integration test
- Story complete before moving to next priority (for sequential execution)

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel
- All tasks for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
Task: "Create add command parser in src/cli/add_command.py"
Task: "Create unit tests for Task dataclass in tests/unit/test_task.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test Add Task independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add Phase 8: Polish → Final delivery
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Add)
   - Developer B: User Story 2 (List)
   - Developer C: User Story 3 (Update)
   - Developer D: User Story 4 (Delete)
   - Developer E: User Story 5 (Toggle)
3. Stories complete and integrate independently

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1: Setup | 9 | Project structure and initialization |
| Phase 2: Foundational | 6 | Task, TaskStore, exceptions, unit tests |
| Phase 3: US1 Add | 4 | Add command parser, handler, integration, test |
| Phase 4: US2 List | 4 | List command parser, handler, integration, test |
| Phase 5: US3 Update | 4 | Update command parser, handler, integration, test |
| Phase 6: US4 Delete | 4 | Delete command parser, handler, integration, test |
| Phase 7: US5 Toggle | 4 | Toggle command parser, handler, integration, test |
| Phase 8: Polish | 6 | Help, validation, metadata, testing |
| **Total** | **41** | All tasks |

### Parallel Opportunities

- Setup: 5 tasks marked [P] can run in parallel
- Foundational: 3 tasks marked [P] can run in parallel
- All user stories can execute in parallel after Phase 2

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests pass before moving to next story
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
