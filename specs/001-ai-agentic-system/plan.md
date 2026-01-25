# Implementation Plan: AI-Powered Agentic Task Management

**Branch**: `001-ai-agentic-system` | **Date**: 2026-01-06 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-ai-agentic-system/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Integrate a natural language interface into the existing task management workspace, enabling users to create, update, view, and delete tasks through conversational AI. The system implements a triple-server architecture (Next.js frontend, FastAPI backend, MCP server) with an AI agent that understands natural language and executes task operations via standardized MCP tools.

---

## Technical Context

**Language/Version**: Python 3.13+ (backend/MCP/AI), TypeScript 5+ (frontend)
**Primary Dependencies**:
  - Backend: FastAPI, SQLModel, SQLite
  - MCP Server: Official MCP SDK, httpx, pydantic
  - AI Agent: OpenAI Agents SDK, openai
  - Frontend: Next.js 15+, React 19+, Radix UI

**Storage**: SQLite (development), PostgreSQL (production, configurable)
**Testing**: pytest (backend), vitest (frontend)
**Target Platform**: Web application
**Project Type**: Full-stack web application with AI integration
**Performance Goals**:
  - Natural language processing: < 2 seconds
  - Task status updates: < 3 seconds
  - UI synchronization: < 1 second after write operations
  - Intent recognition accuracy: 90%+

**Constraints**:
  - Phase III components must live in `/mcp-server` and `/ai-agent` directories
  - No modifications to existing `/backend` logic except adding API endpoints for MCP server
  - AI agent must be stateless; user identification via session_token from frontend
  - Status badges (Done/Pending) must NEVER be blurred; maintain 100% contrast
  - All MCP tools must verify user identity before database operations

**Scale/Scope**: Single-user to small-team task management (10-100 users)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Gates (Initial)

| Principle | Status | Notes |
|-----------|---------|--------|
| I. Spec-Driven Development | ✅ PASS | Feature spec created at `specs/001-ai-agentic-system/spec.md` |
| II. Separation of Concerns | ✅ PASS | Clear boundaries: Frontend (UI), Backend (API), MCP (Tools), AI Agent (Logic) |
| III. Atomic Implementation | ⚠️ WARNING | This is Phase III with 4 user stories - ensure stories implemented independently |
| IV. In-Memory Storage (Phase I) | ⚠️ WARNING | Phase III uses backend with SQLite - allowed as Phase I constraint no longer applies |
| V. Unique Task Identification | ✅ PASS | Existing backend uses auto-increment integer IDs |
| VI. Spec-First Bug Resolution | ✅ PASS | Bug resolution process defined |
| VII. Architecture Isolation | ✅ PASS | Phase III in `/mcp-server` and `/ai-agent` - no backend coupling |
| VIII. Protocol Standardization | ✅ PASS | Official MCP SDK enforced |
| IX. Statelessness | ✅ PASS | AI agent stateless; session tokens passed from frontend |
| X. Badge Integrity | ✅ PASS | FR-010 requires badge visibility; quickstart has verification step |

### Complexity Tracking

No complexity violations identified. Architecture follows constitution principles.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-agentic-system/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   ├── mcp-tools.json
│   └── chat-widget-component.md
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**Option 2: Web application (when "frontend" + "backend" detected)**

```text
backend/                    # EXISTING - Do not modify except for MCP endpoints
├── app/
│   ├── api/v1/
│   │   └── tasks.py      # EXISTING - Task CRUD endpoints
│   ├── models/
│   │   └── task.py      # EXISTING - Task entity
│   └── schemas/
│       └── task.py      # EXISTING - Task schemas
└── todo.db              # EXISTING - SQLite database

mcp-server/                # NEW - Phase III (Constitution Principle VII)
├── main.py               # MCP server entry point
├── tools/
│   ├── __init__.py
│   ├── list_tasks.py      # MCP tool: GET /tasks
│   ├── create_task.py     # MCP tool: POST /tasks
│   ├── toggle_status.py   # MCP tool: PATCH /tasks/{id}/toggle
│   └── remove_task.py    # MCP tool: DELETE /tasks/{id}
├── auth/
│   ├── __init__.py
│   └── validator.py      # Token validation middleware
├── client/
│   ├── __init__.py
│   └── backend.py        # Async HTTP client for backend API
└── .env                 # Backend URL configuration

ai-agent/                  # NEW - Phase III (Constitution Principle VII)
├── assistant.py          # OpenAI Agent main entry point
├── prompts/
│   ├── __init__.py
│   └── system.py         # System prompt as productivity expert
├── intents/
│   ├── __init__.py
│   ├── parser.py         # Intent pattern matching logic
│   └── extractor.py     # Entity extraction from user input
└── .env                 # OpenAI API key configuration

frontend/                   # EXISTING - Add ChatWidget component
├── src/
│   ├── components/
│   │   ├── chat/          # NEW - Chat widget
│   │   │   ├── ChatWidget.tsx
│   │   │   ├── MessageList.tsx
│   │   │   ├── UserMessage.tsx
│   │   │   ├── AssistantMessage.tsx
│   │   │   └── ChatInput.tsx
│   │   └── tasks/         # EXISTING - Task list
│   │       └── TaskList.tsx  # MODIFY - Add refresh event listener
│   ├── lib/
│   │   └── auth-context.tsx  # EXISTING - Provides session token
│   └── app/
│       └── dashboard/
│           └── page.tsx   # MODIFY - Add ChatWidget integration
└── package.json
```

