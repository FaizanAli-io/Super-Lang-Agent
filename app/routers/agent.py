from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..dependencies import get_db
from ..crud.agent import CRUDAgent

router = APIRouter()


@router.post("/", response_model=schemas.Agent)
def create_agent(
    agent: schemas.AgentCreate,
    db: Session = Depends(get_db),
):
    return CRUDAgent.create(db=db, agent=agent)


@router.get("/{agent_id}", response_model=schemas.Agent)
def get_agent(
    agent_id: int,
    db: Session = Depends(get_db),
):
    return CRUDAgent.get(db=db, agent_id=agent_id)


@router.get("/", response_model=list[schemas.Agent])
def get_agents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return CRUDAgent.get_all(db=db, skip=skip, limit=limit)


@router.put("/{agent_id}", response_model=schemas.Agent)
def update_agent(
    agent_id: int,
    agent: schemas.AgentCreate,
    db: Session = Depends(get_db),
):
    return CRUDAgent.update(db=db, agent_id=agent_id, update_data=agent)


@router.delete("/{agent_id}", response_model=schemas.Agent)
def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db),
):
    return CRUDAgent.delete(db=db, agent_id=agent_id)
