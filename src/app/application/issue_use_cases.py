from datetime import datetime, timezone
from typing import Optional

from app.domain.issue import Issue, IssueStatus
from app.application.repositories.issue_repository import IssueRepository


class IssueService:
    def __init__(self, repository: IssueRepository):
        self.repository = repository

    def create_issue(self, title: str, body: Optional[str] = None) -> Issue:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        issue = Issue(
            id=None,
            title=title,
            body=body,
            status=IssueStatus.OPEN,
            created_at=now,
            updated_at=now,
        )
        return self.repository.create(issue)

    def get_issue(self, issue_id: int) -> Optional[Issue]:
        return self.repository.get_by_id(issue_id)

    def list_issues(self) -> list[Issue]:
        return self.repository.list_all()

    def close_issue(self, issue_id: int) -> Optional[Issue]:
        return self.repository.set_status(issue_id, IssueStatus.CLOSED)

    def reopen_issue(self, issue_id: int) -> Optional[Issue]:
        return self.repository.set_status(issue_id, IssueStatus.OPEN)

    def delete_issue(self, issue_id: int) -> bool:
        return self.repository.delete(issue_id)