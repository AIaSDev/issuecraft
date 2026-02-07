"""Integration tests for the FastAPI application."""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.frameworks.persistence.models import Base

# Use in-memory SQLite for integration tests
TEST_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")


@pytest.fixture
def test_db():
    """Create a fresh database for each test."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client(test_db):
    """Create a test client with database override."""
    # Import app here to avoid early initialization
    from app.frameworks.web.app import create_app
    
    app = create_app()
    
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_issue(client):
    """Test creating an issue via API."""
    issue_data = {
        "title": "Test Issue",
        "body": "Test body"
    }
    
    response = client.post("/issues", json=issue_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Test Issue"
    assert data["body"] == "Test body"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_issue_without_body(client):
    """Test creating an issue without body."""
    issue_data = {
        "title": "Test Issue"
    }
    
    response = client.post("/issues", json=issue_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Test Issue"
    assert data["body"] is None


def test_create_issue_with_empty_title(client):
    """Test creating an issue with empty title."""
    issue_data = {
        "title": "",
        "body": "Test body"
    }
    
    response = client.post("/issues", json=issue_data)
    assert response.status_code == 400


def test_list_issues_empty(client):
    """Test listing issues when database is empty."""
    response = client.get("/issues")
    assert response.status_code == 200
    assert response.json() == []


def test_list_issues(client):
    """Test listing issues after creating some."""
    # Create issues
    issue1 = {"title": "Issue 1", "body": "Body 1"}
    issue2 = {"title": "Issue 2", "body": "Body 2"}
    
    client.post("/issues", json=issue1)
    client.post("/issues", json=issue2)
    
    # List issues
    response = client.get("/issues")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Issue 1"
    assert data[1]["title"] == "Issue 2"


def test_get_issue(client):
    """Test getting a specific issue."""
    # Create an issue
    issue_data = {"title": "Test Issue", "body": "Test body"}
    create_response = client.post("/issues", json=issue_data)
    issue_id = create_response.json()["id"]
    
    # Get the issue
    response = client.get(f"/issues/{issue_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == issue_id
    assert data["title"] == "Test Issue"
    assert data["body"] == "Test body"


def test_get_issue_not_found(client):
    """Test getting a non-existent issue."""
    response = client.get("/issues/999")
    assert response.status_code == 404
