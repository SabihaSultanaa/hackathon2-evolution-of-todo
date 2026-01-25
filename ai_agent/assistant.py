"""OpenAI Agent for task management.

This agent uses the OpenAI Assistants API to understand natural language
and execute task management operations.

Constitution Compliance:
- Principle VIII: Protocol Standardization - All operations route through defined tools
- Principle IX: Statelessness - Agent is stateless, relies on session_token
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
import logging
from typing import Dict, Any, List, Optional
import json

from ai_agent.prompts.system import SYSTEM_PROMPT
# Removed: from ai_agent.intents.parser import parse_intent, Intent
# Removed: from ai_agent.intents.extractor import (
# Removed:     extract_create_entities,
# Removed:     extract_task_reference,
# Removed:     extract_inquiry_filters
# Removed: )

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    client = None
    logger.warning(f"OpenAI client could not be initialized: {e}. AI assistant will be disabled.")


class TaskManagementAgent:
    """AI agent for task management using OpenAI function calling."""

    def __init__(self):
        """Initialize the task management agent."""
        self.client = client
        self.system_prompt = SYSTEM_PROMPT
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the user's todo list.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The title of the task."
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional: A detailed description for the task."
                            },
                            "category": {
                                "type": "string",
                                "description": "Optional: The category of the task (e.g., 'Work', 'Personal', 'Urgent', 'Shopping', 'General'). Defaults to 'General'."
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List existing tasks for the user, optionally filtered by category or status.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "description": "Optional: Filter tasks by category (e.g., 'Work', 'Personal', 'Urgent')."
                            },
                            "status": {
                                "type": "string",
                                "enum": ["completed", "pending", "all"],
                                "description": "Optional: Filter tasks by status ('completed', 'pending', 'all'). Defaults to 'all'."
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "toggle_task",
                    "description": "Toggle the completion status of a specific task (from completed to pending, or vice-versa).",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_reference": {
                                "type": "string",
                                "description": "A reference to the task to toggle, e.g., 'the report', 'task 3', 'buy groceries'."
                            }
                        },
                        "required": ["task_reference"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Permanently delete a specific task from the user's todo list.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_reference": {
                                "type": "string",
                                "description": "A reference to the task to delete, e.g., 'the old report', 'task 5', 'meeting notes'."
                            }
                        },
                        "required": ["task_reference"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update the title, description, or category of an existing task.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_reference": {
                                "type": "string",
                                "description": "A reference to the task to update, e.g., 'the report', 'task 3'."
                            },
                            "new_title": {
                                "type": "string",
                                "description": "Optional: The new title for the task."
                            },
                            "new_description": {
                                "type": "string",
                                "description": "Optional: The new description for the task."
                            },
                            "new_category": {
                                "type": "string",
                                "description": "Optional: The new category for the task."
                            }
                        },
                        "required": ["task_reference"]
                    }
                }
            }
        ]

    async def process_message(
        self,
        message: str,
        session_token: str,
        conversation_history: List[Dict[str, Any]] | None = None,
        available_tools: List[Dict[str, Any]] | None = None # This parameter is now mostly ignored
    ) -> Dict[str, Any]:
        """Process user message and return AI response, using OpenAI function calling.

        Args:
            message: User's natural language input
            session_token: User's authentication token (not directly used by LLM, but for tools)
            conversation_history: Previous conversation context (optional, but good for future)

        Returns:
            Dict containing assistant response, tool calls, and intent (derived from tool call)
        """
        if not self.client:
            return {
                "content": "The AI assistant is not configured. Please set the OPENAI_API_KEY.",
                "tool_calls": [],
                "intent": "error"
            }
        
        messages = [{"role": "system", "content": self.system_prompt}]
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self.tools,
                tool_choice="auto", # Let the LLM decide if it needs to call a tool
                temperature=0.7
            )

            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls

            if tool_calls:
                # The LLM decided to call one or more tools
                parsed_tool_calls = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        logger.error(f"LLM provided malformed JSON for tool arguments: {tool_call.function.arguments}")
                        # If malformed, treat as a conversational response or log and skip this tool call
                        # For now, we'll log and treat it as if no tool call was intended for this specific one.
                        continue # Skip to next tool call if any
                    
                    # Add session_token to relevant tool calls
                    if function_name in ["add_task", "list_tasks", "toggle_task", "delete_task", "update_task"]:
                        function_args["session_token"] = session_token
                    
                    parsed_tool_calls.append({
                        "name": function_name,
                        "arguments": function_args
                    })
                
                if parsed_tool_calls: # Only proceed if there are successfully parsed tool calls
                    # Determine intent based on the first tool call
                    # Ensure intent is always uppercase string, e.g., "ADD", "LIST"
                    intent_from_tool = parsed_tool_calls[0]["name"].split('_')[0].upper() 
                    logger.info(f"LLM generated tool calls: {parsed_tool_calls}, derived intent: {intent_from_tool}")
                    return {
                        "content": response_message.content or "Okay, processing your request.",
                        "tool_calls": parsed_tool_calls,
                        "intent": intent_from_tool
                    }
                else: # No valid tool calls were parsed, treat as conversational
                    logger.info(f"LLM responded with content: {response_message.content} (no valid tool calls parsed)")
                    return {
                        "content": response_message.content,
                        "tool_calls": [],
                        "intent": "chat" # A generic intent for conversational responses
                    }
            else:
                # The LLM responded with a natural language message
                logger.info(f"LLM responded with content: {response_message.content} (no tool calls)")
                return {
                    "content": response_message.content,
                    "tool_calls": [],
                    "intent": "chat" # A generic intent for conversational responses
                }

        except Exception as e:
            logger.error(f"OpenAI API error: {e}", exc_info=True)
            return {
                "content": "I'm having trouble connecting to my AI brain. Please check the backend logs.",
                "tool_calls": [],
                "intent": "error"
            }

# Removed global agent instance and process_user_message convenience function
# The TaskManagementAgent should be instantiated in chat.py
# Removed: async def _handle_create_intent(...)
# Removed: async def _handle_toggle_intent(...)
# Removed: async def _handle_inquiry_intent(...)
# Removed: async def _handle_delete_intent(...)
# Removed: if __name__ == "__main__": test code
