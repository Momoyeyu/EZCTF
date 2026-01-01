from typing import Optional
from sqlmodel import Session, select
from user.model import User
from user.schema import UserCreate, UserResponse, UserUpdate
from common import security, erri
from datetime import datetime, timezone

def get_by_username(session: Session, username: str) -> Optional[User]:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()

def get_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def create_user(session: Session, user_create: UserCreate) -> User:
    if get_by_username(session, user_create.username):
        raise erri.bad_request("Username already registered")
    
    if user_create.email and get_by_email(session, user_create.email):
        raise erri.bad_request("Email already registered")
        
    db_user = User.model_validate(user_create, update={"hashed_password": security.get_password_hash(user_create.password)})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def authenticate(session: Session, username: str, password: str) -> Optional[User]:
    user = get_by_username(session, username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

def get_user_profile(session: Session, user_id: int) -> UserResponse:
    user = session.get(User, user_id)
    if not user:
        raise erri.not_found("User not found")
    
    team_name = user.team.team_name if user.team else None
    is_leader = (user.team and user.team.leader_id == user.id) or False
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        score=user.score,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        team_id=user.team_id,
        team_name=team_name,
        is_leader=is_leader
    )

def update_user_profile(session: Session, user_id: int, user_update: UserUpdate) -> User:
    user = session.get(User, user_id)
    if not user:
        raise erri.not_found("User not found")
        
    if user_update.email is not None:
        user.email = user_update.email
    # Add other fields as needed
    if user_update.password is not None:
        user.hashed_password = security.get_password_hash(user_update.password)
        
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise erri.not_found("User not found")
    session.delete(user)
    session.commit()
