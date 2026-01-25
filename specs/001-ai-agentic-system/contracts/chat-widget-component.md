# Frontend Contract: Chat Widget Component

**Date**: 2026-01-06

---

## Component Overview

**Name**: ChatWidget
**Type**: React Component
**Location**: `/src/components/chat/ChatWidget.tsx`
**Purpose**: Floating chat interface for natural language task management

---

## Props Interface

```typescript
interface ChatWidgetProps {
  sessionToken: string;  // JWT token from auth context
  onRefreshEvent?: (event: RefreshEvent) => void;  // Callback for dashboard updates
  isOpen?: boolean;  // Controlled open/close state
  onToggle?: () => void;  // Toggle handler (optional for uncontrolled mode)
  className?: string;  // Additional CSS classes
}
```

---

## Component Structure

```
ChatWidget (Floating Container)
├── ChatHeader
│   ├── Title: "AI Task Assistant"
│   └── Close Button
├── MessageList
│   └── Message[] (Scrollable)
│       ├── UserMessage
│       └── AssistantMessage
│           └── ToolResult (Optional)
└── ChatInput
    ├── TextArea (Auto-resize)
    └── Send Button
```

---

## State Management

```typescript
interface ChatWidgetState {
  messages: ConversationMessage[];  // Full conversation history
  isLoading: boolean;  // AI processing state
  isOpen: boolean;  // Widget visibility
  inputText: string;  // Current draft input
}
```

---

## Message Structure

```typescript
interface ConversationMessage {
  id: string;  // UUID or timestamp-based
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  toolCalls?: ToolCall[];  // For assistant messages
  toolResults?: ToolResult[];  // After tool execution
}
```

---

## Events

### Emitted Events

#### refresh-event
Emitted after any write operation (create, update, delete).

**Event Payload**:
```typescript
interface RefreshEvent {
  event_type: 'refresh-event';
  operation_type: 'create' | 'update' | 'delete';
  task_id?: number;  // Present if applicable
  timestamp: Date;
}
```

**When Emitted**:
- After successful `create_task` tool execution
- After successful `toggle_status` tool execution
- After successful `remove_task` tool execution

**Event Flow**:
1. Chat widget receives tool result indicating success
2. Chat widget emits `refresh-event` via `onRefreshEvent` prop
3. Dashboard receives event and triggers task list refetch
4. Task list updates and re-renders

---

### Received Events

None - ChatWidget does not listen for external events.

---

## Lifecycle

1. **Mount**
   - Initialize empty message array
   - Set isOpen from prop or default false
   - Optional: Display welcome message from assistant

2. **User Sends Message**
   - Add user message to state
   - Set isLoading to true
   - Send message + conversation history to AI agent
   - Wait for AI response

3. **AI Responds**
   - Parse assistant message
   - Identify tool calls (if any)
   - Execute tool calls via MCP server
   - Display tool results inline
   - Add assistant message with tool calls/results to state
   - Set isLoading to false

4. **Write Operation Success**
   - Emit `refresh-event` to parent
   - Update assistant message with confirmation

5. **Unmount**
   - Clear any pending timeouts
   - Release event listeners

---

## Integration Points

### Authentication Context

```typescript
import { useAuth } from '@/lib/auth-context';

function DashboardPage() {
  const { sessionToken } = useAuth();

  return (
    <ChatWidget
      sessionToken={sessionToken}
      onRefreshEvent={handleRefreshEvent}
    />
  );
}
```

### Dashboard

```typescript
function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const { sessionToken } = useAuth();

  const handleRefreshEvent = (event: RefreshEvent) => {
    // Fetch updated task list
    fetchTasks().then(setTasks);
  };

  const handleChatToggle = () => {
    // Optional: Track analytics or trigger side effects
  };

  return (
    <div>
      <TaskList tasks={tasks} />
      <ChatWidget
        sessionToken={sessionToken}
        onRefreshEvent={handleRefreshEvent}
        onToggle={handleChatToggle}
      />
    </div>
  );
}
```

