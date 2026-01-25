# Data Model: AI-Powered Agentic Task Management

**Date**: 2026-01-06

---

## Overview

This data model defines the entities and data structures for the AI-powered task management system. The system leverages the existing Task entity from the backend and extends it with new entities for the AI agent functionality.

---

## Core Entities

### Task (Existing)

Represents a user's todo item.

**Attributes**:
- `id` (int, PK): Unique identifier
- `title` (string, required): Task title, max 500 characters
- `description` (string, optional): Task details, max 5000 characters, default ""
- `category` (string, optional): Task category, max 100 characters, default "General"
- `completed` (boolean, required): Completion status, default False
- `user_id` (int, FK): Reference to owning user
- `created_at` (datetime): Timestamp when task was created
- `updated_at` (datetime): Timestamp when task was last modified

**Relationships**:
- Belongs to `User` (many-to-one)

**State Transitions**:
- `Pending` (completed=False) → `Done` (completed=True)
- `Done` (completed=True) → `Pending` (completed=False)

---

### User (Existing)

Represents an authenticated user.

**Attributes**:
- `id` (int, PK): Unique identifier
- `username` (string, required): Unique username
- `email` (string, required): Unique email address
- `hashed_password` (string, required): Bcrypt hashed password
- `created_at` (datetime): Account creation timestamp

**Relationships**:
- Has many `Task` (one-to-many)

---

## New Entities

### ConversationMessage (Frontend In-Memory)

Represents a single message in the chat conversation. Managed entirely by frontend (stateless per Constitution Principle IX).

**Attributes**:
- `id` (string): Unique message identifier (UUID or timestamp-based)
- `role` (enum): Message sender - "user" or "assistant"
- `content` (string): Message text content
- `timestamp` (datetime): When message was created
- `tool_calls` (array, optional): Tool invocations triggered by this message
- `tool_results` (array, optional): Results from tool invocations

**Structure**:
```json
{
  "id": "msg_12345",
  "role": "assistant",
  "content": "I've created a new task for you: 'Finish quarterly report'",
  "timestamp": "2026-01-06T10:30:00Z",
  "tool_calls": [
    {
      "tool": "create_task",
      "arguments": {
        "title": "Finish quarterly report",
        "category": "Work"
      }
    }
  ],
  "tool_results": [
    {
      "tool": "create_task",
      "success": true,
      "data": {
        "id": 42,
        "title": "Finish quarterly report",
        "completed": false
      }
    }
  ]
}
```

**Validation Rules**:
- `role` must be "user" or "assistant"
- `content` cannot be empty
- `tool_calls` only present when `role` is "assistant"
- `tool_results` only present after tool execution

---

### ToolCall (Frontend In-Memory)

Represents a tool invocation by the AI agent.

**Attributes**:
- `tool_name` (string, required): Name of the tool being called
- `arguments` (object, required): Parameters passed to the tool
- `session_token` (string, required): User authentication token
- `timestamp` (datetime): When tool was invoked

**Available Tools**:
1. `list_tasks`: Retrieve user's tasks
2. `create_task`: Create a new task
3. `toggle_status`: Toggle task completion
4. `remove_task`: Delete a task

---

### ToolResult (Frontend In-Memory)

Represents the result of a tool invocation.

**Attributes**:
- `tool_name` (string, required): Name of the tool that was called
- `success` (boolean, required): Whether tool execution succeeded
- `data` (object, optional): Response data if successful
- `error` (string, optional): Error message if failed
- `timestamp` (datetime): When result was received

---

### RefreshEvent (Frontend Event)

Event emitted by chat widget to trigger dashboard task list refresh.

**Attributes**:
- `event_type` (string): "refresh-event"
- `operation_type` (enum): "create", "update", "delete"
- `task_id` (int, optional): ID of affected task (if applicable)
- `timestamp` (datetime): When event was emitted

**Structure**:
```json
{
  "event_type": "refresh-event",
  "operation_type": "create",
  "task_id": 42,
  "timestamp": "2026-01-06T10:30:05Z"
}
```

---

## MCP Tool Schemas

### list_tasks Tool

