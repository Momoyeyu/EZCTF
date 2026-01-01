from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from user.model import User

class Team(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    team_name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    member_count: int = Field(default=1)
    allow_join: bool = Field(default=True)
    score: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    leader_id: int = Field(foreign_key="user.id")
    
    # Relationships
    # We use string forward references to avoid circular imports at runtime
    members: List["User"] = Relationship(back_populates="team", sa_relationship_kwargs={"foreign_keys": "User.team_id"})
    
    # Optional: Relationship to the leader
    # leader: "User" = Relationship(sa_relationship_kwargs={"foreign_keys": "Team.leader_id"})
