"""Unit tests for GetIssue use case."""
from app.use_cases.get_issue import GetIssue
from app.use_cases.create_issue import CreateIssue
from tests.unit.fake_repository import FakeIssueRepository


def test_get_issue():
    """Test GetIssue use case with existing issue."""
    repo = FakeIssueRepository()
    create_use_case = CreateIssue(repo)
    get_use_case = GetIssue(repo)
    
    # Create an issue
    created = create_use_case.execute(title="Test Issue", body="Test body")
    
    # Get the issue
    result = get_use_case.execute(created.id)
    
    assert result is not None
    assert result.id == created.id
    assert result.title == "Test Issue"
    assert result.body == "Test body"


def test_get_issue_not_found():
    """Test GetIssue use case with non-existent issue."""
    repo = FakeIssueRepository()
    use_case = GetIssue(repo)
    
    result = use_case.execute(999)
    
    assert result is None
