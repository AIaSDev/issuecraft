"""Fake in-memory repository for testing."""
from typing import Dict, List, Optional

from app.entities.issue import Issue
from app.interfaces.gateways.issue_repository import IssueRepository


class FakeIssueRepository(IssueRepository):
    """In-memory repository for testing without SQLAlchemy."""
    
    def __init__(self):
        self._storage: Dict[int, Issue] = {}
        self._next_id = 1
    
    def create(self, issue: Issue) -> Issue:
        """Create a new issue in memory."""
        issue.id = self._next_id
        self._storage[self._next_id] = issue
        self._next_id += 1
        return issue
    
    def get_by_id(self, issue_id: int) -> Optional[Issue]:
        """Get an issue by ID."""
        return self._storage.get(issue_id)
    
    def list_all(self) -> List[Issue]:
        """List all issues."""
        return list(self._storage.values())
