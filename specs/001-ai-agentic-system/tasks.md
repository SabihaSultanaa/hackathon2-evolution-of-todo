# Tasks: AI-Powered Agentic Task Management

**Input**: Design documents from `/specs/001-ai-agentic-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Triple-server architecture**: `backend/`, `mcp-server/`, `ai-agent/`, `frontend/`
- **Backend**: `backend/app/` - Existing FastAPI, minimal modifications
- **MCP Server**: `mcp-server/` - New Phase III module
- **AI Agent**: `ai-agent/` - New Phase III module
- **Frontend**: `frontend/src/` - Existing Next.js, add ChatWidget

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create mcp-server/ directory structure
- [ ] T002 Create ai-agent/ directory structure
- [ ] T003 [P] Create mcp-server/main.py entry point
- [ ] T004 [P] Create mcp-server/tools/__init__.py
- [ ] T005 [P] Create mcp-server/auth/__init__.py
- [ ] T006 [P] Create mcp-server/client/__init__.py
- [ ] T007 [P] Create ai-agent/assistant.py entry point
- [ ] T008 [P] Create ai-agent/prompts/__init__.py
- [ ] T009 [P] Create ai-agent/intents/__init__.py
- [ ] T010 [P] Create mcp-server/.env with BACKEND_URL configuration
- [ ] T011 [P] Create ai-agent/.env with OPENAI_API_KEY configuration
- [ ] T012 Create frontend/src/components/chat/ directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T013 [P] Create token validation endpoint in backend/app/api/v1/tasks.py (POST /validate-token)
- [ ] T014 [P] Create backend HTTP client in mcp-server/client/backend.py
- [ ] T015 [P] Create token validation middleware in mcp-server/auth/validator.py
- [ ] T016 [P] Create list_tasks tool stub in mcp-server/tools/list_tasks.py
- [ ] T017 [P] Create create_task tool stub in mcp-server/tools/create_task.py
- [ ] T018 [P] Create toggle_status tool stub in mcp-server/tools/toggle_status.py
- [ ] T019 [P] Create remove_task tool stub in mcp-server/tools/remove_task.py
- [ ] T020 [P] Create system prompt in ai-agent/prompts/system.py
- [ ] T021 [P] Create intent parser in ai-agent/intents/parser.py
- [ ] T022 [P] Create entity extractor in ai-agent/intents/extractor.py
- [ ] T023 [P] Create ChatWidget component in frontend/src/components/chat/ChatWidget.tsx
- [ ] T024 [P] Create MessageList component in frontend/src/components/chat/MessageList.tsx
- [ ] T025 [P] Create UserMessage component in frontend/src/components/chat/UserMessage.tsx
- [ ] T026 [P] Create AssistantMessage component in frontend/src/components/chat/AssistantMessage.tsx
- [ ] T027 [P] Create ChatInput component in frontend/src/components/chat/ChatInput.tsx
- [ ] T028 Update frontend/src/app/dashboard/page.tsx to integrate ChatWidget (add onRefreshEvent handler)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Natural Language Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks through natural language without using forms

**Independent Test**: User types "I need to finish quarterly report" in chat and task is created with correct title/category

### Implementation for User Story 1

- [ ] T029 [P] [US1] Implement list_tasks tool logic in mcp-server/tools/list_tasks.py (call backend GET /api/v1/tasks)
- [ ] T030 [P] [US1] Implement create_task tool logic in mcp-server/tools/create_task.py (call backend POST /api/v1/tasks)
- [ ] T031 [P] [US1] Add session token validation to list_tasks tool (call backend /validate-token before API call)
- [ ] T032 [P] [US1] Add session token validation to create_task tool (call backend /validate-token before API call)
- [ ] T033 [US1] Implement CREATE intent pattern in ai-agent/intents/parser.py (match "add", "create", "need to", "should do")
- [ ] T034 [P] [US1] Implement title extraction in ai-agent/intents/extractor.py (extract task title from natural language)
- [ ] T035 [P] [US1] Implement category extraction in ai-agent/intents/extractor.py (infer category from context or default to "General")
- [ ] T036 [P] [US1] Implement description extraction in ai-agent/intents/extractor.py (extract details from user input)
- [ ] T037 [US1] Connect AI agent to MCP create_task tool in ai-agent/assistant.py
- [ ] T038 [US1] Implement chat message history state in frontend/src/components/chat/ChatWidget.tsx
- [ ] T039 [P] [US1] Implement user message submission in frontend/src/components/chat/ChatInput.tsx
- [ ] T040 [P] [US1] Implement AI response display in frontend/src/components/chat/AssistantMessage.tsx
- [ ] T041 [P] [US1] Implement session token integration in frontend/src/components/chat/ChatWidget.tsx (receive from auth context)
- [ ] T042 [P] [US1] Implement message history rendering in frontend/src/components/chat/MessageList.tsx
- [ ] T043 [US1] Connect ChatWidget to AI agent in frontend/src/components/chat/ChatWidget.tsx
- [ ] T044 [US1] Emit refresh-event after successful create_task in frontend/src/components/chat/ChatWidget.tsx
- [ ] T045 [US1] Update frontend/src/app/dashboard/page.tsx to listen for refresh-event and refetch tasks
- [ ] T046 [US1] Add confirmation message display in frontend/src/components/chat/AssistantMessage.tsx

**Checkpoint**: At this point, User Story 1 should be fully functional - user can say "I need to finish quarterly report" and task is created with confirmation

---

## Phase 4: User Story 2 - Conversational Task Status Updates (Priority: P1)

**Goal**: Users can toggle task completion status through natural language

**Independent Test**: User types "I'm done with reviewing code" and task status updates to Done

### Implementation for User Story 2

- [ ] T047 [P] [US2] Implement toggle_status tool logic in mcp-server/tools/toggle_status.py (call backend PATCH /api/v1/tasks/{id}/toggle)
- [ ] T048 [P] [US2] Add session token validation to toggle_status tool (call backend /validate-token before API call)
- [ ] T049 [US2] Implement TOGGLE intent pattern in ai-agent/intents/parser.py (match "done with", "finished", "complete", "mark done")
- [ ] T050 [P] [US2] Implement task reference extraction in ai-agent/intents/extractor.py (extract task ID or title from user input)
- [ ] T051 [P] [US2] Implement task disambiguation in ai-agent/intents/extractor.py (handle multiple matching tasks)
- [ ] T052 [US2] Connect AI agent to MCP toggle_status tool in ai-agent/assistant.py
- [ ] T053 [P] [US2] Add clarification question generation in ai-agent/prompts/system.py (for ambiguous task references)
- [ ] T054 [US2] Emit refresh-event after successful toggle_status in frontend/src/components/chat/ChatWidget.tsx
- [ ] T055 [US2] Add status update confirmation message in frontend/src/components/chat/AssistantMessage.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently - user can create tasks and toggle completion

---

## Phase 5: User Story 3 - Natural Language Task Inquiry (Priority: P2)

**Goal**: Users can ask about their tasks and receive relevant lists

**Independent Test**: User types "What tasks do I have?" and system displays all their tasks

### Implementation for User Story 3

- [ ] T056 [P] [US3] Complete list_tasks tool implementation in mcp-server/tools/list_tasks.py (add category filtering support)
- [ ] T057 [P] [US3] Add session token validation to list_tasks tool (call backend /validate-token before API call)
- [ ] T058 [US3] Implement INQUIRY intent pattern in ai-agent/intents/parser.py (match "what", "show", "list", "display")
- [ ] T059 [P] [US3] Implement category filter extraction in ai-agent/intents/extractor.py (parse "work tasks", "personal tasks", etc.)
- [ ] T060 [P] [US3] Implement prioritization logic in ai-agent/intents/extractor.py (order tasks for "what should I focus on")
- [ ] T061 [US3] Connect AI agent to MCP list_tasks tool in ai-agent/assistant.py
- [ ] T062 [P] [US3] Add task list display in frontend/src/components/chat/AssistantMessage.tsx (format tasks as readable text)
- [ ] T063 [US3] Add category highlighting in task list display (bold category names)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Conversational Task Deletion (Priority: P3)

**Goal**: Users can delete tasks through natural language

**Independent Test**: User types "Remove grocery list task" and task is deleted with confirmation

### Implementation for User Story 4

- [ ] T064 [P] [US4] Implement remove_task tool logic in mcp-server/tools/remove_task.py (call backend DELETE /api/v1/tasks/{id})
- [ ] T065 [P] [US4] Add session token validation to remove_task tool (call backend /validate-token before API call)
- [ ] T066 [US4] Implement DELETE intent pattern in ai-agent/intents/parser.py (match "remove", "delete", "get rid of", "don't need")
- [ ] T067 [P] [US4] Enhance task reference extraction for deletion in ai-agent/intents/extractor.py
- [ ] T068 [US4] Add deletion confirmation prompt in ai-agent/prompts/system.py (verify before deleting ambiguous matches)
- [ ] T069 [US4] Connect AI agent to MCP remove_task tool in ai-agent/assistant.py
- [ ] T070 [US4] Emit refresh-event after successful remove_task in frontend/src/components/chat/ChatWidget.tsx
- [ ] T071 [US4] Add deletion confirmation message in frontend/src/components/chat/AssistantMessage.tsx

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T072 [P] Add error handling for invalid/expired session tokens in mcp-server/auth/validator.py
- [ ] T073 [P] Add error handling for task not found in all MCP tools in mcp-server/tools/
- [ ] T074 [P] Implement rate limiting per session token in mcp-server/main.py
- [ ] T075 [P] Add retry logic with exponential backoff for backend API calls in mcp-server/client/backend.py
- [ ] T076 [P] Implement debouncing for refresh-event in frontend/src/components/chat/ChatWidget.tsx (100ms debounce)
- [ ] T077 [P] Add loading state indicators in frontend/src/components/chat/ChatWidget.tsx (show spinner during AI processing)
- [ ] T078 [P] Add error message display in frontend/src/components/chat/AssistantMessage.tsx (user-friendly error messages)
- [ ] T079 [P] Add keyboard navigation support in frontend/src/components/chat/ChatInput.tsx (Enter to send, Shift+Enter for newline)
- [ ] T080 [P] Implement CSS filters for completed task content in frontend/src/components/tasks/TaskList.tsx (blur title/description)
- [ ] T081 [P] Ensure status badges exclude blur filters in frontend/src/components/tasks/TaskList.tsx (Constitution Principle X - Badge Integrity)
- [ ] T082 [P] Add high-contrast text styles in frontend/src/components/chat/ChatWidget.tsx (WCAG AA compliant)
- [ ] T083 [P] Add accessibility attributes to chat components (aria-labels, roles, live regions)
- [ ] T084 [P] Update system prompt in ai-agent/prompts/system.py with productivity expert persona
- [ ] T085 [P] Add conversation history management in frontend/src/components/chat/ChatWidget.tsx (limit to 100 messages)
- [ ] T086 [P] Add message timestamp display in frontend/src/components/chat/MessageList.tsx
- [ ] T087 [P] Add auto-scroll to latest message in frontend/src/components/chat/MessageList.tsx
- [ ] T088 [P] Add responsive styling for ChatWidget in frontend/src/components/chat/ChatWidget.tsx (mobile-friendly)
- [ ] T089 [P] Test constitution compliance for Badge Integrity (verify badges remain 100% sharp and visible)
- [ ] T090 Performance test natural language processing (target < 2 seconds)
- [ ] T091 Performance test task status updates (target < 3 seconds)
- [ ] T092 Performance test UI synchronization (target < 1 second after write operations)
- [ ] T093 [P] Add unit tests for MCP tools in mcp-server/tests/
- [ ] T094 [P] Add integration tests for AI agent in ai-agent/tests/
- [ ] T095 [P] Add component tests for ChatWidget in frontend/src/components/chat/__tests__/
- [ ] T096 Update quickstart.md with any setup changes discovered during implementation
- [ ] T097 Constitution compliance audit (verify Principles VII-X are satisfied)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

### Within Each User Story

- Token validation (backend/MCP) before any tool implementation
- Tool logic before AI agent integration
- AI agent integration before frontend chat widget
- Frontend chat widget before dashboard integration
- All components functional before cross-cutting polish

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tool implementations for each story marked [P] can run in parallel
- All AI agent intent parsing marked [P] can run in parallel
- All frontend message components marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1 (Natural Language Task Creation)

```bash
# Launch all tool implementations together:
Task: "Implement list_tasks tool logic in mcp-server/tools/list_tasks.py"
Task: "Implement create_task tool logic in mcp-server/tools/create_task.py"
Task: "Add session token validation to list_tasks tool"
Task: "Add session token validation to create_task tool"