---

## Styling Requirements

### Floating Widget

```css
.chat-widget {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 400px;
  max-height: 600px;
  display: flex;
  flex-direction: column;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  background: var(--background-primary);
  z-index: 1000;
}
```

### Message List

```css
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.user-message {
  align-self: flex-end;
  background: var(--primary-color);
  color: white;
  border-radius: 12px 12px 0 12px;
  padding: 0.75rem 1rem;
  max-width: 80%;
}

.assistant-message {
  align-self: flex-start;
  background: var(--background-secondary);
  border-radius: 12px 12px 12px 0;
  padding: 0.75rem 1rem;
  max-width: 80%;
}
```

### Tool Results

```css
.tool-result {
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: var(--background-tertiary);
  border-radius: 6px;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.tool-result.success {
  border-left: 3px solid var(--success-color);
}

.tool-result.error {
  border-left: 3px solid var(--error-color);
}
```

---

## Accessibility Requirements

### Keyboard Navigation
- Tab navigation through widget (header, message list, input, send button)
- Enter key submits message in input field
- Shift+Enter for new line in input field
- Escape key closes widget (if closable)

### Screen Reader Support
- `aria-label` on ChatWidget: "AI Task Assistant Chat"
- `role="log"` on message list for reading conversation history
- `aria-live="polite"` on new messages
- `aria-label` on send button: "Send message"

### High Contrast
- All text must meet WCAG AA contrast ratio (4.5:1)
- Input and buttons must have visible focus states
- Tool result status indicators use icons + text

---

## Performance Requirements

### Message Rendering
- Display up to 100 messages efficiently
- Virtualize message list if > 50 messages (future optimization)
- Debounce scroll events for performance

### Event Emission
- Emit `refresh-event` with 100ms debounce
- Batch rapid updates into single event

### Memory Management
- Limit conversation history to last 100 messages
- Clear old messages when limit reached (LRU)

---

## Error Handling

### Connection Errors
```typescript
interface ErrorMessage {
  type: 'connection_error' | 'auth_error' | 'api_error';
  message: string;
  retryable: boolean;
}
```

**Display**: Error message in chat bubble with retry button if retryable

### Authentication Errors
- Display "Session expired. Please refresh the page."
- Disable input until token refreshed

### Network Errors
- Display "Connection lost. Retrying..."
- Automatic retry with exponential backoff (3 attempts)
- Manual retry button after failed attempts

---

## Testing Requirements

### Unit Tests
- Component renders correctly with props
- Message list displays messages in order
- User message input handling
- Event emission on write operations

### Integration Tests
- Integration with auth context (session token)
- Event emission and dashboard refresh
- Message submission to AI agent

### E2E Tests
- User creates task via chat
- User toggles task status via chat
- User deletes task via chat
- Refresh event triggers task list update

---

## Constitution Compliance

### Badge Integrity (Principle X)

While the ChatWidget itself doesn't render badges, the `refresh-event` it emits must ensure that:
- Task list updates preserve badge visibility
- Dashboard applies selective CSS filters (content blurred, badges sharp)
- Status badges maintain 100% contrast

**Verification**: Task list component must implement CSS selectors that exclude badges from blur effects.

### High Contrast (FR-009)

Chat widget text must maintain high contrast:
- Background: `var(--background-primary)` vs text: `var(--text-primary)`
- Tool result backgrounds: `var(--background-tertiary)` vs text: `var(--text-secondary)`
- Error messages: Error color backgrounds must pass contrast check

---

## Future Enhancements (Out of Scope for Phase III)

- Conversation persistence (save to database)
- Voice input support
- Rich task display (with priority, due date)
- Multi-task operations (batch create, bulk toggle)
- File attachment support for task descriptions
- Analytics on user interactions
- Custom AI personality selection
- Task suggestion prompts
