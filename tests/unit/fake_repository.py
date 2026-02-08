from typing import Dict, Optional

from app.domain.issue import Issue, IssueStatus
from app.application.repositories.issue_repository import IssueRepository


class FakeIssueRepository(IssueRepository):
    def __init__(self):
        self._storage: Dict[int, Issue] = {}
        self._next_id = 1

    def create(self, issue: Issue) -> Issue:
        new_issue = Issue(
            id=self._next_id,
            title=issue.title,
            body=issue.body,
            status=issue.status,
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

    def set_status(self, issue_id: int, status: IssueStatus) -> Optional[Issue]:
        issue = self._storage.get(issue_id)
        if issue is None:
            return None
        issue.status = status
        return issue

    def delete(self, issue_id: int) -> bool:
        return self._storage.pop(issue_id, None) is not None