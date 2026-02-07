"""Use case for listing all issues."""
from typing import List

from app.entities.issue import Issue
from app.interfaces.gateways.issue_repository import IssueRepository


class ListIssues:
    """Use case to list all issues."""
    
    def __init__(self, repository: IssueRepository):
        self.repository = repository
    
    def execute(self) -> List[Issue]:
        """List all issues."""
        return self.repository.list_all()
