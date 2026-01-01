import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from conf.db import get_session
import conf.db
from user.model import User
from team.model import Team

# Use in-memory SQLite for testing
sqlite_url = "sqlite://" 

engine = create_engine(
    sqlite_url, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

@pytest.fixture(name="session")
def session_fixture():
    # Patch the engine in conf.db so direct usages use our test engine
    # We need to patch it before create_all probably, or create_all on our engine
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    with Session(engine) as session:
        yield session
    
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")
def client_fixture(session: Session, monkeypatch):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    
    # Also patch the global engine used in services that don't use dependency injection yet
    monkeypatch.setattr(conf.db, "engine", engine)
    
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
