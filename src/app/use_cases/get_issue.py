"""Use case for getting an issue by ID."""
from typing import Optional

from app.entities.issue import Issue
from app.interfaces.gateways.issue_repository import IssueRepository


class GetIssue:
    """Use case to get an issue by ID."""
    
    def __init__(self, repository: IssueRepository):
        self.repository = repository
    
    def execute(self, issue_id: int) -> Optional[Issue]:
        """Get an issue by its ID."""
        return self.repository.get_by_id(issue_id)
