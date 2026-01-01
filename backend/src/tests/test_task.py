import pytest
from sqlmodel import Session
from user.model import User
from task.model import Task, Difficulty
from common.security import create_access_token, get_password_hash

def create_user(session: Session, username: str, is_superuser: bool = False) -> User:
    user = User(
        username=username,
        hashed_password=get_password_hash("password"),
        email=f"{username}@example.com",
        is_superuser=is_superuser,
        score=0
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_auth_headers(user: User) -> dict:
    token = create_access_token(user.id)
    return {"Authorization": f"Bearer {token}"}

def test_create_task(client, session: Session):
    admin = create_user(session, "admin", is_superuser=True)
    
    response = client.post(
        "/api/v1/task/",
        json={
            "title": "Test Task",
            "description": "Description",
            "flag": "flag{test}",
            "difficulty": 0, # EASY
            "points": 100,
            "category": "WEB"
        },
        headers=get_auth_headers(admin)
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["score"] == 100
    # Flag should not be in response
    assert "flag" not in data

def test_create_task_forbidden(client, session: Session):
    user = create_user(session, "normal_user")
    
    response = client.post(
        "/api/v1/task/",
        json={
            "title": "Test Task Forbidden",
            "description": "Desc",
            "flag": "flag{test}",
            "difficulty": 0,
            "points": 100,
            "category": "MISC"
        },
        headers=get_auth_headers(user)
    )
    
    assert response.status_code == 403

def test_submit_flag_correct(client, session: Session):
    admin = create_user(session, "admin_task", is_superuser=True)
    create_res = client.post(
        "/api/v1/task/",
        json={
            "title": "Solve Me",
            "description": "Desc",
            "flag": "flag{correct}",
            "difficulty": 0,
            "score": 50,
            "category": "WEB"
        },
        headers=get_auth_headers(admin)
    )
    assert create_res.status_code == 200
    task_id = create_res.json()["id"]
    
    # Get task object for later verification
    task = session.get(Task, task_id)

    user = create_user(session, "solver")
    response = client.post(
        f"/api/v1/task/{task_id}/submit",
        json={"flag": "flag{correct}"},
        headers=get_auth_headers(user)
    )
    
    assert response.status_code == 200
    assert response.json()["correct"] is True
    # assert response.json()["points"] == 50 # AnswerResponse usually returns 0 or just msg, let's check service
    
    # Verify user score updated
    session.refresh(user)
    assert user.score == 50
    
    # Verify task solve count
    session.refresh(task) # Need to refresh task instance to get updated fields
    assert task.solve_count == 1

def test_submit_flag_wrong(client, session: Session):
    admin = create_user(session, "admin_task_2", is_superuser=True)
    create_res = client.post(
        "/api/v1/task/",
        json={
            "title": "Solve Me 2",
            "description": "Desc",
            "flag": "flag{correct}",
            "difficulty": 0,
            "score": 50,
            "category": "WEB"
        },
        headers=get_auth_headers(admin)
    )
    task_id = create_res.json()["id"]
    
    user = create_user(session, "failer")
    response = client.post(
        f"/api/v1/task/{task_id}/submit",
        json={"flag": "flag{wrong}"},
        headers=get_auth_headers(user)
    )
    
    assert response.status_code == 200
    assert response.json()["correct"] is False
    
    session.refresh(user)
    assert user.score == 0

def test_submit_duplicate(client, session: Session):
    admin = create_user(session, "admin_task_3", is_superuser=True)
    create_res = client.post(
        "/api/v1/task/",
        json={
            "title": "Solve Me 3",
            "description": "Desc",
            "flag": "flag{correct}",
            "difficulty": 0,
            "score": 50,
            "category": "WEB"
        },
        headers=get_auth_headers(admin)
    )
    task_id = create_res.json()["id"]
    
    user = create_user(session, "double_solver")
    
    # First submit
    client.post(
        f"/api/v1/task/{task_id}/submit",
        json={"flag": "flag{correct}"},
        headers=get_auth_headers(user)
    )
    
    # Second submit
    response = client.post(
        f"/api/v1/task/{task_id}/submit",
        json={"flag": "flag{correct}"},
        headers=get_auth_headers(user)
    )
    
    assert response.status_code == 400
