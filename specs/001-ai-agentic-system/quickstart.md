# Quickstart Guide: AI-Powered Agentic Task Management

**Date**: 2026-01-06

---

## Overview

This guide helps you quickly set up and test the AI-powered task management system. The system consists of three independent servers working together.

---

## Architecture Diagram

```
┌─────────────────┐
│   Next.js UI    │  Port 3000
│   (Frontend)    │
│                 │
│  - Dashboard     │
│  - Chat Widget  │◄─────┐
└────────┬────────┘      │
         │                │
         │ Session Token   │
         │                │
         │                ▼
         │       ┌─────────────────┐
         │       │  MCP Server    │  Port 8080
         │       │                │
         │       │  - list_tasks  │
         │       │  - create_task │◄─────┐
         │       │  - toggle_status│       │
         │       │  - remove_task │       │
         │       └───────┬───────┘       │
         │               │                 │
         ▼               ▼                 │
┌─────────────────┐ ┌─────────────────┐   │
│  FastAPI       │ │  AI Agent      │   │
│  Backend       │ │  (OpenAI SDK)  │   │
│                │ │                │   │
│  - Task CRUD   │ │  - Intent Parse │   │
│  - Auth        │◄┼─┼─ System Prompt│   │
│  - Database    │ │  - Tool Calls   │   │
└────────┬────────┘ └─────────────────┘   │
         │                                 │
         └─────────────────────────────────┘
                      OpenAI API
```

---

## Prerequisites

- Node.js 18+ (for frontend)
- Python 3.13+ (for backend and MCP server)
- OpenAI API key with access to gpt-4 model
- SQLite (for development database)

---

## Step 1: Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your SECRET_KEY
   ```

5. **Initialize database**:
   ```bash
   uv run alembic upgrade head
   ```

6. **Start backend server**:
   ```bash
   uv run uvicorn app.main:app --reload --port 8000
   ```

**Verify**: Visit `http://localhost:8000/docs` to see API documentation

---

## Step 2: MCP Server Setup

1. **Navigate to MCP server directory**:
   ```bash
   cd mcp-server
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   uv pip install mcp httpx pydantic python-dotenv
   ```

4. **Set environment variables**:
   ```bash
   # Create .env file
   echo "BACKEND_URL=http://localhost:8000" > .env
   ```

5. **Start MCP server**:
   ```bash
   uv run python main.py
   ```

**Verify**: Server should start on port 8080 and log "MCP server listening on port 8080"

---

## Step 3: AI Agent Setup

1. **Navigate to AI agent directory**:
   ```bash
   cd ai-agent
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   uv pip install openai python-dotenv
   ```

4. **Set environment variables**:
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   ```

5. **Start AI agent** (for testing, runs in CLI mode):
   ```bash
   uv run python assistant.py
   ```

**Note**: In production, the AI agent will be called by MCP server, not run independently.

---

## Step 4: Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set environment variables**:
   ```bash
   echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
   echo "NEXT_PUBLIC_MCP_URL=http://localhost:8080" >> .env.local
   ```

4. **Start development server**:
   ```bash
   npm run dev
   ```

**Verify**: Visit `http://localhost:3000` and you should see the task dashboard

---

## Testing the System

### 1. Create a User Account

1. Navigate to `http://localhost:3000/register`
2. Create a new account with email and password
3. You'll be redirected to the login page

### 2. Log In

1. Enter your credentials
2. You'll be redirected to the dashboard
3. Note the JWT token stored in localStorage (used by chat widget)

### 3. Open Chat Widget

1. Click the chat icon in the bottom-right corner
2. Chat widget opens as a floating panel

### 4. Create a Task via Natural Language

**Type in chat**:
```
I need to finish the quarterly report by Friday
```

**Expected behavior**:
- AI assistant acknowledges the request
- A new task appears with title "Finish quarterly report"
- Category is inferred (e.g., "Work")
- Confirmation message: "I've created a task for you: 'Finish quarterly report'"
- Task list in dashboard updates automatically

### 5. Toggle Task Completion

**Type in chat**:
```
I'm done with the quarterly report
```

**Expected behavior**:
- AI assistant identifies the task
- Task status changes to "Done"
- Confirmation message: "I've marked 'Finish quarterly report' as Done for you."
- Task list updates with status badge showing "Done"
- **IMPORTANT**: Status badge remains sharp and visible (Constitution Principle X)

### 6. Ask About Tasks

**Type in chat**:
```
What tasks do I have?
```

**Expected behavior**:
- AI assistant lists all your tasks
- Shows title, category, and status for each

