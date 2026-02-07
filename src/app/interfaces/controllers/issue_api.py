"""FastAPI controllers for issue management."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.frameworks.persistence.sqlalchemy_repository import SQLAlchemyIssueRepository
from app.use_cases.issue_service import IssueService

router = APIRouter(prefix="/issues", tags=["issues"])


class IssueCreate(BaseModel):
    title: str
    body: Optional[str] = None


class IssueResponse(BaseModel):
    id: int
    title: str
    body: Optional[str]
    created_at: datetime
    updated_at: datetime


def _service(db: Session) -> IssueService:
    repo = SQLAlchemyIssueRepository(db)
    return IssueService(repo)


@router.post("", response_model=IssueResponse, status_code=201)
def create_issue(payload: IssueCreate, db: Session = Depends(get_db)) -> IssueResponse:
    try:
        issue = _service(db).create_issue(title=payload.title, body=payload.body)
        return IssueResponse(**issue.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[IssueResponse])
def list_issues(db: Session = Depends(get_db)) -> List[IssueResponse]:
    issues = _service(db).list_issues()
    return [IssueResponse(**i.__dict__) for i in issues]


@router.get("/{issue_id}", response_model=IssueResponse)
def get_issue(issue_id: int, db: Session = Depends(get_db)) -> IssueResponse:
    issue = _service(db).get_issue(issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return IssueResponse(**issue.__dict__)