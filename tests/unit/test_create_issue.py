"""Unit tests for CreateIssue use case."""
from datetime import datetime
from unittest.mock import Mock

from src.entities.issue import Issue
from src.use_cases.create_issue import CreateIssue


def test_create_issue_use_case():
    """Test CreateIssue use case."""
    # Mock repository
    mock_repo = Mock()
    now = datetime.utcnow()
    expected_issue = Issue(
        id=1,
        title="Test Issue",
        description="Test description",
        status="open",
        created_at=now,
        updated_at=now
    )
    mock_repo.create.return_value = expected_issue
    
    # Execute use case
    use_case = CreateIssue(mock_repo)
    result = use_case.execute(
        title="Test Issue",
        description="Test description",
        status="open"
    )
    
    # Verify
    assert result == expected_issue
    mock_repo.create.assert_called_once()
    
    # Verify the issue passed to repository has correct attributes
    call_args = mock_repo.create.call_args[0][0]
    assert call_args.title == "Test Issue"
    assert call_args.description == "Test description"
    assert call_args.status == "open"
    assert call_args.id is None  # ID should be None before persistence


def test_create_issue_default_status():
    """Test CreateIssue use case with default status."""
    mock_repo = Mock()
    now = datetime.utcnow()
    expected_issue = Issue(
        id=1,
        title="Test Issue",
        description="Test description",
        status="open",
        created_at=now,
        updated_at=now
    )
    mock_repo.create.return_value = expected_issue
    
    use_case = CreateIssue(mock_repo)
    result = use_case.execute(
        title="Test Issue",
        description="Test description"
    )
    
    # Verify default status is "open"
    call_args = mock_repo.create.call_args[0][0]
    assert call_args.status == "open"
