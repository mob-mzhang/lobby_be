# app/schemas.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    username: str
    phone_number: str

class UserLogin(BaseModel):
    phone_number: str

class User(BaseModel):
    id: str
    username: str
    phone_number: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Friend(BaseModel):
    id: str
    user_id: str
    friend_id: str

    model_config = ConfigDict(from_attributes=True)

class Event(BaseModel):
    id: str
    name: str
    description: str
    date: datetime
    host_id: str

    model_config = ConfigDict(from_attributes=True)

class UserWithFriendsAndEvents(BaseModel):
    user: User
    friends: List[User]
    events: List[Event]

    model_config = ConfigDict(from_attributes=True)

# Add this new schema
class FriendCreate(BaseModel):
    friend_id: str

# ... rest of the code ...