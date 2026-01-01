from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from team.model import Team
    from task.model import Solved

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    email: Optional[str] = None
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    
    # Game related fields
    score: int = Field(default=0)
    last_answer_time: Optional[datetime] = None
    
    # Relationships
    team_id: Optional[int] = Field(default=None, sa_column=Column(Integer, ForeignKey("team.id", use_alter=True), nullable=True))
    team: Optional["Team"] = Relationship(back_populates="members", sa_relationship_kwargs={"foreign_keys": "User.team_id"})
    
    solved_records: List["Solved"] = Relationship(back_populates="user")
