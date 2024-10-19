from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src import schema
from src.crud import lobbys_crud
from src.database import get_db
from typing import List

router = APIRouter()

@router.post("/lobbies/", response_model=schema.Lobby)
def create_lobby(lobby: schema.LobbyCreate, host_id: str, db: Session = Depends(get_db)):
    return lobbys_crud.create_lobby(db=db, lobby=lobby, host_id=host_id)

@router.get("/lobbies/{lobby_id}", response_model=schema.Lobby)
def read_lobby(lobby_id: str, include_users: bool = False, include_host: bool = False, db: Session = Depends(get_db)):
    db_lobby = lobbys_crud.get_lobby(db, lobby_id=lobby_id, include_users=include_users, include_host=include_host)
    if db_lobby is None:
        raise HTTPException(status_code=404, detail="Lobby not found")
    return db_lobby

@router.get("/lobbies/", response_model=List[schema.Lobby])
def read_lobbies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lobbies = lobbys_crud.get_lobbies(db, skip=skip, limit=limit)
    return lobbies

@router.put("/lobbies/{lobby_id}", response_model=schema.Lobby)
def update_lobby(lobby_id: str, lobby: schema.LobbyUpdate, db: Session = Depends(get_db)):
    db_lobby = lobbys_crud.update_lobby(db, lobby_id=lobby_id, lobby_update=lobby)
    if db_lobby is None:
        raise HTTPException(status_code=404, detail="Lobby not found")
    return db_lobby

@router.delete("/lobbies/{lobby_id}", response_model=bool)
def delete_lobby(lobby_id: str, db: Session = Depends(get_db)):
    success = lobbys_crud.delete_lobby(db, lobby_id=lobby_id)
    if not success:
        raise HTTPException(status_code=404, detail="Lobby not found")
    return success

@router.put("/lobbies/{lobby_id}/status", response_model=schema.Lobby)
def change_lobby_status(lobby_id: str, new_status: str, db: Session = Depends(get_db)):
    db_lobby = lobbys_crud.change_lobby_status(db, lobby_id=lobby_id, new_status=new_status)
    if db_lobby is None:
        raise HTTPException(status_code=404, detail="Lobby not found")
    return db_lobby

@router.post("/lobbies/{lobby_id}/users/{user_id}", response_model=schema.Lobby)
def add_user_to_lobby(lobby_id: str, user_id: str, db: Session = Depends(get_db)):
    db_lobby = lobbys_crud.add_user_to_lobby(db, lobby_id=lobby_id, user_id=user_id)
    if db_lobby is None:
        raise HTTPException(status_code=400, detail="Unable to add user to lobby")
    return db_lobby

@router.delete("/lobbies/{lobby_id}/users/{user_id}", response_model=schema.Lobby)
def remove_user_from_lobby(lobby_id: str, user_id: str, db: Session = Depends(get_db)):
    db_lobby = lobbys_crud.remove_user_from_lobby(db, lobby_id=lobby_id, user_id=user_id)
    if db_lobby is None:
        raise HTTPException(status_code=400, detail="Unable to remove user from lobby")
    return db_lobby

@router.get("/lobbies/host/{host_id}", response_model=List[schema.Lobby])
def read_lobbies_by_host(host_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    lobbies = lobbys_crud.get_lobbies_by_host(db, host_id=host_id, skip=skip, limit=limit)
    return lobbies

