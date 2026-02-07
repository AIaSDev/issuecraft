import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.frameworks.web.app import create_app


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def client(db_session):
    app = create_app(init_db=False)

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_health_check(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "healthy"}


def test_create_issue(client):
    r = client.post("/issues", json={"title": "Test Issue", "body": "Test body"})
    assert r.status_code == 201  # important
    data = r.json()
    assert data["title"] == "Test Issue"
    assert data["body"] == "Test body"
    assert "id" in data


def test_create_issue_without_body(client):
    r = client.post("/issues", json={"title": "Test Issue"})
    assert r.status_code == 201
    assert r.json()["body"] is None


def test_create_issue_with_empty_title(client):
    r = client.post("/issues", json={"title": "", "body": "x"})
    assert r.status_code == 400


def test_list_issues_empty(client):
    r = client.get("/issues")
    assert r.status_code == 200
    assert r.json() == []


def test_list_issues(client):
    client.post("/issues", json={"title": "Issue 1", "body": "Body 1"})
    client.post("/issues", json={"title": "Issue 2", "body": "Body 2"})

    r = client.get("/issues")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    assert data[0]["title"] == "Issue 1"
    assert data[1]["title"] == "Issue 2"


def test_get_issue(client):
    created = client.post("/issues", json={"title": "Test Issue", "body": "Test body"}).json()
    issue_id = created["id"]

    r = client.get(f"/issues/{issue_id}")
    assert r.status_code == 200
    assert r.json()["id"] == issue_id


def test_get_issue_not_found(client):
    r = client.get("/issues/999")
    assert r.status_code == 404


def test_close_and_reopen_issue(client):
    created = client.post("/issues", json={"title": "Test"}).json()
    issue_id = created["id"]

    closed = client.patch(f"/issues/{issue_id}/close").json()
    assert closed["status"] == "closed"

    reopened = client.patch(f"/issues/{issue_id}/reopen").json()
    assert reopened["status"] == "open"


def test_delete_issue(client):
    created = client.post("/issues", json={"title": "Test"}).json()
    issue_id = created["id"]

    r = client.delete(f"/issues/{issue_id}")
    assert r.status_code == 204

    r = client.get(f"/issues/{issue_id}")
    assert r.status_code == 404