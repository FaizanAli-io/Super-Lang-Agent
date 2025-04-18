from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas
from ..dependencies import get_db
from ..crud.message import CRUDMessage

router = APIRouter()


@router.post("/", response_model=schemas.Message)
def create_message(
    message: schemas.MessageCreate,
    session_id: int,
    db: Session = Depends(get_db),
):
    return CRUDMessage.create(db=db, message=message, session_id=session_id)


@router.get("/{message_id}", response_model=schemas.Message)
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
):
    return CRUDMessage.get(db=db, message_id=message_id)


@router.get("/", response_model=list[schemas.Message])
def get_messages(
    session_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return CRUDMessage.get_all(db=db, session_id=session_id, skip=skip, limit=limit)


@router.put("/{message_id}", response_model=schemas.Message)
def update_message(
    message_id: int,
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
):
    return CRUDMessage.update(db=db, message_id=message_id, update_data=message)


@router.delete("/{message_id}", response_model=schemas.Message)
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
):
    return CRUDMessage.delete(db=db, message_id=message_id)
