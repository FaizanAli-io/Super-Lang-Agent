from sqlalchemy.orm import Session
from .. import models, schemas


class CRUDMessage:
    @staticmethod
    def create(db: Session, message: schemas.MessageCreate, session_id: int):
        db_message = models.Message(**message.dict(), session_id=session_id)
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    @staticmethod
    def get_all(db: Session, session_id: int, skip: int = 0, limit: int = 100):
        return (
            db.query(models.Message)
            .filter(models.Message.session_id == session_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get(db: Session, message_id: int):
        return db.query(models.Message).filter(models.Message.id == message_id).first()

    @staticmethod
    def update(db: Session, message_id: int, update_data: schemas.MessageCreate):
        message = (
            db.query(models.Message).filter(models.Message.id == message_id).first()
        )
        if message:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(message, key, value)
            db.commit()
            db.refresh(message)
        return message

    @staticmethod
    def delete(db: Session, message_id: int):
        message = (
            db.query(models.Message).filter(models.Message.id == message_id).first()
        )
        if message:
            db.delete(message)
            db.commit()
        return message
