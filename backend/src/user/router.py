from fastapi import APIRouter, Request, Depends, HTTPException, status
from typing import Any
from sqlmodel import Session

from conf.db import get_session
from middleware import auth
from common import security
from user import service
from user.schema import UserCreate, UserLogin, UserResponse, UserUpdate, UserRank
from user.model import User
from sqlmodel import select, desc
from typing import List

router = APIRouter(prefix="/api/v1/user", tags=["user"])

@auth.exempt
@router.get("/rank", response_model=List[UserRank])
def get_user_ranking(session: Session = Depends(get_session)):
    users = session.exec(select(User).order_by(desc(User.score), User.last_answer_time)).all()
    rank_list = []
    for i, user in enumerate(users):
        rank_list.append(UserRank(
            rank=i+1,
            username=user.username,
            score=user.score,
            last_answer_time=user.last_answer_time
        ))
    return rank_list


@auth.exempt
@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate,
    session: Session = Depends(get_session)
):
    return service.create_user(session, user_in)

@auth.exempt
@router.post("/login")
async def login(
    user_in: UserLogin,
    session: Session = Depends(get_session)
):
    user = service.authenticate(session, user_in.username, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    request: Request,
    session: Session = Depends(get_session)
):
    user_id = auth.get_current_user_id(request)
    return service.get_user_profile(session, user_id)

@router.patch("/me", response_model=UserResponse)
async def update_user_me(
    request: Request,
    user_in: UserUpdate,
    session: Session = Depends(get_session)
):
    user_id = auth.get_current_user_id(request)
    return service.update_user_profile(session, user_id, user_in)

@router.delete("/me")
async def delete_user_me(
    request: Request,
    session: Session = Depends(get_session)
):
    user_id = auth.get_current_user_id(request)
    service.delete_user(session, user_id)
    return {"message": "User deleted successfully"}
