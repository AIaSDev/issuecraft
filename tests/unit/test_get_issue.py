"""Unit tests for GetIssue use case."""
from datetime import datetime
from unittest.mock import Mock

from src.entities.issue import Issue
from src.use_cases.get_issue import GetIssue


def test_get_issue_use_case():
    """Test GetIssue use case with existing issue."""
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
    mock_repo.get_by_id.return_value = expected_issue
    
    # Execute use case
    use_case = GetIssue(mock_repo)
    result = use_case.execute(1)
    
    # Verify
    assert result == expected_issue
    mock_repo.get_by_id.assert_called_once_with(1)


def test_get_issue_not_found():
    """Test GetIssue use case with non-existent issue."""
    mock_repo = Mock()
    mock_repo.get_by_id.return_value = None
    
    use_case = GetIssue(mock_repo)
    result = use_case.execute(999)
    
    assert result is None
    mock_repo.get_by_id.assert_called_once_with(999)
