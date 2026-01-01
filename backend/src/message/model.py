from enum import IntEnum
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class MessageType(IntEnum):
    OTHER = 0
    CHAT = 1
    SYSTEM = 2
    APPLICATION = 3
    INVITATION = 4
    KICKOUT = 5

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    receiver_id: int = Field(foreign_key="user.id")
    origin_id: int = Field(foreign_key="user.id")
    msg: str
    checked: bool = Field(default=False)
    msg_type: MessageType
    create_time: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
