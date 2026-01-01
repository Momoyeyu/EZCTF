import pytest
from fastapi.testclient import TestClient
from main import app
from user import service
from user.model import User
from common import security
import middleware.auth
# Import Team model to resolve relationship during User instantiation
from team.model import Team

client = TestClient(app)

def test_register_user(monkeypatch):
    def mock_create_user(session, user_in):
        return User(id=1, username=user_in.username, email=user_in.email, hashed_password="hashed")

    monkeypatch.setattr(service, "create_user", mock_create_user)
    
    response = client.post(
        "/api/v1/user/register",
        json={"username": "testuser", "email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_login_user(monkeypatch):
    def mock_authenticate(session, username, password):
        return User(id=1, username=username, hashed_password="hashed")
        
    def mock_create_access_token(subject):
        return "fake-token"

    monkeypatch.setattr(service, "authenticate", mock_authenticate)
    # We need to mock create_access_token where it is imported in the router or used
    # Assuming the router uses security.create_access_token
    from common import security
    monkeypatch.setattr(security, "create_access_token", mock_create_access_token)
    
    response = client.post(
        "/api/v1/user/login",
        json={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_get_me_unauthorized():
    response = client.get("/api/v1/user/me")
    assert response.status_code == 401

def test_get_me_authorized(monkeypatch):
    # Mock token verification in middleware
    def mock_verify_token(token):
        return {"sub": "1"}
    # Patch where it is used
    monkeypatch.setattr(middleware.auth, "verify_token", mock_verify_token)
    
    # Mock get user profile
    def mock_get_user_profile(session, user_id):
        return User(id=1, username="testuser", email="test@example.com", hashed_password="x")
    monkeypatch.setattr(service, "get_user_profile", mock_get_user_profile)
    
    response = client.get("/api/v1/user/me", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_delete_me_authorized(monkeypatch):
    # Mock token verification in middleware
    def mock_verify_token(token):
        return {"sub": "1"}
    monkeypatch.setattr(middleware.auth, "verify_token", mock_verify_token)
    
    # Mock delete user service
    deleted_ids = []
    def mock_delete_user(session, user_id):
        deleted_ids.append(user_id)
        return
        
    monkeypatch.setattr(service, "delete_user", mock_delete_user)
    
    response = client.delete("/api/v1/user/me", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 200
    assert deleted_ids == [1]
    assert response.json()["message"] == "User deleted successfully"
