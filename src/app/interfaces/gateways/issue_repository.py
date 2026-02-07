"""Repository interface for issue persistence."""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.entities.issue import Issue


class IssueRepository(ABC):
    """Abstract interface for issue persistence."""
    
    @abstractmethod
    def create(self, issue: Issue) -> Issue:
        """Create a new issue and return it with assigned ID."""
        pass
    
    @abstractmethod
    def get_by_id(self, issue_id: int) -> Optional[Issue]:
        """Get an issue by ID, returns None if not found."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Issue]:
        """List all issues."""
        pass
