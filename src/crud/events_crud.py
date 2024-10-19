from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List, Optional

def create_event(db: Session, event: schemas.Event) -> schemas.Event:
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_event(db: Session, event_id: str) -> Optional[schemas.Event]:
    return db.query(models.Event).filter(models.Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.Event]:
    return db.query(models.Event).offset(skip).limit(limit).all()

def update_event(db: Session, event_id: str, event_update: schemas.Event) -> Optional[schemas.Event]:
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        for key, value in event_update.dict(exclude_unset=True).items():
            setattr(db_event, key, value)
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: str) -> Optional[schemas.Event]:
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event
