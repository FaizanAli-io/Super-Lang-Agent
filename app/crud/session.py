from sqlalchemy.orm import Session
from .. import models, schemas


class CRUDSession:
    @staticmethod
    def create(db: Session, session: schemas.SessionCreate):
        db_session = models.Session(agent_id=session.agent_id)
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session

    @staticmethod
    def get_all(db: Session, agent_id: int, skip: int = 0, limit: int = 100):
        return (
            db.query(models.Session)
            .filter(models.Session.agent_id == agent_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get(db: Session, session_id: int):
        return db.query(models.Session).filter(models.Session.id == session_id).first()

    @staticmethod
    def update(db: Session, session_id: int, update_data: schemas.SessionCreate):
        session = (
            db.query(models.Session).filter(models.Session.id == session_id).first()
        )
        if session:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(session, key, value)
            db.commit()
            db.refresh(session)
        return session

    @staticmethod
    def delete(db: Session, session_id: int):
        session = (
            db.query(models.Session).filter(models.Session.id == session_id).first()
        )
        if session:
            db.delete(session)
            db.commit()
        return session
