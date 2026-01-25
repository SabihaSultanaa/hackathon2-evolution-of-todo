import sys
import os
import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlmodel import Session, select

# Bridge to your Auth and Database
from app.api.v1.auth import get_current_user
from app.database import engine
from app.models import Task, Message

# --- ROBUST PATH BRIDGE ---
current_file_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_file_path, "../../../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

try:
    from ai_agent.assistant import TaskManagementAgent
    from ai_agent.intents.extractor import EntityExtractor # Now importing EntityExtractor directly
    from ai_agent.intents import extract_task_reference # Now importing from __init__.py
except ImportError as e:
    logging.exception("Could not import AI agent components")
    TaskManagementAgent = None
    EntityExtractor = None # Adjust this if only EntityExtractor is used
    extract_task_reference = None


router = APIRouter(tags=["chat"])
logger = logging.getLogger(__name__)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    requires_refresh: bool = False

# This decorator + the prefix in main.py creates: /api/v1/chat
@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest, 
    user=Depends(get_current_user)
):
    if TaskManagementAgent is None or extract_task_reference is None: # Removed Intent from check
        raise HTTPException(status_code=500, detail="AI agent components not loaded due to import errors.")

    try:
        agent = TaskManagementAgent() # Instantiate agent here
        session_token = getattr(user, 'email', str(user.id))
        conversation_id = str(user.id) # Use user ID as conversation ID

        with Session(engine) as db:
            # 1. Load History
            history_statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.timestamp.desc()).limit(10) # Get last 10 messages
            raw_history = db.exec(history_statement).all()
            # History needs to be in chronological order for the agent
            conversation_history = [
                {"role": m.role, "content": m.content}
                for m in reversed(raw_history)
            ]
            
            # Append current user message to history for agent processing (but don't save yet)
            agent_history_with_current_message = conversation_history + [{"role": "user", "content": request.message}]

            # 2. Get AI Response
            result = await agent.process_message(
                message=request.message,
                session_token=session_token,
                conversation_history=agent_history_with_current_message
            )
            logger.info(f"== RAW AI Agent Result: {result}") # LOGGING
            logger.info(f"User message: {request.message}") # Log user message
            
            ai_message_content = result.get("content", "I'm processing that...")

            # 3. Save current user message
            user_msg_db = Message(
                conversation_id=conversation_id,
                role="user",
                content=request.message
            )
            db.add(user_msg_db)
            
            # 4. Save AI response
            assistant_msg_db = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=ai_message_content # Use the content directly from the agent's result
            )
            db.add(assistant_msg_db)
            db.commit()
            db.refresh(user_msg_db)
            db.refresh(assistant_msg_db)

            if result.get("intent") == "error" and "not configured" in result.get("content", ""):
                raise HTTPException(status_code=500, detail=result.get("content"))

            ai_message = ai_message_content # Set ai_message for tool processing below
            tool_calls = result.get("tool_calls", [])
            logger.info(f"== Initial tool_calls from agent: {tool_calls}") # LOGGING
            execute_refresh = False

            # --- Enhanced Database Execution based on tool_calls ---
            final_tool_calls = [] # This will hold calls with resolved task_ids

            for call in tool_calls:
                call_name = call.get("name")
                call_args = call.get("arguments", {})
                
                # Handle task_reference resolution for TOGGLE, DELETE, UPDATE
                if call_name in ["toggle_task", "delete_task", "update_task"]:
                    task_reference = call_args.get("task_reference")
                    if task_reference:
                        statement = select(Task).where(Task.user_id == user.id)
                        user_tasks: List[Task] = db.exec(statement).all()
                        
                        user_tasks_dicts = [{
                            "id": t.id, 
                            "title": t.title, 
                            "description": t.description, 
                            "category": t.category, 
                            "completed": t.completed
                        } for t in user_tasks]

                        # EntityExtractor.extract_task_reference might need actual chat history for context
                        identified_task = EntityExtractor.extract_task_reference(task_reference, user_tasks_dicts)
                        
                        if identified_task:
                            resolved_task_id = identified_task["id"]
                            # Create a new tool call with the resolved ID
                            new_call_args = {k: v for k, v in call_args.items() if k != "task_reference"}
                            new_call_args["task_id"] = resolved_task_id
                            final_tool_calls.append({
                                "name": call_name,
                                "arguments": new_call_args
                            })
                            ai_message = result.get("content", f"Okay, I'll try to {call_name.replace('_task', '')} '{identified_task['title']}'.")
                        else:
                            ai_message = "I couldn't identify the specific task you're referring to. Please be more specific or provide the task number."
                            logger.warning(f"No task identified for {call_name} from reference '{task_reference}'.")
                            # If task reference could not be resolved, do not add to final_tool_calls
                            continue # Skip to next tool call
                    else:
                        ai_message = f"I need a task reference to {call_name.replace('_task', '')}."
                        logger.warning(f"Tool call {call_name} without task_reference.")
                        continue # Skip to next tool call
                else:
                    final_tool_calls.append(call) # For add_task, list_tasks, etc. directly add

            logger.info(f"Final tool_calls before execution: {final_tool_calls}")
            # Execute tool calls (now with resolved task_ids)
            for call in final_tool_calls:
                call_name = call.get("name")
                call_args = call.get("arguments", {})
                logger.info(f"Executing tool call: {call_name} with args: {call_args}")

                if call_name == "add_task":
                    new_task = Task(
                        title=call_args.get("title", "New Task"),
                        description=call_args.get("description", ""),
                        category=call_args.get("category", "General"),
                        user_id=user.id
                    )
                    db.add(new_task)
                    db.commit()
                    db.refresh(new_task)
                    execute_refresh = True
                    ai_message = f"Added task: '{new_task.title}'."
                    logger.info(f"Task added: {new_task.title}")
                
                elif call_name == "list_tasks":
                    # Filter by category if provided by LLM
                    category_filter = call_args.get("category")
                    status_filter = call_args.get("status")

                    statement = select(Task).where(Task.user_id == user.id)
                    if category_filter:
                        statement = statement.where(Task.category == category_filter)
                    if status_filter == "completed":
                        statement = statement.where(Task.completed == True)
                    elif status_filter == "pending":
                        statement = statement.where(Task.completed == False)

                    tasks = db.exec(statement).all()
                    if tasks:
                        task_list = "\n".join([f"• {t.title} (ID: {t.id}, {'Completed' if t.completed else 'Pending'})" for t in tasks])
                        ai_message = f"Here are your tasks:\n{task_list}"
                        logger.info("Tasks listed.")
                    else:
                        ai_message = "You don't have any tasks yet."
                        logger.info("No tasks to list.")
                
                elif call_name == "toggle_task":
                    task_id = call_args.get("task_id")
                    if task_id:
                        task_to_toggle = db.get(Task, task_id)
                        logger.info(f"Attempting to toggle task ID {task_id}. Found: {task_to_toggle}")
                        if task_to_toggle and task_to_toggle.user_id == user.id:
                            task_to_toggle.completed = not task_to_toggle.completed
                            db.add(task_to_toggle)
                            db.commit()
                            db.refresh(task_to_toggle)
                            execute_refresh = True
                            ai_message = f"Task '{task_to_toggle.title}' marked as {'completed' if task_to_toggle.completed else 'pending'}."
                            logger.info(f"Task toggled: {task_to_toggle.title}, new status: {task_to_toggle.completed}")
                        else:
                            ai_message = "I couldn't find that task to toggle or it doesn't belong to you."
                            logger.warning(f"Failed to toggle task ID {task_id}. Not found or user mismatch.")
                    else:
                        ai_message = "I need a task ID to toggle."
                        logger.warning("Toggle task call without task_id.")
                
                elif call_name == "delete_task":
                    task_id = call_args.get("task_id")
                    if task_id:
                        task_to_delete = db.get(Task, task_id)
                        logger.info(f"Attempting to delete task ID {task_id}. Found: {task_to_delete}")
                        if task_to_delete and task_to_delete.user_id == user.id:
                            db.delete(task_to_delete)
                            db.commit()
                            execute_refresh = True
                            ai_message = f"Task '{task_to_delete.title}' deleted."
                            logger.info(f"Task deleted: {task_to_delete.title}")
                        else:
                            ai_message = "I couldn't find that task to delete or it doesn't belong to you."
                            logger.warning(f"Failed to delete task ID {task_id}. Not found or user mismatch.")
                    else:
                        ai_message = "I need a task ID to delete."
                        logger.warning("Delete task call without task_id.")
                
                elif call_name == "update_task":
                    task_id = call_args.get("task_id")
                    if task_id:
                        task_to_update = db.get(Task, task_id)
                        logger.info(f"Attempting to update task ID {task_id}. Found: {task_to_update}")
                        if task_to_update and task_to_update.user_id == user.id:
                            new_title = call_args.get("new_title")
                            new_description = call_args.get("new_description")
                            new_category = call_args.get("new_category")

                            if new_title:
                                task_to_update.title = new_title
                            if new_description is not None: # Allow empty string to clear description
                                task_to_update.description = new_description
                            if new_category:
                                task_to_update.category = new_category
                            
                            db.add(task_to_update)
                            db.commit()
                            db.refresh(task_to_update)
                            execute_refresh = True
                            ai_message = f"Task '{task_to_update.title}' updated successfully."
                            logger.info(f"Task updated: {task_to_update.title}")
                        else:
                            ai_message = "I couldn't find that task to update or it doesn't belong to you."
                            logger.warning(f"Failed to update task ID {task_id}. Not found or user mismatch.")
                    else:
                        ai_message = "I need a task ID to update."
                        logger.warning("Update task call without task_id.")


            return ChatResponse(
                response=ai_message,
                requires_refresh=execute_refresh
            )

        
    except Exception as e:
        logger.exception(f"Critical Chat Error: {str(e)}") # Using logger.exception here
        if isinstance(e, HTTPException) and "not configured" in e.detail:
            return ChatResponse(
                response=e.detail,
                requires_refresh=False
            )
        return ChatResponse(
            response="I'm having trouble connecting to my AI brain. Please check the backend logs for details.",
            requires_refresh=False
        )