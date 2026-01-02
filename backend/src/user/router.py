from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from conf.db import get_session
from middleware import auth
from common import erri
from user import service
from user.schema import UserCreate, UserLogin, UserResponse, UserUpdate, UserRank

router = APIRouter(prefix="/api/v1/user", tags=["user"])

@auth.exempt
@router.get("/rank", response_model=List[UserRank])
def get_user_ranking(session: Session = Depends(get_session)):
    return service.get_ranking(session)


@auth.exempt
@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate,
    session: Session = Depends(get_session)
):
    try:
        return service.create_user(session, user_in)
    except erri.BusinessError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@auth.exempt
@router.post("/login")
async def login(
    user_in: UserLogin,
    session: Session = Depends(get_session)
):
    try:
        access_token = service.login_user(session, user_in.username, user_in.password)
        return {"access_token": access_token, "token_type": "bearer"}
    except erri.BusinessError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    request: Request,
    session: Session = Depends(get_session)
):
    try:
        user_id = auth.get_current_user_id(request)
        return service.get_user_profile(session, user_id)
    except erri.BusinessError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/me", response_model=UserResponse)
async def update_user_me(
    request: Request,
    user_in: UserUpdate,
    session: Session = Depends(get_session)
):
    try:
        user_id = auth.get_current_user_id(request)
        return service.update_user_profile(session, user_id, user_in)
    except erri.BusinessError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

@router.post("/me/delete")
async def delete_user_me(
    request: Request,
    session: Session = Depends(get_session)
):
    try:
        user_id = auth.get_current_user_id(request)
        service.delete_user(session, user_id)
        return {"message": "User deleted successfully"}
    except erri.BusinessError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
