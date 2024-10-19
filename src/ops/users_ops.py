from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from src import schema
from src.crud import users_crud
from src.database import get_db
from typing import List, Optional

router = APIRouter()

@router.post("/users/", response_model=schema.User)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = users_crud.get_user_by_phone(db, phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return users_crud.create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=schema.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = users_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/users/phone/{phone_number}", response_model=Optional[schema.User])
def read_user_by_phone(phone_number: str, db: Session = Depends(get_db)):
    db_user = users_crud.get_user_by_phone(db, phone_number=phone_number)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user has not finished signup process")
    return db_user

@router.get("/users/", response_model=List[schema.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = users_crud.get_users(db, skip=skip, limit=limit)
    return users

@router.put("/users/{user_id}", response_model=schema.User)
def update_user(user_id: str, user: schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = users_crud.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/users/{user_id}/friends", response_model=schema.Friend)
def add_friend(user_id: str, friend: schema.FriendCreate, db: Session = Depends(get_db)):
    db_friend = users_crud.add_friend(db, user_id=user_id, friend_username=friend.username)
    if db_friend is None:
        raise HTTPException(status_code=400, detail="Unable to add friend")
    return db_friend

@router.post("/users/{user_id}/lobbies/{lobby_id}", response_model=schema.Lobby)
def join_lobby(user_id: str, lobby_id: str, db: Session = Depends(get_db)):
    db_lobby = users_crud.join_lobby(db, user_id=user_id, lobby_id=lobby_id)
    if db_lobby is None:
        raise HTTPException(status_code=400, detail="Unable to join lobby")
    return db_lobby

@router.put("/users/{user_id}/queue_status", response_model=schema.User)
def set_queue_status(user_id: str, active: bool, db: Session = Depends(get_db)):
    db_user = users_crud.set_queue_status(db, user_id=user_id, active=active)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

