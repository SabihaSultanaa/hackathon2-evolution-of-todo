# Tasks: Phase 2 Full-Stack Todo Web Migration

**Input**: Design documents from `/specs/005-fullstack-todo-migration/`
**Prerequisites**: plan.md, spec.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [T001] [P] Create monorepo structure with `frontend/` and `backend/` directories
- [T002] [P] Initialize Python 3.13 FastAPI project in `backend/` with pyproject.toml
- [T003] [P] Initialize Next.js 15+ project in `frontend/` with TypeScript
- [T004] [P] Configure Tailwind CSS in frontend
- [T005] [P] Configure backend dependencies: fastapi, sqlmodel, alembic, uvicorn
- [T006] [x] Configure frontend dependencies: shadcn-ui, lucide-react, next-themes (T006 completed: Next.js 16.1.1 initialized with shadcn-ui components installed)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

### Database Setup

- [T007] [x] Configure SQLModel with Neon PostgreSQL connection in `backend/app/database.py` (existing)
- [T008] [x] Create User model in `backend/app/models/user.py` (existing)
- [T009] [x] Create Task model in `backend/app/models/task.py` (existing)
- [T010] [x] Configure Alembic migrations in `backend/alembic/` (existing)
- [T011] [x] Create initial migration for User and Task tables (existing)

### Auth Framework

- [T012] [x] Install and configure Better Auth in backend (using custom JWT implementation - validated)
- [T013] [x] Create JWT token generation/validation utilities in `backend/app/auth/security.py` (existing)
- [T014] [x] Create auth dependency injection for FastAPI endpoints in `backend/app/auth/dependencies.py` (existing)
- [T015] [x] Create Better Auth configuration for frontend in `frontend/src/lib/auth-context.tsx` and API client in `frontend/src/lib/api.ts` (completed)

### API Structure

- [T016] [x] Set up FastAPI application in `backend/app/main.py` (existing)
- [T017] [x] Configure CORS middleware for cross-origin API communication (existing)
- [T018] [x] Create API router structure in `backend/app/api/v1/` (existing)
- [T019] [x] Create error handling middleware in `backend/app/exceptions.py` (existing)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Registration & Authentication (Priority: P1) MVP

**Goal**: Users can register and log in to access their todo list

**Independent Test**: Register a new user, verify login succeeds with valid credentials and fails with invalid ones

### Backend Implementation

- [T020] [US1] Create user registration endpoint in `backend/app/api/v1/auth.py` (existing)
- [T021] [US1] Implement password hashing with bcrypt in `backend/app/auth/security.py` (existing)
- [T022] [US1] Create user database operations in `backend/app/api/v1/auth.py` (existing)
- [T023] [US1] Create login endpoint returning JWT token in `backend/app/api/v1/auth.py` (existing)
- [T024] [US1] Add input validation for email/password in registration/login (existing)

### Frontend Implementation

- [T025] [US1] Create auth pages: login and register in `frontend/src/app/(auth)/` (completed)
- [T026] [US1] Implement auth form components in `frontend/src/components/auth/auth-form.tsx` (completed)
- [T027] [US1] Create auth API client in `frontend/src/lib/api.ts` (completed)
- [T028] [US1] Integrate Better Auth client in `frontend/src/lib/auth-context.tsx` (completed - using custom JWT)
- [T029] [US1] Add auth state management with React Context in `frontend/src/lib/auth-context.tsx` (completed)

**Checkpoint**: User Story 1 complete - users can register and authenticate ✓

---

## Phase 4: User Story 2 - Task Creation (Priority: P1) MVP

**Goal**: Authenticated users can create tasks with title and optional description

**Independent Test**: Create a task and verify it appears in the user's task list

### Backend Implementation

- [T030] [US2] Create task creation endpoint in `backend/app/api/v1/tasks.py` (existing)
- [T031] [US2] Implement task service in `backend/app/api/v1/tasks.py` (existing)
- [T032] [US2] Add input validation for task title (required, max 500 chars) (existing)
- [T033] [US2] Add input validation for task description (optional, max 5000 chars) (existing)

### Frontend Implementation

- [T034] [US2] Create task input component in `frontend/src/components/tasks/task-input.tsx` (completed)
- [T035] [US2] Create task list component in `frontend/src/components/tasks/task-list.tsx` (completed)
- [T036] [US2] Connect task creation and list to API with loading state in `frontend/src/components/tasks/` (completed)

**Checkpoint**: User Story 2 complete - users can create and view tasks ✓

---

## Phase 5: User Story 3 - Task List Viewing (Priority: P1) MVP

**Goal**: Authenticated users can view all their tasks

**Independent Test**: View task list and verify only authenticated user's tasks are shown

### Backend Implementation

- [T037] [US3] Create task list endpoint in `backend/app/api/v1/tasks.py` (existing)
- [T038] [US3] Implement user-scoped query in `backend/app/api/v1/tasks.py` (existing)
- [T039] [US3] Add empty state response handling (existing)

### Frontend Implementation

