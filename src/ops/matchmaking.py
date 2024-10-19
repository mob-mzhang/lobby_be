from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from src import schema, models
from src.crud import users_crud, lobbys_crud
from src.database import get_db
from typing import List
import random
from datetime import datetime
import asyncio

router = APIRouter()

async def check_and_start_matchmaking(db: Session):
    while True:
        active_users = users_crud.get_users_by_queue_status(db, active=True)
        if len(active_users) >= 4:
            perform_matchmaking(db)
        await asyncio.sleep(10)  # Check every 10 seconds

def perform_matchmaking(db: Session):
    # Get all users with active queue status
    active_users = users_crud.get_users_by_queue_status(db, active=True)
    
    # Shuffle the users to ensure random matching
    random.shuffle(active_users)
    
    # Match users in groups of 4
    for i in range(0, len(active_users), 4):
        group = active_users[i:i+4]
        
        # If we have a full group of 4 users
        if len(group) == 4:
            # Create a new lobby
            lobby = schema.LobbyCreate(
                name=f"Matched Lobby {random.randint(1000, 9999)}",
                description="Automatically created lobby from matchmaking",
                date=datetime.utcnow()
            )
            db_lobby = lobbys_crud.create_lobby(db, lobby, host_id=group[0].id)
            
            # Add users to the lobby and update their queue status
            for user in group:
                lobbys_crud.add_user_to_lobby(db, db_lobby.id, user.id)
                users_crud.set_queue_status(db, user.id, False)
            
            # Set the lobby status to active
            lobbys_crud.change_lobby_status(db, db_lobby.id, "active")

@router.on_event("startup")
async def start_background_tasks():
    asyncio.create_task(check_and_start_matchmaking(next(get_db())))

@router.get("/matchmaking/active-users", response_model=List[schema.User])
def get_active_users(db: Session = Depends(get_db)):
    return users_crud.get_users_by_queue_status(db, active=True)

