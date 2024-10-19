###event endpoints and operations

from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List
from ..crud import users_crud, events_crud, users_events_crud
from .. import schemas
from ..database import get_db
from ..utils import format_phone_number
from pydantic import ValidationError

router = APIRouter()

@router.get("/{user_id}/events", response_model=List[schemas.Event])
def get_user_events(user_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = users_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    events = users_events_crud.get_user_events(db, user_id=user_id, skip=skip, limit=limit)
    return events

@router.get("/{user_id}/available-events", response_model=List[schemas.Event])
def get_available_events(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    db_user = users_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    available_events = users_events_crud.get_available_events_for_user(db, user_id=user_id, skip=skip, limit=limit)
    return [schemas.Event.model_validate(event) for event in available_events]

@router.get("/phone/{phone_number}/available-events", response_model=List[schemas.Event])
def get_available_events_by_phone(
    phone_number: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    formatted_phone = format_phone_number(phone_number)
    db_user = users_crud.get_user_by_phone(db, phone_number=formatted_phone)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    available_events = users_events_crud.get_available_events_for_user(db, user_id=db_user.id, skip=skip, limit=limit)
    return [schemas.Event.model_validate(event) for event in available_events]

@router.post("/{user_id}/createevent", response_model=schemas.Event)
def create_event_for_user(
    user_id: str,
    event: schemas.Event = Body(...),
    db: Session = Depends(get_db)
):
    db_user = users_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        event_data = event.model_dump()
        event_data['host_id'] = user_id
        
        validated_event = schemas.Event(**event_data)
        
        db_event = events_crud.create_event(db, validated_event)
        
        users_events_crud.add_user_to_event(db, user_id=user_id, event_id=db_event.id)
        
        return db_event
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.post("/{user_id}/join/{event_id}", response_model=schemas.Event)
def join_event(
    user_id: str,
    event_id: str,
    db: Session = Depends(get_db)
):
    # Check if user exists
    db_user = users_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if event exists
    db_event = events_crud.get_event(db, event_id=event_id)
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if user is already in the event
    if users_events_crud.is_user_in_event(db, user_id=user_id, event_id=event_id):
        raise HTTPException(status_code=400, detail="User is already in this event")
    
    # Add user to event
    users_events_crud.add_user_to_event(db, user_id=user_id, event_id=event_id)
    
    # Refresh the event data
    updated_event = events_crud.get_event(db, event_id=event_id)
    
    return updated_event