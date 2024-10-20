from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from src import models, schema
from typing import List, Optional
from uuid import uuid4

def create_user(db: Session, user: schema.UserCreate) -> models.User:
    db_user = models.User(id=str(uuid4()), **user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: str, include_friends: bool = False, include_lobbies: bool = False, include_parties: bool = False) -> Optional[models.User]:
    query = db.query(models.User)
    if include_friends:
        query = query.options(joinedload(models.User.friends))
    if include_lobbies:
        query = query.options(joinedload(models.User.lobbies))
    if include_parties:
        query = query.options(joinedload(models.User.parties))
    return query.filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: str, user_update: dict) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for key, value in user_update.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str) -> bool:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def add_friend(db: Session, user_id: str, friend_username: str) -> Optional[models.Friend]:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    friend = db.query(models.User).filter(models.User.username == friend_username).first()
    
    if user and friend:
        new_friendship = models.Friend(user_id=user.id, friend_id=friend.id)
        db.add(new_friendship)
        try:
            db.commit()
            db.refresh(new_friendship)
            return new_friendship
        except IntegrityError:
            db.rollback()
    return None

def join_lobby(db: Session, user_id: str, lobby_id: str) -> Optional[models.Lobby]:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    
    if user and lobby:
        user.lobbies.append(lobby)
        db.commit()
        db.refresh(lobby)
        return lobby
    return None

def set_queue_status(db: Session, user_id: str, active: bool) -> Optional[models.User]:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.queue_status = active
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def get_users_by_queue_status(db: Session, active: bool) -> List[models.User]:
    return db.query(models.User).filter(models.User.queue_status == active).all()

def get_user_by_phone(db: Session, phone_number: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

def get_user_lobbies(db: Session, user_id: str) -> List[models.Lobby]:
    """
    Retrieve all lobbies associated with a user.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        return user.lobbies  # Assuming there's a relationship defined between User and Lobby
    return []
