"""Fake in-memory repository for testing."""
from typing import Dict, Optional

from app.entities.issue import Issue
from app.interfaces.gateways.issue_repository import IssueRepository


class FakeIssueRepository(IssueRepository):
    def __init__(self):
        self._storage: Dict[int, Issue] = {}
        self._next_id = 1

    def create(self, issue: Issue) -> Issue:
        new_issue = Issue(
            id=self._next_id,
            title=issue.title,
            body=issue.body,
            created_at=issue.created_at,
            updated_at=issue.updated_at,
        )
        self._storage[self._next_id] = new_issue
        self._next_id += 1
        return new_issue

    def get_by_id(self, issue_id: int) -> Optional[Issue]:
        return self._storage.get(issue_id)

    def list_all(self) -> list[Issue]:
        return list(self._storage.values())