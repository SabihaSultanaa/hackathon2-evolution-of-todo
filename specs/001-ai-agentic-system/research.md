# Research: AI-Powered Agentic Task Management

**Date**: 2026-01-06
**Purpose**: Resolve technical unknowns and establish best practices for AI agent integration

---

## Technology Decisions

### 1. AI Engine Framework

**Decision**: OpenAI Agents SDK (Official)

**Rationale**:
- Official SDK with robust agent orchestration capabilities
- Built-in tool calling support
- Active community and comprehensive documentation
- Seamless integration with OpenAI's language models

**Alternatives Considered**:
- LangChain: More flexible but requires more boilerplate for basic agent use cases
- AutoGen: Good for multi-agent systems but overkill for single-agent scenario
- Custom implementation: Would require significant development time and maintenance

---

### 2. MCP SDK Integration

**Decision**: Official Model Context Protocol (MCP) Python SDK

**Rationale**:
- Protocol standard for AI tool integration
- Enables interoperability with AI clients and IDEs
- Built-in support for tool definitions and capabilities
- Aligns with Constitution Principle VIII (Protocol Standardization)

**Alternatives Considered**:
- Direct HTTP APIs: Would break MCP protocol requirements
- Custom WebSocket protocol: Would violate standardization requirement
- OpenAI Function Calling only: Lacks standardized tool description format

---

### 3. Authentication Pattern

**Decision**: Session Token Validation at MCP Tool Level

**Rationale**:
- Frontend manages session tokens (JWT or opaque)
- MCP server validates token against backend before any operation
- Stateless architecture (Constitution Principle IX)
- Aligns with Constitution Principle IX (Authentication Requirements)

**Authentication Flow**:
1. Frontend sends session token from auth context to MCP tools
2. MCP server validates token with backend `/api/v1/validate-token` endpoint
3. Backend returns user identity on successful validation
4. MCP tools execute operations on behalf of validated user
5. Frontend session management remains responsible for token lifecycle

**Token Requirements**:
- Must be passed in all MCP tool calls as `session_token` parameter
- Token validation must occur BEFORE any database operation
- Invalid/expired tokens must reject operation with clear error message

---

### 4. Frontend Chat Interface Architecture

**Decision**: Floating Chat Widget with Event Bus Pattern

**Rationale**:
- Non-intrusive UI that doesn't disrupt existing dashboard
- Event bus enables loose coupling between chat widget and main dashboard
- Supports real-time synchronization (Constitution FR-008)
- Enables "refresh-event" for task list updates

**Component Structure**:
- ChatWidget: Main component with message history and input
- Message List: Displays conversation history
- Message Input: Text input area for user messages
- Event Emitter: Emits events to parent dashboard

**Event Types**:
- `refresh-event`: Emitted after write operations (create, update, delete)
- Event carries operation type and task details
- Dashboard listens for event and refetches task list

---

### 5. Natural Language Understanding Strategy

**Decision**: Multi-Intent Pattern Matching with Fallback

**Rationale**:
- Simpler than full NLP pipeline for this domain
- Sufficient for task management operations
- Reduces false positives
- Allows for clear error messages when intent unclear

**Intent Categories**:
1. **CREATE**: Add, create, new task, need to, should do
2. **TOGGLE**: Done with, finished, complete, mark done, toggle
3. **INQUIRY**: Show, what, list, display, my tasks
4. **DELETE**: Remove, delete, get rid of, don't need

**Pattern Matching**:
- Regex-based initial intent classification
- Entity extraction for task references
- Context-aware disambiguation for multiple matching tasks

---

### 6. UI Synchronization Strategy

**Decision**: Event-Driven Refresh with Debouncing

**Rationale**:
- Avoids race conditions from multiple rapid updates
- Maintains UI responsiveness
- Simplifies state management
- Meets 1-second sync requirement (Success Criterion SC-004)

**Implementation**:
1. Chat widget emits `refresh-event` with 100ms debounce
2. Dashboard receives event and triggers task list refetch
3. Task list updates and re-renders
4. Chat widget receives confirmation of refresh completion

**Debounce Window**: 100ms (allows rapid batch operations while maintaining responsiveness)

---

### 7. Badge Integrity Compliance

**Decision**: Selective CSS Filter Application

**Rationale**:
- Meets Constitution Principle X (Badge Integrity)
- Allows content blurring while preserving badge visibility
- Achieves visual hierarchy without accessibility compromise

**Implementation**:
- Task container: Apply blur/opacity filters to completed task content
- Badge element: Explicitly excluded from filters via CSS selector specificity
- Use CSS child combinators: `.task-completed > .task-content { filter: blur(2px); }`
- Badge: `.task-badge { filter: none !important; opacity: 1 !important; }`

**CSS Strategy**:
```css
/* Content blurring on completed tasks */
.task-card.completed .task-content {
  filter: blur(1px);
  opacity: 0.7;
}

/* Badge explicitly unblurred */
.task-card.completed .task-badge {
  filter: none !important;
  opacity: 1 !important;
}
```

---

## Architecture Patterns

### Triple-Server Architecture

The system operates with three independent servers:

