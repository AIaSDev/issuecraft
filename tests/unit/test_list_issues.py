"""Unit tests for ListIssues use case."""
from datetime import datetime, timezone
from unittest.mock import Mock

from src.entities.issue import Issue
from src.use_cases.list_issues import ListIssues


def test_list_issues_use_case():
    """Test ListIssues use case."""
    # Mock repository
    mock_repo = Mock()
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    expected_issues = [
        Issue(
            id=1,
            title="Issue 1",
            description="Description 1",
            status="open",
            created_at=now,
            updated_at=now
        ),
        Issue(
            id=2,
            title="Issue 2",
            description="Description 2",
            status="closed",
            created_at=now,
            updated_at=now
        )
    ]
    mock_repo.list_all.return_value = expected_issues
    
    # Execute use case
    use_case = ListIssues(mock_repo)
    result = use_case.execute()
    
    # Verify
    assert result == expected_issues
    assert len(result) == 2
    mock_repo.list_all.assert_called_once()


def test_list_issues_empty():
    """Test ListIssues use case with no issues."""
    mock_repo = Mock()
    mock_repo.list_all.return_value = []
    
    use_case = ListIssues(mock_repo)
    result = use_case.execute()
    
    assert result == []
    assert len(result) == 0
