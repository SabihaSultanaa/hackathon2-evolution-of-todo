"""AI Agent module for natural language task management.

This module provides an AI assistant that understands natural language
and executes task management operations through MCP tools.

Constitution Compliance:
- Principle VIII: Protocol Standardization - All operations route through MCP tools
- Principle IX: Statelessness - Agent is stateless, relies on session_token
"""

from .assistant import TaskManagementAgent

__all__ = ["TaskManagementAgent"]
