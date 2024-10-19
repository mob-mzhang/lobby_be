from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List, Optional
from sqlalchemy import and_

def add_user_to_event(db: Session, user_id: str, event_id: str) -> Optional[schemas.Event]:
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_event and db_user:
        db_event.users.append(db_user)
        db.commit()
        db.refresh(db_event)
    return db_event

def remove_user_from_event(db: Session, user_id: str, event_id: str) -> Optional[schemas.Event]:
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_event and db_user:
        db_event.users.remove(db_user)
        db.commit()
        db.refresh(db_event)
    return db_event

def get_user_events(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[schemas.Event]:
    return db.query(models.Event).filter(models.Event.users.any(id=user_id)).offset(skip).limit(limit).all()

def get_available_events_for_user(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[models.Event]:
    friend_relationships = db.query(models.Friend).filter(models.Friend.user_id == user_id).all()
    friend_ids = [fr.friend_id for fr in friend_relationships]
    
    available_events = db.query(models.Event).join(models.user_event).filter(
        models.user_event.c.user_id.in_(friend_ids)
    ).distinct().offset(skip).limit(limit).all()
    
    return available_events

def is_user_in_event(db: Session, user_id: str, event_id: str) -> bool:
    return db.query(models.user_event).filter(
        and_(
            models.user_event.c.user_id == user_id,
            models.user_event.c.event_id == event_id
        )
    ).first() is not None
