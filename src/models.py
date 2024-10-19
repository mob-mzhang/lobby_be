# app/models.py

from sqlalchemy import Column, String, DateTime, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()

# Association table for the many-to-many relationship between users and events
user_event = Table('user_event', Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('event_id', String, ForeignKey('events.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    phone_number = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    friends = relationship("User", 
                           secondary="friends",
                           primaryjoin="User.id==Friend.user_id",
                           secondaryjoin="User.id==Friend.friend_id",
                           backref="friended_by")
    events = relationship("Event", secondary=user_event, back_populates="users")
    hosted_events = relationship("Event", back_populates="host")

class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    friend_id = Column(String, ForeignKey('users.id'))

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    date = Column(DateTime)
    host_id = Column(String, ForeignKey('users.id'))
    host = relationship("User", back_populates="hosted_events")
    users = relationship("User", secondary=user_event, back_populates="events")

class FriendCreate(BaseModel):
    # Fields for friend creation
    username: str
    # Add other fields as necessary
