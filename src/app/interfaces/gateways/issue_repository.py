"""Repository interface for issue persistence."""
from abc import ABC, abstractmethod
from typing import Optional

from app.entities.issue import Issue


class IssueRepository(ABC):
    @abstractmethod
    def create(self, issue: Issue) -> Issue: ...

    @abstractmethod
    def get_by_id(self, issue_id: int) -> Optional[Issue]: ...

    @abstractmethod
    def list_all(self) -> list[Issue]: ...