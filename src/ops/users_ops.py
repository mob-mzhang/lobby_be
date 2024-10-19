# user endpoints and operations

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import logging
from ..crud import users_crud
from .. import schemas, models
from ..database import get_db
from ..utils import format_phone_number, generate_unique_id
from pydantic import ValidationError
from datetime import datetime
from supabase import create_client, Client

router = APIRouter()

logger = logging.getLogger(__name__)

# Supabase client initialization
supabase_url = "https://icwupqucbnxynldgqxaq.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imljd3VwcXVjYm54eW5sZGdxeGFxIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyODQzMTA4NiwiZXhwIjoyMDQ0MDA3MDg2fQ.Ao-QT5dCDUVRu9KBDowcNBgUFFmsUKiQzSLAYq8RgrY"
supabase: Client = create_client(supabase_url, supabase_key)


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = users_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/{user_id}/friends", response_model=List[schemas.User])
def get_user_friends(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = users_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Note: We need to add get_user_friends function to users_crud.py
    friend_relationships = users_crud.get_user_friends(
        db, user_id=user_id, skip=skip, limit=limit)
    friend_ids = [fr.friend_id for fr in friend_relationships]
    friends = [users_crud.get_user(db, user_id=friend_id)
               for friend_id in friend_ids]
    return [friend for friend in friends if friend is not None]


@router.get("/phone/{phone_number}", response_model=schemas.UserWithFriendsAndEvents)
def get_user_by_phone(phone_number: str, db: Session = Depends(get_db)):
    formatted_phone = format_phone_number(phone_number)
    db_user = users_crud.get_user_by_phone(db, phone_number=formatted_phone)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = schemas.User.from_orm(db_user)
    friends = [schemas.User.from_orm(friend) for friend in db_user.friends]
    events = [schemas.Event.from_orm(event) for event in db_user.events]

    return schemas.UserWithFriendsAndEvents(
        user=user,
        friends=friends,
        events=events
    )


@router.post("/{user_id}/friends", response_model=schemas.Friend)
def add_friend(
    user_id: str,
    friend: schemas.FriendCreate,
    db: Session = Depends(get_db)
):
    try:
        # Check if the user exists
        user = users_crud.get_user(db, user_id=user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the friend exists
        friend_user = users_crud.get_user(db, user_id=friend.friend_id)
        if friend_user is None:
            raise HTTPException(status_code=404, detail="Friend not found")

        # Check if the friendship already exists
        existing_friendship = db.query(models.Friend).filter(
            (models.Friend.user_id == user_id) & (
                models.Friend.friend_id == friend.friend_id)
        ).first()
        if existing_friendship:
            raise HTTPException(
                status_code=400, detail="Friendship already exists")

        # Create the friendship
        friendship = users_crud.create_friendship(
            db, user_id, friend.friend_id)
        return friendship

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate = Body(...), db: Session = Depends(get_db)):
    try:
        # Check if user with the same phone number already exists
        existing_user = users_crud.get_user_by_phone(
            db, phone_number=user.phone_number)
        if existing_user:
            raise HTTPException(
                status_code=400, detail="User with this phone number already exists")

        # Format phone number
        formatted_phone = format_phone_number(user.phone_number)

        # Create user in Supabase Auth
        supabase_user = supabase.auth.admin.create_user({
            "phone": formatted_phone,
            # Supabase requires an email, so we create a dummy one
            "email": f"{formatted_phone}@example.com",
            "password": generate_unique_id(),  # Generate a random password
            "email_confirm": True  # Auto-confirm the email
        })

        # Generate a unique ID for the user (use Supabase user ID)
        user_id = supabase_user.id

        # Get current timestamp
        current_time = datetime.utcnow()

        # Create user object
        new_user = schemas.User(
            id=user_id,
            username=user.username,
            phone_number=formatted_phone,
            created_at=current_time,
            updated_at=current_time
        )

        # Create user in the database
        created_user = users_crud.create_user(db, new_user)
        return created_user
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")
