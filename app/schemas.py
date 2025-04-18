from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from .enums import ToolEnum


class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    tools: Optional[List[ToolEnum]] = None


class AgentCreate(AgentBase):
    pass


class Agent(AgentBase):
    id: int
    sessions: List["Session"] = []

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    sender: str
    content: str
    timestamp: datetime


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    session_id: int

    class Config:
        from_attributes = True


class SessionBase(BaseModel):
    agent_id: int


class SessionCreate(SessionBase):
    pass


class Session(SessionBase):
    id: int
    created_at: datetime
    messages: List[Message]

    class Config:
        from_attributes = True
