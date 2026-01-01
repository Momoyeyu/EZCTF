import pytest
from sqlmodel import Session
from user.model import User
from common.security import create_access_token, get_password_hash

def create_test_user(session: Session, username: str = "testuser") -> User:
    user = User(
        username=username,
        hashed_password=get_password_hash("password"),
        email=f"{username}@example.com",
        score=0
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_auth_headers(user: User) -> dict:
    token = create_access_token(user.id)
    return {"Authorization": f"Bearer {token}"}

def test_create_team(client, session: Session):
    user = create_test_user(session, "team_creator")
    headers = get_auth_headers(user)
    
    response = client.post(
        "/api/v1/team/",
        json={"team_name": "Test Team", "allow_join": True},
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["team_name"] == "Test Team"
    assert data["leader_id"] == user.id
    assert data["member_count"] == 1
    
    # Verify user's team_id is updated
    session.refresh(user)
    assert user.team_id == data["id"]

def test_create_team_duplicate_name(client, session: Session):
    user1 = create_test_user(session, "user1")
    user2 = create_test_user(session, "user2")
    
    client.post(
        "/api/v1/team/",
        json={"team_name": "Unique Team"},
        headers=get_auth_headers(user1)
    )
    
    response = client.post(
        "/api/v1/team/",
        json={"team_name": "Unique Team"},
        headers=get_auth_headers(user2)
    )
    
    assert response.status_code == 400
    assert "Team name already exists" in response.json()["detail"]

def test_search_teams(client, session: Session):
    user = create_test_user(session, "searcher")
    
    # Create some teams directly in DB or via client
    # Using client to ensure side effects (user update) happen if we cared, 
    # but here we just need teams exist.
    # Since creating team via API requires a user without team, let's create users.
    
    u1 = create_test_user(session, "u1")
    client.post("/api/v1/team/", json={"team_name": "Alpha Team"}, headers=get_auth_headers(u1))
    
    u2 = create_test_user(session, "u2")
    client.post("/api/v1/team/", json={"team_name": "Beta Team"}, headers=get_auth_headers(u2))
    
    headers = get_auth_headers(user)
    
    # Search all
    response = client.get("/api/v1/team/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 2
    
    # Search keyword
    response = client.get("/api/v1/team/?keyword=Alpha", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["team_name"] == "Alpha Team"

def test_join_team(client, session: Session):
    leader = create_test_user(session, "leader")
    create_res = client.post("/api/v1/team/", json={"team_name": "Joinable Team"}, headers=get_auth_headers(leader))
    team_id = create_res.json()["id"]

    joiner = create_test_user(session, "joiner")
    headers = get_auth_headers(joiner)
    
    response = client.post(
        "/api/v1/team/join",
        json={"team_name": "Joinable Team"},
        headers=headers
    )
    
    assert response.status_code == 200
    # join_team returns a message, not team object
    assert response.json()["message"] == "Successfully joined team"
    
    # Verify member count via get_team
    get_res = client.get(f"/api/v1/team/{team_id}", headers=get_auth_headers(leader))
    assert get_res.json()["member_count"] == 2
    
    session.refresh(joiner)
    assert joiner.team_id == team_id

def test_quit_team(client, session: Session):
    leader = create_test_user(session, "leader_quit")
    client.post("/api/v1/team/", json={"team_name": "Quit Team"}, headers=get_auth_headers(leader))
    
    member = create_test_user(session, "member_quit")
    client.post(
        "/api/v1/team/join",
        json={"team_name": "Quit Team"},
        headers=get_auth_headers(member)
    )
    
    # Member quits
    response = client.post("/api/v1/team/quit", headers=get_auth_headers(member))
    assert response.status_code == 200
    
    session.refresh(member)
    assert member.team_id is None
    
    # Check team member count
    response = client.get("/api/v1/team/?keyword=Quit Team", headers=get_auth_headers(leader))
    assert response.json()[0]["member_count"] == 1

def test_delete_team(client, session: Session):
    leader = create_test_user(session, "leader_del")
    create_res = client.post("/api/v1/team/", json={"team_name": "Del Team"}, headers=get_auth_headers(leader))
    team_id = create_res.json()["id"]
    
    # Add a member
    member = create_test_user(session, "member_del")
    client.post(
        "/api/v1/team/join",
        json={"team_name": "Del Team"},
        headers=get_auth_headers(member)
    )
    
    # Leader deletes team
    response = client.delete(f"/api/v1/team/{team_id}", headers=get_auth_headers(leader))
    assert response.status_code == 200
    
    # Verify team is gone
    get_res = client.get(f"/api/v1/team/{team_id}", headers=get_auth_headers(leader))
    assert get_res.status_code == 404
    
    # Verify member is free
    session.refresh(member)
    assert member.team_id is None
