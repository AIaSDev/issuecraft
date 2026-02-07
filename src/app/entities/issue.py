from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Issue:
    id: Optional[int]
    title: str
    body: Optional[str]
    created_at: datetime
    updated_at: datetime