**Input Schema**:
```typescript
{
  "session_token": string;  // Required: JWT token for authentication
  "category_filter": string | null;  // Optional: Filter by category
}
```

**Output Schema**:
```typescript
{
  "success": boolean;
  "tasks": TaskResponse[];
  "error": string | null;  // Present if success is false
}
```

---

### create_task Tool

**Input Schema**:
```typescript
{
  "session_token": string;  // Required: JWT token for authentication
  "title": string;  // Required: Task title
  "description": string;  // Optional: Task details
  "category": string;  // Optional: Task category, default "General"
}
```

**Output Schema**:
```typescript
{
  "success": boolean;
  "task": TaskResponse | null;
  "error": string | null;  // Present if success is false
}
```

---

### toggle_status Tool

**Input Schema**:
```typescript
{
  "session_token": string;  // Required: JWT token for authentication
  "task_id": number;  // Required: ID of task to toggle
}
```

**Output Schema**:
```typescript
{
  "success": boolean;
  "task": TaskResponse | null;  // Updated task with new status
  "error": string | null;  // Present if success is false
}
```

---

### remove_task Tool

**Input Schema**:
```typescript
{
  "session_token": string;  // Required: JWT token for authentication
  "task_id": number;  // Required: ID of task to delete
}
```

**Output Schema**:
```typescript
{
  "success": boolean;
  "message": string;  // Confirmation message
  "error": string | null;  // Present if success is false
}
```

---

### Common Types

#### TaskResponse (from backend)
```typescript
{
  "id": number;
  "title": string;
  "description": string;
  "category": string;
  "completed": boolean;
  "user_id": number;
  "created_at": string;  // ISO 8601 datetime
  "updated_at": string;  // ISO 8601 datetime
}
```

---

## Data Flow

### Task Creation Flow
```
User Input → AI Agent → Intent Parsing → create_task Tool
    ↓                                    ↓
Frontend                             MCP Server
    ↓                                    ↓
Session Token Token Validation      Backend API
    ↓                                    ↓
Token Response                  POST /api/v1/tasks
    ↓                                    ↓
Success/Failure                      Task Created
    ↓                                    ↓
Refresh Event → Dashboard → Task List Updated
```

### Task Status Toggle Flow
```
User Input → AI Agent → Intent Parsing → toggle_status Tool
    ↓                                        ↓
Frontend                                 MCP Server
    ↓                                        ↓
Session Token Token Validation            Backend API
    ↓                                        ↓
Token Response                        PATCH /api/v1/tasks/{id}/toggle
    ↓                                        ↓
Success/Failure                            Task Updated
    ↓                                        ↓
Refresh Event → Dashboard → Task List Updated
```

---

## Validation Rules

### Task Entity
- `title` must be between 1-500 characters
- `description` cannot exceed 5000 characters
- `category` cannot exceed 100 characters
- `user_id` must reference an existing User

### Session Token
- Must be valid JWT token with signature verified
- Must contain user_id in "sub" claim
- Must not be expired
- User must exist in database

### MCP Tool Inputs
- `session_token` is required for all tools
- `task_id` must be positive integer and reference existing task owned by user
- `title` cannot be empty when creating task

---

## Privacy and Security

### Data Isolation
- All task operations filtered by `user_id`
- Session token validation prevents cross-user access
- MCP tools cannot access tasks outside user's ownership

### Sensitive Data
- Session tokens never logged in plain text
- Passwords never exposed to MCP layer
- User IDs used for authorization, not authentication

### Error Messages
- Generic "Invalid or expired token" for auth failures (no data leakage)
- Specific error details for business logic failures (usability)
- No internal system details in user-facing errors

---

## Indexing Considerations

### Existing Indexes (from backend)
- Primary key: `tasks.id`
- Foreign key: `tasks.user_id`
- Composite index: `(user_id, created_at)` for efficient task listing

### No New Indexes Required
Phase III does not introduce persistent storage, so no database migrations needed.

---

## Statelessness (Constitution Principle IX)

All Phase III entities related to AI conversation are **stateless**:
- Conversation history stored in frontend memory only
- No conversation persistence in backend
- Session tokens passed on each request
- MCP server maintains no user state between requests

Future phases could add conversation persistence if business requirements justify it.
