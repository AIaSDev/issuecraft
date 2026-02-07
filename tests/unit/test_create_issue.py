"""Unit tests for CreateIssue use case."""
from app.use_cases.create_issue import CreateIssue
from tests.unit.fake_repository import FakeIssueRepository


def test_create_issue_with_body():
    """Test CreateIssue use case with body."""
    repo = FakeIssueRepository()
    use_case = CreateIssue(repo)
    
    result = use_case.execute(title="Test Issue", body="Test body")
    
    assert result.id == 1
    assert result.title == "Test Issue"
    assert result.body == "Test body"
    assert result.created_at is not None
    assert result.updated_at is not None


def test_create_issue_without_body():
    """Test CreateIssue use case without body."""
    repo = FakeIssueRepository()
    use_case = CreateIssue(repo)
    
    result = use_case.execute(title="Test Issue")
    
    assert result.id == 1
    assert result.title == "Test Issue"
    assert result.body is None
    assert result.created_at is not None
    assert result.updated_at is not None
