from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    score: int = 0
    is_active: bool = True
    is_superuser: bool = False
    team_id: Optional[int] = None
    team_name: Optional[str] = None
    is_leader: bool = False
    
class UserUpdate(BaseModel):
    nickname: Optional[str] = None
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = None
    password: Optional[str] = None

class UserRank(BaseModel):
    rank: int
    username: str
    score: int
    last_answer_time: Optional[datetime] = None
