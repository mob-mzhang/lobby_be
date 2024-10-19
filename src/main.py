# main.py

from fastapi import FastAPI, Depends, HTTPException
from .routes import router
from .database import engine, get_db
from . import models, schemas
from .crud import users_crud, events_crud, users_events_crud  # Update this line
import logging
import uuid
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from pydantic import ValidationError
import random
from fastapi.middleware.cors import CORSMiddleware

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Keep the test endpoint in main.py for now
@app.post("/test/create-event", response_model=schemas.Event)
@app.get("/test/create-event", response_model=schemas.Event)
def test_create_event(
    db: Session = Depends(get_db)
):
    # Create a test user
    test_user = schemas.User(
        id=str(uuid.uuid4()),
        username=f"testuser_{uuid.uuid4().hex[:8]}",
        phone_number=f"(555) 000-{str(random.randint(1111,9999))}",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db_user = users_crud.create_user(db, test_user)

    # Create the event with hardcoded sample data
    try:
        event_data = {
            'id': str(uuid.uuid4()),
            'name': 'Sample Event',
            'description': 'This is a sample event for testing purposes',
            'date': datetime.utcnow() + timedelta(days=7),  # Event set to 7 days from now
            'host_id': db_user.id
        }
        
        validated_event = schemas.Event(**event_data)
        db_event = events_crud.create_event(db, validated_event)
        
        # Add the host as a participant
        users_events_crud.add_user_to_event(db, user_id=db_user.id, event_id=db_event.id)
        
        return db_event
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
