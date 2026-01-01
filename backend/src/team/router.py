from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session

from conf.db import get_session
from middleware import auth
from user.model import User
from user.deps import get_current_user
from team.schema import TeamCreate, TeamRead, TeamDetail, TeamUpdate, JoinTeamRequest, TeamRank, KickMemberRequest, ChangeLeaderRequest
from team import service as team_service
from team.model import Team
from sqlmodel import select, desc
from common import erri

router = APIRouter(prefix="/api/v1/team", tags=["team"])

@auth.exempt
@router.get("/rank", response_model=List[TeamRank])
def get_team_ranking(session: Session = Depends(get_session)):
    teams = session.exec(select(Team).order_by(desc(Team.score), Team.created_at)).all()
    rank_list = []
    for i, team in enumerate(teams):
        rank_list.append(TeamRank(
            rank=i+1,
            team_id=team.id,
            team_name=team.team_name,
            member_count=team.member_count,
            score=team.score
        ))
    return rank_list

@router.get("/name/{team_name}", response_model=TeamDetail)
def get_team_by_name(
    team_name: str,
    session: Session = Depends(get_session)
):
    return team_service.get_team_by_name(session, team_name)

@router.post("/kick")
def kick_member(
    req: KickMemberRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if not current_user.team_id:
        raise erri.bad_request("You are not in a team")
    team_service.kick_member(session, current_user.team_id, req.username, current_user)
    return {"status": "success"}

@router.post("/change_leader")
def change_leader(
    req: ChangeLeaderRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if not current_user.team_id:
        raise erri.bad_request("You are not in a team")
    team_service.change_leader(session, current_user.team_id, req.username, current_user)
    return {"status": "success"}

@router.post("/", response_model=TeamRead)
def create_team(
    team_create: TeamCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return team_service.create_team(session, team_create, current_user)

@router.get("/", response_model=List[TeamRead])
def get_teams(
    keyword: str = "",
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return team_service.get_teams(session, keyword=keyword if keyword else None)

@router.get("/{team_id}", response_model=TeamDetail)
def get_team(
    team_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return team_service.get_team_detail(session, team_id)

@router.post("/join")
def join_team(
    join_req: JoinTeamRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    team_service.join_team(session, join_req, current_user)
    return {"message": "Successfully joined team"}

@router.post("/quit")
def quit_team(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    team_service.quit_team(session, current_user)
    return {"message": "Successfully quit team"}

@router.patch("/{team_id}", response_model=TeamRead)
def update_team(
    team_id: int,
    team_update: TeamUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return team_service.update_team(session, team_id, team_update, current_user)

@router.delete("/{team_id}")
def delete_team(
    team_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    team_service.delete_team(session, team_id, current_user)
    return {"message": "Successfully deleted team"}
