# app/models.py

from sqlalchemy import Column, String, DateTime, ForeignKey, Table, Integer, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()

# Association table for the many-to-many relationship between users and lobbies
user_lobby = Table('user_lobby', Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('lobby_id', String, ForeignKey('lobbies.id'))
)

# New association table for the many-to-many relationship between users and parties
user_party = Table('user_party', Base.metadata,
    Column('user_id', String, ForeignKey('users.id')),
    Column('party_id', String, ForeignKey('parties.id'))
)

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    username = Column(String, index=True)
    phone_number = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    queue_status = Column(Boolean, default=False)

    friends = relationship("User", 
                           secondary="friends",
                           primaryjoin="User.id==Friend.user_id",
                           secondaryjoin="User.id==Friend.friend_id",
                           backref="friended_by")
    lobbies = relationship("Lobby", secondary=user_lobby, back_populates="users")
    hosted_lobbies = relationship("Lobby", back_populates="host")
    parties = relationship("Party", secondary=user_party, back_populates="users")

class Friend(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    friend_id = Column(String, ForeignKey('users.id'))

class Lobby(Base):
    __tablename__ = "lobbies"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    date = Column(DateTime)
    status = Column(String, index=True)
    host_id = Column(String, ForeignKey('users.id'))
    host = relationship("User", back_populates="hosted_lobbies")
    users = relationship("User", secondary=user_lobby, back_populates="lobbies")

class Party(Base):
    __tablename__ = "parties"

    id = Column(String, primary_key=True, index=True)
    status = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    queue_status = Column(Boolean, default=False)

    users = relationship("User", secondary=user_party, back_populates="parties")

class FriendCreate(BaseModel):
    # Fields for friend creation
    username: str
    # Add other fields as necessary
