from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Session, select, func
from team.model import Team
from team.schema import TeamCreate, TeamUpdate, TeamDetail, JoinTeamRequest
from user.model import User
from common import erri

def create_team(session: Session, team_create: TeamCreate, user: User) -> Team:
    # Check if user already in team
    if user.team_id:
        raise erri.bad_request("User is already in a team")
        
    # Check team name
    statement = select(Team).where(Team.team_name == team_create.team_name)
    if session.exec(statement).first():
        raise erri.bad_request("Team name already exists")
        
    db_team = Team(
        team_name=team_create.team_name,
        description=team_create.description,
        allow_join=team_create.allow_join,
        leader_id=user.id,
        created_at=datetime.now(timezone.utc)
    )
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    
    # Update user
    user.team_id = db_team.id
    session.add(user)
    session.commit()
    
    return db_team

def get_team(session: Session, team_id: int) -> Team:
    team = session.get(Team, team_id)
    if not team:
        raise erri.not_found("Team not found")
    return team

def get_teams(session: Session, offset: int = 0, limit: int = 100, keyword: Optional[str] = None) -> List[Team]:
    statement = select(Team)
    if keyword:
        statement = statement.where(Team.team_name.contains(keyword))
    statement = statement.offset(offset).limit(limit)
    return session.exec(statement).all()

def get_team_detail(session: Session, team_id: int) -> TeamDetail:
    team = get_team(session, team_id)
    
    # Calculate rank (mock implementation for now)
    rank = 1 
    
    return TeamDetail(
        id=team.id,
        team_name=team.team_name,
        description=team.description,
        allow_join=team.allow_join,
        leader_id=team.leader_id,
        score=team.score,
        created_at=team.created_at,
        member_count=len(team.members),
        rank=rank
    )

def update_team(session: Session, team_id: int, team_update: TeamUpdate, user: User) -> Team:
    db_team = get_team(session, team_id)
    
    # Check permission
    if db_team.leader_id != user.id and not user.is_superuser:
        raise erri.forbidden("Only team leader can update team info")
        
    team_data = team_update.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
        
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team

def delete_team(session: Session, team_id: int, user: User):
    db_team = get_team(session, team_id)
    
    # Check permission
    if db_team.leader_id != user.id and not user.is_superuser:
        raise erri.forbidden("Only team leader can dismiss team")
        
    # Remove all members from team
    for member in db_team.members:
        member.team_id = None
        session.add(member)
        
    session.delete(db_team)
    session.commit()

def join_team(session: Session, join_req: JoinTeamRequest, user: User):
    if user.team_id:
        raise erri.bad_request("User is already in a team")
        
    statement = select(Team).where(Team.team_name == join_req.team_name)
    team = session.exec(statement).first()
    if not team:
        raise erri.not_found("Team not found")
        
    if not team.allow_join:
        raise erri.forbidden("Team does not allow joining")
        
    user.team_id = team.id
    session.add(user)
    session.commit()
    
def quit_team(session: Session, user: User):
    if not user.team_id:
        raise erri.bad_request("User is not in a team")
        
    team = get_team(session, user.team_id)
    if team.leader_id == user.id:
        raise erri.bad_request("Leader cannot quit team, must dismiss it")
        
    user.team_id = None
    session.add(user)
    session.commit()

def kick_member(session: Session, team_id: int, member_username: str, user: User):
    team = get_team(session, team_id)
    if team.leader_id != user.id and not user.is_superuser:
        raise erri.forbidden("Only leader can kick members")
    
    statement = select(User).where(User.username == member_username)
    member = session.exec(statement).first()
    if not member:
        raise erri.not_found("User not found")
        
    if member.team_id != team.id:
        raise erri.bad_request("User is not in this team")
        
    if member.id == user.id:
        raise erri.bad_request("Cannot kick yourself")
        
    member.team_id = None
    session.add(member)
    session.commit()

def change_leader(session: Session, team_id: int, new_leader_username: str, user: User):
    team = get_team(session, team_id)
    if team.leader_id != user.id and not user.is_superuser:
        raise erri.forbidden("Only leader can change leader")
        
    statement = select(User).where(User.username == new_leader_username)
    new_leader = session.exec(statement).first()
    if not new_leader:
        raise erri.not_found("User not found")
        
    if new_leader.team_id != team.id:
        raise erri.bad_request("New leader must be a member of the team")
        
    team.leader_id = new_leader.id
    session.add(team)
    session.commit()

def get_team_by_name(session: Session, team_name: str) -> TeamDetail:
    statement = select(Team).where(Team.team_name == team_name)
    team = session.exec(statement).first()
    if not team:
        raise erri.not_found("Team not found")
    
    # Calculate rank (mock)
    rank = 1
    
    return TeamDetail(
        id=team.id,
        team_name=team.team_name,
        description=team.description,
        allow_join=team.allow_join,
        leader_id=team.leader_id,
        score=team.score,
        created_at=team.created_at,
        member_count=len(team.members),
        rank=rank
    )
