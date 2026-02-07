"""Unit tests for ListIssues use case."""
from app.use_cases.list_issues import ListIssues
from app.use_cases.create_issue import CreateIssue
from tests.unit.fake_repository import FakeIssueRepository


def test_list_issues():
    """Test ListIssues use case."""
    repo = FakeIssueRepository()
    create_use_case = CreateIssue(repo)
    list_use_case = ListIssues(repo)
    
    # Create some issues
    create_use_case.execute(title="Issue 1", body="Body 1")
    create_use_case.execute(title="Issue 2", body="Body 2")
    
    # List issues
    result = list_use_case.execute()
    
    assert len(result) == 2
    assert result[0].title == "Issue 1"
    assert result[1].title == "Issue 2"


def test_list_issues_empty():
    """Test ListIssues use case with no issues."""
    repo = FakeIssueRepository()
    use_case = ListIssues(repo)
    
    result = use_case.execute()
    
    assert result == []
    assert len(result) == 0
