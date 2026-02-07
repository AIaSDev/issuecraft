"""Use case for creating an issue."""
from datetime import datetime

from src.entities.issue import Issue
from src.interfaces.gateways.issue_repository import IssueRepository


class CreateIssue:
    """Use case to create a new issue."""
    
    def __init__(self, repository: IssueRepository):
        self.repository = repository
    
    def execute(self, title: str, description: str, status: str = "open") -> Issue:
        """Create a new issue with the given parameters."""
        now = datetime.utcnow()
        issue = Issue(
            id=None,
            title=title,
            description=description,
            status=status,
            created_at=now,
            updated_at=now
        )
        return self.repository.create(issue)
