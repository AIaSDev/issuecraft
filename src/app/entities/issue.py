"""Issue entity - represents a business issue in the domain."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Issue:
    """Core business entity representing an issue."""
    
    id: Optional[int]
    title: str
    body: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        """Validate issue attributes."""
        if not self.title or not self.title.strip():
            raise ValueError("Issue title cannot be empty")
