from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.infrastructure.database import Base


def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class IssueModel(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    body = Column(Text, nullable=True)
    status = Column(String(16), nullable=False, default="open")
    created_at = Column(DateTime, nullable=False, default=utc_now)
    updated_at = Column(DateTime, nullable=False, default=utc_now, onupdate=utc_now)