# Launch all AI agent intent/extraction tasks together:
Task: "Implement CREATE intent pattern in ai-agent/intents/parser.py"
Task: "Implement title extraction in ai-agent/intents/extractor.py"
Task: "Implement category extraction in ai-agent/intents/extractor.py"
Task: "Implement description extraction in ai-agent/intents/extractor.py"

# Launch all frontend message components together:
Task: "Implement user message submission in frontend/src/components/chat/ChatInput.tsx"
Task: "Implement AI response display in frontend/src/components/chat/AssistantMessage.tsx"
Task: "Implement message history rendering in frontend/src/components/chat/MessageList.tsx"
Task: "Implement session token integration in frontend/src/components/chat/ChatWidget.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Natural Language Task Creation)
4. **STOP and VALIDATE**:
   - User can say "I need to finish quarterly report"
   - Task created with correct title/category
   - Confirmation message displayed
   - Task list updates automatically
   - Status badge remains sharp (Constitution Principle X)
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (P1) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (P1) → Test independently → Deploy/Demo
4. Add User Story 3 (P2) → Test independently → Deploy/Demo
5. Add User Story 4 (P3) → Test independently → Deploy/Demo
6. Add Polish (Phase 7) → Cross-cutting improvements

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (MCP tools + AI agent + frontend chat)
   - Developer B: User Story 2 (MCP tools + AI agent + frontend chat)
   - Developer C: User Story 3 (MCP tools + AI agent + frontend chat)
3. Stories complete and integrate independently
4. Team collaborates on Polish phase (Phase 7)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Constitution Principle X (Badge Integrity) requires special CSS attention in frontend
- All MCP tools MUST validate session_token before database operations
- Event system uses 100ms debounce to prevent race conditions
- AI agent is stateless (Constitution Principle IX) - conversation history in frontend only
- No modifications to existing /backend logic except token validation endpoint
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
