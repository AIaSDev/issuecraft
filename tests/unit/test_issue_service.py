import pytest

from app.use_cases.issue_service import IssueService
from tests.unit.fake_repository import FakeIssueRepository


def test_create_issue_with_body():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    result = svc.create_issue(title="Test Issue", body="Test body")

    assert result.id == 1
    assert result.title == "Test Issue"
    assert result.body == "Test body"
    assert result.created_at is not None
    assert result.updated_at is not None


def test_create_issue_without_body():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    result = svc.create_issue(title="Test Issue")

    assert result.id == 1
    assert result.body is None


def test_create_issue_with_empty_title_raises_error():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    with pytest.raises(ValueError, match="Issue title cannot be empty"):
        svc.create_issue(title="   ")


def test_get_issue_found():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    created = svc.create_issue(title="Test Issue", body="Test body")
    loaded = svc.get_issue(created.id)

    assert loaded is not None
    assert loaded.id == created.id
    assert loaded.title == "Test Issue"


def test_get_issue_not_found():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    assert svc.get_issue(999) is None


def test_list_issues():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    svc.create_issue(title="Issue 1", body="Body 1")
    svc.create_issue(title="Issue 2", body="Body 2")

    result = svc.list_issues()

    assert len(result) == 2
    assert result[0].title == "Issue 1"
    assert result[1].title == "Issue 2"


def test_list_issues_empty():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    assert svc.list_issues() == []