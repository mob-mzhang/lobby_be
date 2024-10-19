from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    phone_number: str

class UserCreate(BaseModel):
    username: str
    phone_number: str

class UserVerify(BaseModel):
    phone: str
    token: str

class User(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    queue_status: bool

    class Config:
        from_attributes = True

class FriendBase(BaseModel):
    user_id: str
    friend_id: str

class FriendCreate(BaseModel):
    username: str

class Friend(FriendBase):
    id: int

    class Config:
        from_attributes = True

class LobbyBase(BaseModel):
    name: str
    description: str
    date: datetime

class LobbyCreate(LobbyBase):
    pass

class Lobby(LobbyBase):
    id: str
    host_id: str
    users: List[User] = []

    class Config:
        from_attributes = True

class PartyBase(BaseModel):
    status: str

class PartyCreate(PartyBase):
    pass

class Party(PartyBase):
    id: str
    created_at: datetime
    queue_status: bool
    users: List[User] = []

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    phone_number: Optional[str] = None
    queue_status: Optional[bool] = None

class LobbyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

class PartyUpdate(BaseModel):
    status: Optional[str] = None
    queue_status: Optional[bool] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int

class UserWithToken(User):
    access_token: str
    refresh_token: str
