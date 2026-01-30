"""FastAPI application entry point."""

import logging
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.config import get_settings
from app.api.v1 import auth, tasks, chat  
from app.database import engine

settings = get_settings()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="Todo API with JWT authentication and AI Chatbot",
)

# 1. CORS Middleware 
# We use "*" for origins during the hackathon to ensure no connection is blocked
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Custom Exception Middleware
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error("=" * 50)
        logger.error("EXCEPTION CAUGHT BY MIDDLEWARE:")
        logger.error(traceback.format_exc())
        logger.error("=" * 50)
        
        # Returning JSON instead of plain Response ensures the Frontend 
        # can parse the error message.
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal Server Error",
                "message": str(e)
            }
        )

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    logger.info("Initializing database tables...")
    try:
        SQLModel.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.app_version}

@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Todo API",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)