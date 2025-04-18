from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import (
    Enum,
    Text,
    String,
    Column,
    Integer,
    DateTime,
    ForeignKey,
)

from .database import Base
from .enums import ToolEnum


class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    tools = Column(ARRAY(Enum(ToolEnum)))
    description = Column(String, nullable=True)
    sessions = relationship("Session", back_populates="agent")


class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"))
    created_at = Column(DateTime, default=datetime.now)
    agent = relationship("Agent", back_populates="sessions")
    messages = relationship("Message", back_populates="session")


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    content = Column(Text)
    sender = Column(String)
    timestamp = Column(DateTime, default=datetime.now)
    session = relationship("Session", back_populates="messages")
