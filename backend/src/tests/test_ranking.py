from sqlmodel import Session
from fastapi.testclient import TestClient
from user.model import User
from team.model import Team
from datetime import datetime, timezone, timedelta

def test_user_ranking(client: TestClient, session: Session):
    # Create users with different scores
    user1 = User(username="user1", hashed_password="pw", score=100, last_answer_time=datetime.now(timezone.utc) - timedelta(hours=1))
    user2 = User(username="user2", hashed_password="pw", score=200, last_answer_time=datetime.now(timezone.utc))
    user3 = User(username="user3", hashed_password="pw", score=100, last_answer_time=datetime.now(timezone.utc) - timedelta(hours=2))
    
    session.add(user1)
    session.add(user2)
    session.add(user3)
    session.commit()
    
    response = client.get("/api/v1/user/rank")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) >= 3
    # user2 should be first (highest score)
    assert data[0]["username"] == "user2"
    assert data[0]["rank"] == 1
    
    # user3 should be second (same score as user1, but answered earlier - wait, logic is score DESC, time ASC usually.
    # Let's check router logic: order_by(desc(User.score), User.last_answer_time)
    # user3 time is T-2h, user1 time is T-1h. T-2h < T-1h. So user3 should be before user1.
    
    assert data[1]["username"] == "user3"
    assert data[1]["rank"] == 2
    
    assert data[2]["username"] == "user1"
    assert data[2]["rank"] == 3

def test_team_ranking(client: TestClient, session: Session):
    # Create leader users
    leader1 = User(username="leader1", hashed_password="pw")
    leader2 = User(username="leader2", hashed_password="pw")
    session.add(leader1)
    session.add(leader2)
    session.commit()
    
    # Create teams
    team1 = Team(team_name="team1", leader_id=leader1.id, score=50, created_at=datetime.now(timezone.utc))
    team2 = Team(team_name="team2", leader_id=leader2.id, score=100, created_at=datetime.now(timezone.utc))
    
    session.add(team1)
    session.add(team2)
    session.commit()
    
    response = client.get("/api/v1/team/rank")
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) >= 2
    # team2 should be first
    assert data[0]["team_name"] == "team2"
    assert data[0]["rank"] == 1
    
    assert data[1]["team_name"] == "team1"
    assert data[1]["rank"] == 2