1. **Next.js Frontend Server** (Port 3000)
   - Renders React UI
   - Manages authentication session
   - Hosts chat widget component
   - Handles user interactions

2. **FastAPI Backend Server** (Port 8000)
   - Provides REST API for task CRUD operations
   - Validates session tokens
   - Manages database persistence
   - Handles business logic

3. **MCP Server** (Port 8080)
   - Exposes MCP tools for AI agent
   - Validates session tokens against backend
   - Routes tool calls to backend API
   - Returns structured responses to AI agent

**Communication Flow**:
```
User → Frontend → MCP Tools → Backend → Database
        ↓          ↑            ↑
    Session    Session      Token Validation
    Token      Token        (via API call)
```

---

## Security Considerations

### 1. Token Validation
- MCP server must validate tokens BEFORE any database operation
- Token validation endpoint on backend: `POST /api/v1/validate-token`
- Response includes user ID and permissions

### 2. User Isolation
- All task operations filtered by user_id
- MCP tools receive session token and validate ownership
- Prevents cross-user data access

### 3. Rate Limiting
- MCP server should implement rate limiting per session token
- Prevents abuse and resource exhaustion

### 4. Error Handling
- Generic error messages for authentication failures
- Detailed error messages for business logic failures
- No sensitive data in error responses

---

## Performance Targets

Based on Success Criteria:

- **Natural language processing**: < 2 seconds (allows 15s total task creation with UI overhead)
- **Task status updates**: < 3 seconds
- **UI synchronization**: < 1 second after write operation
- **Intent recognition accuracy**: 90% success rate

---

## Integration Points

### Existing Backend API (Port 8000)
- `GET /api/v1/tasks` - List tasks (with optional category filter)
- `POST /api/v1/tasks` - Create task
- `PATCH /api/v1/tasks/{id}/toggle` - Toggle completion
- `DELETE /api/v1/tasks/{id}` - Delete task
- `POST /api/v1/validate-token` - Validate session token (NEW endpoint needed)

### Frontend Components (Port 3000)
- Dashboard page: Receives refresh events
- Task list component: Updates on refresh events
- Authentication context: Provides session token to chat widget

### MCP Tools (Port 8080)
- `list_tasks`: Maps to GET /api/v1/tasks
- `create_task`: Maps to POST /api/v1/tasks
- `toggle_status`: Maps to PATCH /api/v1/tasks/{id}/toggle
- `remove_task`: Maps to DELETE /api/v1/tasks/{id}

---

## Implementation Sequence Recommendation

1. **Backend Enhancement**
   - Add token validation endpoint
   - Ensure existing task endpoints support JWT authentication

2. **MCP Server**
   - Implement server with 4 tool definitions
   - Add session token validation middleware
   - Implement tool-to-API routing

3. **AI Agent**
   - Configure OpenAI Agents SDK
   - Define system prompt as productivity expert
   - Implement intent parsing logic
   - Configure tool bindings

4. **Frontend Chat Widget**
   - Create floating widget component
   - Implement message history
   - Add session token integration
   - Implement event emission for UI sync
   - Apply badge integrity CSS

---

## Open Questions Resolved

**Q1**: Should the MCP server directly access the database?
**A**: No - MCP server must route through backend API to maintain separation of concerns and leverage existing authentication logic.

**Q2**: How should conversation context be maintained?
**A**: Frontend manages conversation history as an array of messages. Each message includes role (user/assistant) and content. Full history sent with each new user message to AI agent.

**Q3**: How to handle ambiguous task references (e.g., "mark the report task as done")?
**A**: When multiple tasks match, AI agent will ask for clarification: "I found multiple tasks with 'report' in the title. Which one would you like to mark as done?"

**Q4**: Should we store conversation history in the backend?
**A**: No - Phase III focuses on statelessness (Constitution Principle IX). Frontend manages conversation in memory. Future phases could add persistence if needed.

---

## Dependencies

### External Services
- OpenAI API (for AI model inference)
- Database (SQLite for development, configurable for production)

### Python Packages
- `openai` (Agents SDK)
- `mcp` (Official MCP SDK)
- `httpx` (Async HTTP client for backend API calls)
- `pydantic` (Data validation)

### Frontend Dependencies
- React (existing)
- Event emitter library (or use custom hook)

---

## Risks and Mitigations

### Risk 1: OpenAI API rate limits
**Mitigation**: Implement retry logic with exponential backoff. Consider caching common responses.

### Risk 2: Natural language understanding accuracy below 90%
**Mitigation**: Start with pattern matching, collect user feedback, iterate on intent recognition rules.

### Risk 3: Token validation latency
**Mitigation**: Cache validated tokens for short duration (e.g., 60 seconds) to reduce backend load.

### Risk 4: UI sync delays
**Mitigation**: Implement optimistic updates in chat widget while waiting for backend confirmation.

---

## Research Summary

All technical unknowns resolved. The architecture leverages:
- Official MCP SDK for standardization
- Session token authentication for security
- Event-driven UI synchronization for responsiveness
- Pattern matching for natural language understanding
- Selective CSS filtering for badge integrity compliance

Ready to proceed to Phase 1: Design & Contracts.