**Structure Decision**: Triple-server architecture with clear separation:
- **Backend (Port 8000)**: Existing FastAPI service, no modification except optional token validation endpoint
- **MCP Server (Port 8080)**: New independent module exposing standardized tools
- **AI Agent**: Stateless logic layer using OpenAI Agents SDK
- **Frontend (Port 3000)**: Existing Next.js app, adds ChatWidget component

This structure satisfies Constitution Principle VII (Architecture Isolation) - Phase III components are independent with no coupling to existing codebase.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A |

No violations requiring justification.

---

## Phase 0: Research (Completed)

### Research Summary

**Output**: `research.md`

**Decisions Resolved**:
1. **AI Engine**: OpenAI Agents SDK (official SDK, built-in tool calling)
2. **MCP SDK**: Official MCP Python SDK (standardization requirement)
3. **Authentication**: Session token validation at MCP tool level (statelessness)
4. **Frontend Chat**: Floating widget with event bus pattern (loose coupling)
5. **Natural Language**: Multi-intent pattern matching with fallback (simpler than full NLP)
6. **UI Sync**: Event-driven refresh with 100ms debounce (responsive)
7. **Badge Integrity**: Selective CSS filter application (Constitution Principle X)

**Architecture Patterns Established**:
- Triple-server architecture (Next.js 3000, FastAPI 8000, MCP 8080)
- Event-driven UI synchronization
- Stateless AI agent with token-based authentication

**All NEEDS CLARIFICATION markers resolved** - ready for Phase 1.

---

## Phase 1: Design & Contracts (Completed)

### Data Model

**Output**: `data-model.md`

**New Entities Defined**:
- `ConversationMessage` (frontend in-memory): Chat message structure
- `ToolCall` (frontend in-memory): Tool invocation details
- `ToolResult` (frontend in-memory): Tool execution result
- `RefreshEvent` (frontend event): Dashboard refresh trigger

**Existing Entities Referenced**:
- `Task` (backend): No modifications needed
- `User` (backend): No modifications needed

**MCP Tool Schemas Defined**:
- `list_tasks`: GET /api/v1/tasks
- `create_task`: POST /api/v1/tasks
- `toggle_status`: PATCH /api/v1/tasks/{id}/toggle
- `remove_task`: DELETE /api/v1/tasks/{id}

**Statelessness Confirmed**: All conversation entities managed in frontend memory only.

---

### API Contracts

**Output**: `contracts/mcp-tools.json`, `contracts/chat-widget-component.md`

**MCP Tool Contract** (`mcp-tools.json`):
- 4 tools with full input/output schemas
- Authentication requirements defined
- Rate limits specified (30-60 requests/minute)
- Error codes documented

**Frontend Component Contract** (`chat-widget-component.md`):
- Props interface defined
- Component structure documented
- Event emission/reception specified
- Styling requirements outlined
- Accessibility requirements listed
- Constitution compliance verified

---

### Quickstart Guide

**Output**: `quickstart.md`

**Content**:
- Architecture diagram
- Step-by-step setup for all 3 servers
- Testing scenarios for all user stories
- Verification checklist
- Troubleshooting guide
- Performance benchmarks
- Constitution compliance verification

---

### Agent Context Update

**Action Required**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

**Status**: Not executed (shell script not available in current environment)

**Manual Update**: Add new Phase III technologies to agent context file:
- MCP SDK (`mcp` Python package)
- OpenAI Agents SDK (`openai` Python package)
- React Chat Widget component structure

---

## Post-Design Constitution Check

### Re-evaluation After Phase 1 Design

