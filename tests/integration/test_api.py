"""Integration tests for the FastAPI application."""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import get_db
from src.frameworks.fastapi_app import app
from src.frameworks.models import Base

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create a test client with database override."""
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
        "description": "Test description",
        "status": "open"
    }
    
    response = client.post("/issues", json=issue_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Test Issue"
    assert data["description"] == "Test description"
    assert data["status"] == "open"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_issue_with_invalid_status(client):
    """Test creating an issue with invalid status."""
    issue_data = {
        "title": "Test Issue",
        "description": "Test description",
        "status": "invalid_status"
    }
    
    response = client.post("/issues", json=issue_data)
    assert response.status_code == 400


def test_create_issue_with_empty_title(client):
    """Test creating an issue with empty title."""
    issue_data = {
        "title": "",
        "description": "Test description",
        "status": "open"
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
    issue1 = {
        "title": "Issue 1",
        "description": "Description 1",
        "status": "open"
    }
    issue2 = {
        "title": "Issue 2",
        "description": "Description 2",
        "status": "closed"
    }
    
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
    issue_data = {
        "title": "Test Issue",
        "description": "Test description",
        "status": "open"
    }
    create_response = client.post("/issues", json=issue_data)
    issue_id = create_response.json()["id"]
    
    # Get the issue
    response = client.get(f"/issues/{issue_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == issue_id
    assert data["title"] == "Test Issue"
    assert data["description"] == "Test description"
    assert data["status"] == "open"


def test_get_issue_not_found(client):
    """Test getting a non-existent issue."""
    response = client.get("/issues/999")
    assert response.status_code == 404
