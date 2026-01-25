"""MCP Server for AI-Powered Task Management.

This server exposes task management tools via the Model Context Protocol (MCP),
enabling AI agents to interact with the task management system through standardized tools.

Constitution Compliance:
- Principle VIII: Protocol Standardization - All operations route through MCP SDK
- Principle IX: Authentication Requirements - All tools require valid session_token
"""

import json
from mcp.server import Server
from mcp.types import Tool, TextContent
import logging
import os
from typing import Any

from mcp_server.client.backend import BackendClient
from mcp_server.auth.validator import validate_session_token, TokenValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Backend API client
backend_client = BackendClient()

# MCP Server instance
server = Server("task-management-mcp-server")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List all available MCP tools."""
    return [
        Tool(
            name="list_tasks",
            description="List all tasks for the authenticated user. Optionally filter by category.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_token": {
                        "type": "string",
                        "description": "JWT session token for authentication (required)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Optional category filter (e.g., 'Work', 'Personal')"
                    }
                },
                "required": ["session_token"]
            }
        ),
        Tool(
            name="add_task",
            description="Create a new task with title, optional description, and category.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_token": {
                        "type": "string",
                        "description": "JWT session token for authentication (required)"
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title (required, max 500 characters)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Task description (optional, max 5000 characters)"
                    },
                    "category": {
                        "type": "string",
                        "description": "Task category (optional, defaults to 'General')"
                    }
                },
                "required": ["session_token", "title"]
            }
        ),
        Tool(
            name="toggle_task",
            description="Toggle a task's completion status (complete <-> pending).",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_token": {
                        "type": "string",
                        "description": "JWT session token for authentication (required)"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to toggle (required)"
                    }
                },
                "required": ["session_token", "task_id"]
            }
        ),
        Tool(
            name="delete_task",
            description="Permanently delete a task by ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "session_token": {
                        "type": "string",
                        "description": "JWT session token for authentication (required)"
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "ID of the task to delete (required)"
                    }
                },
                "required": ["session_token", "task_id"]
            }
        )
    }


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool execution with authentication.

    Constitution Principle IX: All MCP tool calls MUST require a valid session_token.
    """
    try:
        # Extract and validate session token (Principle IX)
        session_token = arguments.get("session_token")
        if not session_token:
            logger.warning(f"Tool {name} called without session_token")
            return [TextContent(
                type="text",
                text=json.dumps({
                    "error": "Authentication required: session_token is missing"
                }, indent=2)
            )]

        # Validate token with backend
        user_info = await validate_session_token(session_token, backend_client)
        logger.info(f"Executing tool {name} for user: {user_info.get('username', 'unknown')}")

        # Execute tool based on name
        if name == "list_tasks":
            result = await handle_list_tasks(session_token, arguments.get("category"))
        elif name == "add_task":
            result = await handle_add_task(session_token, arguments)
        elif name == "toggle_task":
            result = await handle_toggle_task(session_token, arguments)
        elif name == "delete_task":
            result = await handle_delete_task(session_token, arguments)
        else:
            return [TextContent(
                type="text",
                text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2)
            )]

        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )]

    except TokenValidationError as e:
        logger.warning(f"Token validation failed for tool {name}: {e}")
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": "Authentication failed: " + str(e)
            }, indent=2)
        )]
    except Exception as e:
        logger.error(f"Error executing tool {name}: {e}")
        return [TextContent(
            type="text",
            text=json.dumps({
                "error": "Internal error: " + str(e)
            }, indent=2)
        )]


async def handle_list_tasks(session_token: str, category: str | None) -> dict[str, Any]:
    """List tasks with optional category filter."""
    result = await backend_client.get_tasks(session_token, category)
    return {
        "success": True,
        "tasks": result.get("tasks", []),
        "count": len(result.get("tasks", [])),
        "category_filter": category
    }


async def handle_add_task(session_token: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Create a new task."""
    title = arguments.get("title")
    description = arguments.get("description", "")
    category = arguments.get("category", "General")

    if not title:
        return {
            "error": "Validation failed: title is required"
        }

    if len(title) > 500:
        return {
            "error": f"Validation failed: title exceeds 500 characters (got {len(title)})"
        }

    if len(description) > 5000:
        return {
            "error": f"Validation failed: description exceeds 5000 characters (got {len(description)})"
        }

    task = await backend_client.create_task(session_token, title, description, category)
    return {
        "success": True,
        "task": task
    }


async def handle_toggle_task(session_token: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Toggle task completion status."""
    task_id = arguments.get("task_id")

    if not task_id or not isinstance(task_id, int):
        return {
            "error": f"Validation failed: task_id must be an integer, got {type(task_id)}"
        }

    task = await backend_client.toggle_task_status(session_token, task_id)
    return {
        "success": True,
        "task": task
    }


async def handle_delete_task(session_token: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """Delete a task."""
    task_id = arguments.get("task_id")

    if not task_id or not isinstance(task_id, int):
        return {
            "error": f"Validation failed: task_id must be an integer, got {type(task_id)}"
        }

    result = await backend_client.remove_task(session_token, task_id)
    return {
        "success": True,
        "message": f"Task {task_id} deleted successfully"
    }


async def main():
    """Start the MCP server."""
    logger.info("Starting MCP server for AI-powered task management")
    async with server.run() as server_session:
        logger.info("MCP server running and ready for tool calls")
        # Keep server running
        await server_session.join()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
