"""Issue entity - represents a business issue in the domain."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Issue:
    """Core business entity representing an issue."""
    
    id: Optional[int]
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validate issue attributes."""
        if not self.title or not self.title.strip():
            raise ValueError("Issue title cannot be empty")
        if self.status not in ["open", "in_progress", "closed"]:
            raise ValueError(f"Invalid status: {self.status}")
