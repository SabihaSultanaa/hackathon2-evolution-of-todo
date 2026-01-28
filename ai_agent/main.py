from fastapi import FastAPI, HTTPException
from ai_agent.assistant import TaskManagementAgent
import uvicorn
import os

app = FastAPI()
agent = TaskManagementAgent()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(payload: dict):
    message = payload.get("message")
    session_token = payload.get("session_token")
    if not message or not session_token:
        raise HTTPException(status_code=400, detail="Missing message or session_token")
    
    response = await agent.process_message(message, session_token)
    return response

if __name__ == "__main__":
    # Railway uses the PORT env var, Minikube uses 8001
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)