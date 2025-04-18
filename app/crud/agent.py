from sqlalchemy.orm import Session
from .. import models, schemas


class CRUDAgent:
    @staticmethod
    def create(db: Session, agent: schemas.AgentCreate):
        db_agent = models.Agent(**agent.dict())
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent

    @staticmethod
    def get(db: Session, agent_id: int):
        return db.query(models.Agent).filter(models.Agent.id == agent_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Agent).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, agent_id: int, update_data: schemas.AgentCreate):
        agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
        if agent:
            for key, value in update_data.dict(exclude_unset=True).items():
                setattr(agent, key, value)
            db.commit()
            db.refresh(agent)
        return agent

    @staticmethod
    def delete(db: Session, agent_id: int):
        agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
        if agent:
            db.delete(agent)
            db.commit()
        return agent
