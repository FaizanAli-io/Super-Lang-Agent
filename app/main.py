from fastapi import FastAPI
from .database import Base, engine
from .routers import agent, message, session

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(agent.router, prefix="/agents", tags=["agents"])
app.include_router(session.router, prefix="/sessions", tags=["sessions"])
app.include_router(message.router, prefix="/messages", tags=["messages"])