**Or filter by category**:
```
Show me my work tasks
```

**Expected behavior**:
- AI assistant lists only tasks in "Work" category

### 7. Delete a Task

**Type in chat**:
```
Remove the grocery list task
```

**Expected behavior**:
- AI assistant identifies the task
- Task is deleted from the system
- Confirmation message: "I've removed the task: 'Grocery list'"
- Task list updates to reflect deletion

---

## Verification Checklist

### Backend (Port 8000)
- [ ] Server starts without errors
- [ ] API documentation accessible at `/docs`
- [ ] Can create user account via API
- [ ] Can login and receive JWT token
- [ ] Task CRUD operations work via Postman/curl

### MCP Server (Port 8080)
- [ ] Server starts without errors
- [ ] Can validate session tokens with backend
- [ ] `list_tasks` tool returns user's tasks
- [ ] `create_task` tool creates new task
- [ ] `toggle_status` tool toggles completion
- [ ] `remove_task` tool deletes task
- [ ] All tools reject invalid/expired tokens

### AI Agent
- [ ] Can parse natural language input
- [ ] Identifies intent (create, toggle, inquiry, delete)
- [ ] Extracts task details from user input
- [ ] Calls appropriate MCP tools
- [ ] Provides helpful confirmation messages

### Frontend (Port 3000)
- [ ] Dashboard renders correctly
- [ ] Can create user account via UI
- [ ] Can login and see dashboard
- [ ] Task list displays tasks
- [ ] Chat widget opens/closes
- [ ] Can send messages to AI
- [ ] Receive AI responses
- [ ] Task list updates after chat operations
- [ ] Status badges remain sharp and visible (Constitution Principle X)

---

## Troubleshooting

### Backend Issues

**Issue**: Backend won't start
- **Check**: Python 3.13+ installed
- **Check**: Virtual environment activated
- **Check**: Dependencies installed: `uv pip list`
- **Check**: Database initialized: `ls backend/todo.db`

**Issue**: Authentication fails
- **Check**: JWT secret key set in `.env`
- **Check**: Token not expired (default 7 days)

### MCP Server Issues

**Issue**: MCP server can't connect to backend
- **Check**: Backend running on port 8000
- **Check**: `BACKEND_URL` set correctly in `.env`
- **Check**: Token validation endpoint exists: `POST /api/v1/validate-token`

**Issue**: Tools fail with "Invalid token"
- **Check**: Frontend session token valid
- **Check**: Token passed correctly to MCP tools

### AI Agent Issues

**Issue**: OpenAI API calls fail
- **Check**: API key set in `.env`
- **Check**: API key has credits
- **Check**: Internet connectivity

**Issue**: Intent recognition inaccurate
- **Check**: System prompt correctly configured
- **Check**: Pattern matching rules loaded

### Frontend Issues

**Issue**: Chat widget doesn't appear
- **Check**: Component imported in dashboard
- **Check**: `sessionToken` prop passed from auth context
- **Check**: Console for errors

**Issue**: Task list doesn't update after chat operation
- **Check**: `refresh-event` emitted by chat widget
- **Check**: Dashboard listening for `refresh-event`
- **Check**: `onRefreshEvent` prop connected

**Issue**: Status badges are blurred (Constitution violation)
- **Check**: CSS filters applied only to task content, not badges
- **Check**: Badge element has `filter: none !important`
- **Check**: CSS selector specificity is correct

---

## Performance Benchmarks

Use these benchmarks to validate performance requirements:

| Operation                    | Target Time | Measured Time | Status |
|------------------------------|-------------|----------------|---------|
| Natural language processing   | < 2s        | _____ ms       |         |
| Task status update            | < 3s        | _____ ms       |         |
| UI sync after write          | < 1s        | _____ ms       |         |
| Intent recognition accuracy    | 90%         | _____ %        |         |

---

## Next Steps

After quickstart validation:

1. **Run test suite**: `npm test` (frontend), `pytest` (backend)
2. **Review Constitution compliance**: Check Principles VII-X
3. **Customize AI agent**: Adjust system prompt for your domain
4. **Add task categories**: Update category inference logic
5. **Deploy**: Set up production environment with PostgreSQL

---

## Additional Resources

- **API Documentation**: `http://localhost:8000/docs`
- **Constitution**: `.specify/memory/constitution.md`
- **MCP Tools Spec**: `specs/001-ai-agentic-system/contracts/mcp-tools.json`
- **Chat Widget Contract**: `specs/001-ai-agentic-system/contracts/chat-widget-component.md`
- **Architecture Research**: `specs/001-ai-agentic-system/research.md`
