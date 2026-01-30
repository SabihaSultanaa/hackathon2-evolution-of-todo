import logging
import httpx
import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlmodel import Session, select

# Bridge to your Auth and Database
from app.api.v1.auth import get_current_user
from app.database import engine
from app.models import Task, Message

router = APIRouter(tags=["chat"])
logger = logging.getLogger(__name__)

# Get AI Agent URL from environment
AI_AGENT_URL = os.getenv("AI_AGENT_URL")

# Try to import AI agent for monolithic deployment (Phase 3)
try:
    from ai_agent.assistant import TaskManagementAgent
    from ai_agent.intents.extractor import EntityExtractor
    from ai_agent.intents import extract_task_reference
    MONOLITHIC_MODE = True
    logger.info("Running in MONOLITHIC mode (Phase 3) - AI agent imported directly")
except ImportError:
    TaskManagementAgent = None
    EntityExtractor = None
    extract_task_reference = None
    MONOLITHIC_MODE = False
    logger.info("Running in MICROSERVICES mode (Phase 4) - Will use HTTP to call AI agent")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    requires_refresh: bool = False

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest, 
    user=Depends(get_current_user)
):
    try:
        session_token = getattr(user, 'email', str(user.id))
        conversation_id = str(user.id)

        with Session(engine) as db:
            # 1. Load conversation history
            history_statement = select(Message).where(
                Message.conversation_id == conversation_id
            ).order_by(Message.timestamp.desc()).limit(10)
            raw_history = db.exec(history_statement).all()
            conversation_history = [
                {"role": m.role, "content": m.content}
                for m in reversed(raw_history)
            ]
            
            # 2. Get AI response based on deployment mode
            if MONOLITHIC_MODE and TaskManagementAgent:
                # Phase 3: Use direct import (monolithic)
                logger.info("Using monolithic AI agent (direct import)")
                agent = TaskManagementAgent()
                agent_history_with_current_message = conversation_history + [
                    {"role": "user", "content": request.message}
                ]
                result = await agent.process_message(
                    message=request.message,
                    session_token=session_token,
                    conversation_history=agent_history_with_current_message
                )
            elif AI_AGENT_URL:
                # Phase 4: Use HTTP to call separate service (microservices)
                logger.info(f"Using microservices AI agent at {AI_AGENT_URL}")
                async with httpx.AsyncClient(timeout=30.0) as client:
                    try:
                        ai_response = await client.post(
                            f"{AI_AGENT_URL}/chat",
                            json={
                                "message": request.message,
                                "session_token": session_token
                            }
                        )
                        ai_response.raise_for_status()
                        result = ai_response.json()
                    except httpx.HTTPError as e:
                        logger.error(f"Failed to connect to AI agent: {e}")
                        raise HTTPException(
                            status_code=503,
                            detail="AI agent service is unavailable"
                        )
            else:
                # No AI agent available
                raise HTTPException(
                    status_code=500,
                    detail="AI agent not configured. Set AI_AGENT_URL or ensure ai_agent module is available."
                )
            
            logger.info(f"AI Agent Result: {result}")
            ai_message_content = result.get("content", "I'm processing that...")
            
            # 3. Save user message
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
                content=ai_message_content
            )
            db.add(assistant_msg_db)
            db.commit()
            
            # 5. Process tool calls from AI agent
            tool_calls = result.get("tool_calls", [])
            execute_refresh = False
            ai_message = ai_message_content
            
            # If in monolithic mode and we have EntityExtractor, resolve task references
            if MONOLITHIC_MODE and EntityExtractor and extract_task_reference:
                final_tool_calls = []
                for call in tool_calls:
                    call_name = call.get("name")
                    call_args = call.get("arguments", {})
                    
                    if call_name in ["toggle_task", "delete_task", "update_task"]:
                        task_reference = call_args.get("task_reference")
                        if task_reference:
                            statement = select(Task).where(Task.user_id == user.id)
                            user_tasks = db.exec(statement).all()
                            user_tasks_dicts = [{
                                "id": t.id,
                                "title": t.title,
                                "description": t.description,
                                "category": t.category,
                                "completed": t.completed
                            } for t in user_tasks]
                            
                            identified_task = EntityExtractor.extract_task_reference(
                                task_reference, user_tasks_dicts
                            )
                            
                            if identified_task:
                                new_call_args = {k: v for k, v in call_args.items() if k != "task_reference"}
                                new_call_args["task_id"] = identified_task["id"]
                                final_tool_calls.append({
                                    "name": call_name,
                                    "arguments": new_call_args
                                })
                            else:
                                logger.warning(f"Could not resolve task reference: {task_reference}")
                                continue
                        else:
                            continue
                    else:
                        final_tool_calls.append(call)
                
                tool_calls = final_tool_calls
            
            # Execute tool calls
            for call in tool_calls:
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
                
                elif call_name == "list_tasks":
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
                        task_list = "\n".join([
                            f"• {t.title} (ID: {t.id}, {'Completed' if t.completed else 'Pending'})"
                            for t in tasks
                        ])
                        ai_message = f"Here are your tasks:\n{task_list}"
                    else:
                        ai_message = "You don't have any tasks yet."
                
                elif call_name == "toggle_task":
                    task_id = call_args.get("task_id")
                    if task_id:
                        task = db.get(Task, task_id)
                        if task and task.user_id == user.id:
                            task.completed = not task.completed
                            db.add(task)
                            db.commit()
                            execute_refresh = True
                            ai_message = f"Task '{task.title}' marked as {'completed' if task.completed else 'pending'}."
                        else:
                            ai_message = "I couldn't find that task."
                
                elif call_name == "delete_task":
                    task_id = call_args.get("task_id")
                    if task_id:
                        task = db.get(Task, task_id)
                        if task and task.user_id == user.id:
                            db.delete(task)
                            db.commit()
                            execute_refresh = True
                            ai_message = f"Task '{task.title}' deleted."
                        else:
                            ai_message = "I couldn't find that task."
                
                elif call_name == "update_task":
                    task_id = call_args.get("task_id")
                    if task_id:
                        task = db.get(Task, task_id)
                        if task and task.user_id == user.id:
                            if call_args.get("new_title"):
                                task.title = call_args["new_title"]
                            if call_args.get("new_description") is not None:
                                task.description = call_args["new_description"]
                            if call_args.get("new_category"):
                                task.category = call_args["new_category"]
                            
                            db.add(task)
                            db.commit()
                            execute_refresh = True
                            ai_message = f"Task '{task.title}' updated."
                        else:
                            ai_message = "I couldn't find that task."
            
            return ChatResponse(
                response=ai_message,
                requires_refresh=execute_refresh
            )
    
    except Exception as e:
        logger.exception(f"Chat error: {str(e)}")
        return ChatResponse(
            response="Sorry, I'm having trouble connecting to the server.",
            requires_refresh=False
        )