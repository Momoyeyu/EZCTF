from fastapi import Depends, Request
from sqlmodel import Session

from conf.db import get_session
from middleware.auth import get_current_user_id
from user.model import User
from common import erri

def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
) -> User:
    user_id = get_current_user_id(request)
    user = session.get(User, user_id)
    if not user:
        raise erri.not_found("User not found")
    return user

def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_superuser:
        raise erri.forbidden("Not enough privileges")
    return current_user