| Principle | Status | Notes |
|-----------|---------|--------|
| I. Spec-Driven Development | ✅ PASS | All artifacts spec-driven, no implementation details leaked |
| II. Separation of Concerns | ✅ PASS | Clear boundaries maintained in data model and contracts |
| III. Atomic Implementation | ✅ PASS | User stories independently testable - data model supports this |
| IV. In-Memory Storage (Phase I) | ✅ PASS | Phase I constraint doesn't apply - Phase III uses backend storage |
| V. Unique Task Identification | ✅ PASS | Data model confirms unique IDs |
| VI. Spec-First Bug Resolution | ✅ PASS | Process documented |
| VII. Architecture Isolation | ✅ PASS | `/mcp-server` and `/ai-agent` directories defined |
| VIII. Protocol Standardization | ✅ PASS | MCP tool contracts use official SDK format |
| IX. Statelessness | ✅ PASS | Data model confirms frontend-only conversation storage |
| X. Badge Integrity | ✅ PASS | Contract specifies CSS filter isolation |

**All gates passed** - ready for Phase 2 (task generation).

---

## Phase 2: Implementation (Not Started)

**Prerequisites**: Phase 1 complete (data model, contracts, quickstart)

**Task Generation**: Execute `/sp.tasks` to generate testable, dependency-ordered implementation tasks.

**Expected Output**: `tasks.md` with:
- Phase 1: Setup (infrastructure)
- Phase 2: Foundational (blocking prerequisites)
- Phase 3-N: User Stories (P1, P2, P3 in order)
- Phase N: Polish & Cross-Cutting Concerns

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Natural Language Task Creation - No dependencies on other stories
- **User Story 2 (P1)**: Conversational Task Status Updates - No dependencies on other stories
- **User Story 3 (P2)**: Natural Language Task Inquiry - No dependencies on other stories
- **User Story 4 (P3)**: Conversational Task Deletion - No dependencies on other stories

### Cross-Cutting Dependencies

- **Session Token Management**: Frontend auth context → ChatWidget → MCP tools
- **Event System**: ChatWidget (emitter) → Dashboard (listener) → TaskList (update)
- **Badge Integrity**: CSS in TaskList must exclude badges from blur filters (Constitution Principle X)

---

## Parallel Opportunities

### Setup Tasks (All [P])
- Virtual environment creation (backend/MCP/AI)
- Dependency installation (all servers)
- Environment configuration (all servers)
- Directory structure initialization

### Foundational Tasks (All [P] within Phase 2)
- Backend token validation endpoint
- MCP server initialization
- MCP tool definitions (all 4 tools in parallel)
- AI agent system prompt configuration
- Frontend ChatWidget skeleton

### User Stories (All [P] across P1, P2, P3)
- MCP tool implementations (list, create, toggle, remove)
- AI agent intent parsing (all intents in parallel)
- Frontend message components (user, assistant, input)
- Dashboard integration with chat widget

### Polish Tasks (All [P])
- Documentation updates
- Testing
- Performance optimization
- Constitution compliance verification

---

## MVP Strategy (First Delivery)

**MVP = User Story 1 Only (Natural Language Task Creation)**

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**:
   - User can say "I need to finish the quarterly report"
   - Task created with correct title/category
   - Confirmation message displayed
   - Task list updates automatically
   - Status badge remains sharp (Constitution Principle X)
5. Deploy/demo if ready

**After MVP**: Add remaining stories in priority order (P1 status toggle → P2 inquiry → P3 deletion)

---

## Incremental Delivery Strategy

1. **Setup + Foundational** → Foundation ready
2. **Add Story 1 (P1)** → Test independently → Deploy/Demo (MVP!)
3. **Add Story 2 (P1)** → Test independently → Deploy/Demo
4. **Add Story 3 (P2)** → Test independently → Deploy/Demo
5. **Add Story 4 (P3)** → Test independently → Deploy/Demo

Each story adds value without breaking previous stories.

---

## Architectural Decision Records

No ADRs required at this stage. Architecture follows constitution principles and research phase decisions.

If significant architectural decisions emerge during implementation, consider creating ADRs for:
- Token caching strategy (if implemented for performance)
- Conversation persistence (if added in future phase)
- Multi-tenant support (if scope expands)

---

## Notes

- Constitution Principle X (Badge Integrity) requires special attention in frontend CSS
- Event system must use debouncing (100ms) to prevent race conditions
- MCP server should implement rate limiting per session token
- All error messages must be user-friendly (no technical jargon)
- Session token validation must occur BEFORE any database operation

---

## Next Steps

1. **Execute `/sp.tasks`** to generate detailed implementation tasks
2. **Review tasks.md** for task ordering and dependencies
3. **Begin Phase 1 implementation** (Setup)
4. **Complete Phase 2** (Foundational) before user stories
5. **Implement User Stories** in priority order (P1 → P2 → P3)
6. **Validate Constitution compliance** after each major milestone
