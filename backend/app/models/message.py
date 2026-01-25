from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime, timezone

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: str = Field(index=True)
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
