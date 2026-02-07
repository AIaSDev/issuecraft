"""Unit tests for Issue entity."""
import pytest
from datetime import datetime, timezone

from app.entities.issue import Issue


def test_issue_creation():
    """Test creating a valid issue."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    issue = Issue(
        id=1,
        title="Test Issue",
        body="Test body",
        created_at=now,
        updated_at=now
    )
    
    assert issue.id == 1
    assert issue.title == "Test Issue"
    assert issue.body == "Test body"
    assert issue.created_at == now
    assert issue.updated_at == now


def test_issue_without_body():
    """Test creating an issue without body."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    issue = Issue(
        id=1,
        title="Test Issue",
        body=None,
        created_at=now,
        updated_at=now
    )
    
    assert issue.id == 1
    assert issue.title == "Test Issue"
    assert issue.body is None


def test_issue_empty_title_raises_error():
    """Test that empty title raises ValueError."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    
    with pytest.raises(ValueError, match="Issue title cannot be empty"):
        Issue(
            id=1,
            title="",
            body="Test body",
            created_at=now,
            updated_at=now
        )


def test_issue_whitespace_title_raises_error():
    """Test that whitespace-only title raises ValueError."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    
    with pytest.raises(ValueError, match="Issue title cannot be empty"):
        Issue(
            id=1,
            title="   ",
            body="Test body",
            created_at=now,
            updated_at=now
        )
