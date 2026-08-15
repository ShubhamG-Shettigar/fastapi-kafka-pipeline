from datetime import datetime
from typing import Any
from pydantic import BaseModel

class UserSignup(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    name: str
    surname: str

class MessageResponse(BaseModel):
    message: str

class EventEnvelope(BaseModel):
    event_id: str
    event_type: str
    event_version: int
    timestamp: datetime
    source: str
    payload: dict[str, Any]