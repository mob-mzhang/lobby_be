from sqlalchemy.orm import Session, joinedload
from src import models, schema
from typing import List, Optional
from uuid import uuid4
from datetime import datetime

def create_lobby(db: Session, lobby: schema.LobbyCreate, host_id: str) -> models.Lobby:
    db_lobby = models.Lobby(id=str(uuid4()), **lobby.dict(), host_id=host_id)
    db.add(db_lobby)
    db.commit()
    db.refresh(db_lobby)
    return db_lobby

def get_lobby(db: Session, lobby_id: str, include_users: bool = False, include_host: bool = False) -> Optional[models.Lobby]:
    query = db.query(models.Lobby)
    if include_users:
        query = query.options(joinedload(models.Lobby.users))
    if include_host:
        query = query.options(joinedload(models.Lobby.host))
    return query.filter(models.Lobby.id == lobby_id).first()

def get_lobbies(db: Session, skip: int = 0, limit: int = 100) -> List[models.Lobby]:
    return db.query(models.Lobby).offset(skip).limit(limit).all()

def update_lobby(db: Session, lobby_id: str, lobby_update: schema.LobbyUpdate) -> Optional[models.Lobby]:
    db_lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if db_lobby:
        for key, value in lobby_update.dict(exclude_unset=True).items():
            setattr(db_lobby, key, value)
        db.commit()
        db.refresh(db_lobby)
    return db_lobby

def delete_lobby(db: Session, lobby_id: str) -> bool:
    db_lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if db_lobby:
        db.delete(db_lobby)
        db.commit()
        return True
    return False

def change_lobby_status(db: Session, lobby_id: str, new_status: str) -> Optional[models.Lobby]:
    db_lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    if db_lobby:
        db_lobby.status = new_status
        db.commit()
        db.refresh(db_lobby)
        return db_lobby
    return None

def add_user_to_lobby(db: Session, lobby_id: str, user_id: str) -> Optional[models.Lobby]:
    db_lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_lobby and db_user:
        db_lobby.users.append(db_user)
        db.commit()
        db.refresh(db_lobby)
        return db_lobby
    return None

def remove_user_from_lobby(db: Session, lobby_id: str, user_id: str) -> Optional[models.Lobby]:
    db_lobby = db.query(models.Lobby).filter(models.Lobby.id == lobby_id).first()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_lobby and db_user:
        db_lobby.users.remove(db_user)
        db.commit()
        db.refresh(db_lobby)
        return db_lobby
    return None

def get_lobbies_by_host(db: Session, host_id: str, skip: int = 0, limit: int = 100) -> List[models.Lobby]:
    return db.query(models.Lobby).filter(models.Lobby.host_id == host_id).offset(skip).limit(limit).all()

