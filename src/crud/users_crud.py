from sqlalchemy.orm import Session
from .. import models, schemas
from typing import List, Optional
import uuid
from sqlalchemy.exc import IntegrityError
from datetime import datetime

def create_user(db: Session, user: schemas.User):
    db_user = models.User(
        id=user.id,
        username=user.username,
        phone_number=user.phone_number,
        created_at=user.created_at,
        updated_at=user.updated_at
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str) -> Optional[schemas.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[schemas.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_phone(db: Session, phone_number: str) -> Optional[schemas.User]:
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: str, user_update: schemas.User) -> Optional[schemas.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str) -> Optional[schemas.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def create_friendship(db: Session, user_id: str, friend_id: str) -> models.Friend:
    try:
        friendship = models.Friend(id=str(uuid.uuid4()), user_id=user_id, friend_id=friend_id)
        db.add(friendship)
        db.commit()
        db.refresh(friendship)
        return friendship
    except IntegrityError:
        db.rollback()
        raise ValueError("Friendship already exists or invalid user/friend ID")

def get_user_friends(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[schemas.Friend]:
    return db.query(models.Friend).filter(models.Friend.user_id == user_id).offset(skip).limit(limit).all()
