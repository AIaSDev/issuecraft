"""Use case for creating an issue."""
from datetime import datetime, timezone

from app.entities.issue import Issue
from app.interfaces.gateways.issue_repository import IssueRepository


class CreateIssue:
    """Use case to create a new issue."""
    
    def __init__(self, repository: IssueRepository):
        self.repository = repository
    
    def execute(self, title: str, body: str = None) -> Issue:
        """Create a new issue with the given parameters."""
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        issue = Issue(
            id=None,
            title=title,
            body=body,
            created_at=now,
            updated_at=now
        )
        return self.repository.create(issue)
