from abc import ABC, abstractmethod
from typing import Optional

from app.domain.issue import Issue, IssueStatus


class IssueRepository(ABC):
    @abstractmethod
    def create(self, issue: Issue) -> Issue: ...

    @abstractmethod
    def get_by_id(self, issue_id: int) -> Optional[Issue]: ...

    @abstractmethod
    def list_all(self) -> list[Issue]: ...

    @abstractmethod
    def set_status(self, issue_id: int, status: IssueStatus) -> Optional[Issue]: ...

    @abstractmethod
    def delete(self, issue_id: int) -> bool: ...