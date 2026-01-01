from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TeamBase(BaseModel):
    team_name: str
    description: Optional[str] = None
    allow_join: bool = True

class TeamCreate(TeamBase):
    pass

class TeamUpdate(BaseModel):
    team_name: Optional[str] = None
    description: Optional[str] = None
    allow_join: Optional[bool] = None

class TeamRead(TeamBase):
    id: int
    leader_id: int
    score: int
    member_count: int = 1
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class TeamDetail(TeamRead):
    member_count: int
    rank: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class JoinTeamRequest(BaseModel):
    team_name: str

class TeamRank(BaseModel):
    rank: int
    team_id: int
    team_name: str
    member_count: int
    score: int

class KickMemberRequest(BaseModel):
    username: str

class ChangeLeaderRequest(BaseModel):
    username: str
