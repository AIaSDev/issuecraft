"""Unit tests for Issue entity."""
import pytest
from datetime import datetime, timezone

from src.entities.issue import Issue


def test_issue_creation():
    """Test creating a valid issue."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    issue = Issue(
        id=1,
        title="Test Issue",
        description="Test description",
        status="open",
        created_at=now,
        updated_at=now
    )
    
    assert issue.id == 1
    assert issue.title == "Test Issue"
    assert issue.description == "Test description"
    assert issue.status == "open"
    assert issue.created_at == now
    assert issue.updated_at == now


def test_issue_empty_title_raises_error():
    """Test that empty title raises ValueError."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    
    with pytest.raises(ValueError, match="Issue title cannot be empty"):
        Issue(
            id=1,
            title="",
            description="Test description",
            status="open",
            created_at=now,
            updated_at=now
        )


def test_issue_invalid_status_raises_error():
    """Test that invalid status raises ValueError."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    
    with pytest.raises(ValueError, match="Invalid status"):
        Issue(
            id=1,
            title="Test Issue",
            description="Test description",
            status="invalid",
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
            description="Test description",
            status="open",
            created_at=now,
            updated_at=now
        )