- [T040] [US3] Create task list component in `frontend/src/components/tasks/task-list.tsx` (completed)
- [T041] [US3] Create task item component in `frontend/src/components/tasks/task-list.tsx` (completed - inline)
- [T042] [US3] Create empty state component in `frontend/src/components/tasks/task-list.tsx` (completed - inline)
- [T043] [US3] Implement task list fetching with loading state in `frontend/src/components/tasks/` (completed)
- [T044] [US3] Build dashboard page in `frontend/src/app/(dashboard)/dashboard/page.tsx` (completed)

**Checkpoint**: User Story 3 complete - users can view their tasks ✓

---

## Phase 6: User Story 4 - Task Update (Priority: P2)

**Goal**: Authenticated users can update task title and description

**Independent Test**: Update a task and verify the changes are reflected

### Backend Implementation

- [T045] [US4] Create task update endpoint (PUT) in `backend/app/api/v1/tasks.py` (existing)
- [T046] [US4] Implement ownership verification in `backend/app/api/v1/tasks.py` (existing)
- [T047] [US4] Add input validation for title and description updates (existing)

### Frontend Implementation

- [T048] [US4] Create task edit dialog in `frontend/src/components/tasks/task-edit-dialog.tsx` (completed)
- [T049] [US4] Connect edit functionality to API with loading states in `frontend/src/components/tasks/` (completed)
- [T050] [US4] Add error handling for unauthorized updates (completed)

**Checkpoint**: User Story 4 complete - users can update tasks ✓

---

## Phase 7: User Story 5 - Task Toggle (Priority: P2)

**Goal**: Authenticated users can mark tasks as complete or pending

**Independent Test**: Toggle task status and verify the change is reflected

### Backend Implementation

- [T051] [US5] Create task toggle endpoint (PATCH) in `backend/app/api/v1/tasks.py` (existing)
- [T052] [US5] Implement ownership verification for toggle operation (existing)

### Frontend Implementation

- [T053] [US5] Add checkbox component for task completion in `frontend/src/components/tasks/task-list.tsx` (completed)
- [T054] [US5] Implement toggle with loading state in `frontend/src/components/tasks/` (completed)
- [T055] [US5] Add visual feedback for completed vs pending tasks (completed)

**Checkpoint**: User Story 5 complete - users can toggle task completion ✓

---

## Phase 8: User Story 6 - Task Deletion (Priority: P2)

**Goal**: Authenticated users can permanently remove tasks

**Independent Test**: Delete a task and verify it no longer appears in the list

### Backend Implementation

- [T056] [US6] Create task deletion endpoint (DELETE) in `backend/src/api/v1/routes/tasks.py`
- [T057] [US6] Implement ownership verification for deletion
- [T058] [US6] Ensure task IDs are not reused after deletion

### Frontend Implementation

- [T059] [US6] Add delete button to task item in `frontend/src/components/tasks/task-item.tsx`
- [T060] [US6] Create delete confirmation dialog in `frontend/src/components/tasks/delete-confirm-dialog.tsx`
- [T061] [US6] Implement optimistic delete with loading state
- [T062] [US6] Add undo option before permanent deletion

**Checkpoint**: User Story 6 complete - users can delete tasks

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [T063] [x] Add light/dark mode support with next-themes in frontend (completed: ThemeToggle component + DropdownMenu)
- [T064] [x] Add error toasts/notifications for failed operations in frontend (completed: sonner toasts on all actions)
- [T065] [x] Add loading skeletons for task list in frontend (completed: TaskListSkeleton with 3 placeholder items)
- [T066] [x] Add responsive design for mobile devices in all components (completed: hidden email on mobile, sticky navbar)
- [T067] [x] Create logout functionality in frontend (completed: logout in auth-context + Navbar)
- [T068] [P] Add session timeout handling in frontend (pending - future enhancement)
- [T069] [x] API documentation with OpenAPI/Swagger (completed: /docs endpoint available)
- [T070] [P] Create integration tests for API endpoints in `backend/tests/` (pending - optional)
- [T071] [P] Create unit tests for task service in `backend/tests/` (pending - optional)

**Phase 9 Complete** - Core polish features implemented ✓

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-8)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational - No dependencies on other stories
- **US2 (P1)**: Can start after Foundational - No dependencies on other stories
- **US3 (P1)**: Can start after Foundational - No dependencies on other stories
- **US4 (P2)**: Can start after Foundational - No dependencies on other stories
- **US5 (P2)**: Can start after Foundational - No dependencies on other stories
- **US6 (P2)**: Can start after Foundational - No dependencies on other stories

### Within Each User Story

- Backend models before services
- Services before endpoints
- Core backend implementation before frontend integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel
- Once Foundational phase completes, all user stories can start in parallel
- Backend and frontend work for a story can proceed in parallel

---

## Implementation Strategy

### MVP First (User Stories 1-3 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Auth)
4. Complete Phase 4: User Story 2 (Create)
5. Complete Phase 5: User Story 3 (View)
6. **STOP and VALIDATE**: Test MVP independently
7. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 → Test independently → Deploy/Demo (Auth ready)
3. Add US2 → Test independently → Deploy/Demo (Create tasks)
4. Add US3 → Test independently → Deploy/Demo (View tasks)
5. Add US4 → Test independently → Deploy/Demo (Update tasks)
6. Add US5 → Test independently → Deploy/Demo (Toggle tasks)
7. Add US6 → Test independently → Deploy/Demo (Delete tasks)
8. Add Phase 9 polish → Final deployment

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
