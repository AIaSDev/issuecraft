import pytest

from app.domain.issue import IssueStatus
from app.application.issue_use_cases import IssueService
from fake_repository import FakeIssueRepository


def test_create_issue_default_status_open():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    issue = svc.create_issue("Test")
    assert issue.status == IssueStatus.OPEN


def test_close_issue():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    issue = svc.create_issue("Test")
    closed = svc.close_issue(issue.id)

    assert closed.status == IssueStatus.CLOSED


def test_reopen_issue():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    issue = svc.create_issue("Test")
    svc.close_issue(issue.id)
    reopened = svc.reopen_issue(issue.id)

    assert reopened.status == IssueStatus.OPEN


def test_delete_issue():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    issue = svc.create_issue("Test")
    assert svc.delete_issue(issue.id) is True
    assert svc.get_issue(issue.id) is None


def test_delete_issue_not_found():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    assert svc.delete_issue(999) is False


def test_create_issue_empty_title_raises():
    repo = FakeIssueRepository()
    svc = IssueService(repo)

    with pytest.raises(ValueError):
        svc.create_issue("")