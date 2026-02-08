from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class IssueStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"


@dataclass
class Issue:
    id: Optional[int]
    title: str
    body: Optional[str]
    status: IssueStatus
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("Issue title cannot be empty")