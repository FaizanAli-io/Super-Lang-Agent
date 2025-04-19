from typing import Union
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from .. import schemas
from ..dependencies import get_db
from ..crud.session import CRUDSession

router = APIRouter()


@router.post("/", response_model=Union[schemas.Session, list[schemas.Session]])
def create_session(
    session: Union[schemas.SessionCreate, list[schemas.SessionCreate]],
    db: Session = Depends(get_db),
):
    if isinstance(session, list):
        return [CRUDSession.create(db=db, session=s) for s in session]
    return CRUDSession.create(db=db, session=session)


@router.get("/{session_id}", response_model=schemas.Session)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    return CRUDSession.get(db=db, session_id=session_id)


@router.get("/", response_model=list[schemas.Session])
def get_sessions(
    agent_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return CRUDSession.get_all(db=db, agent_id=agent_id, skip=skip, limit=limit)


@router.put("/{session_id}", response_model=schemas.Session)
def update_session(
    session_id: int,
    session: schemas.SessionCreate,
    db: Session = Depends(get_db),
):
    return CRUDSession.update(db=db, session_id=session_id, update_data=session)


@router.delete("/{session_id}", response_model=schemas.Session)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    return CRUDSession.delete(db=db, session_id=session_id)
