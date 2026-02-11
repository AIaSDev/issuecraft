from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.domain.issue import IssueStatus
from app.application.issue_use_cases import IssueService


class IssueCreate(BaseModel):
    title: str
    body: Optional[str] = None


class IssueResponse(BaseModel):
    id: int
    title: str
    body: Optional[str]
    status: IssueStatus
    created_at: datetime
    updated_at: datetime


router = APIRouter(prefix="/issues", tags=["issues"])


def get_service() -> IssueService:
    raise NotImplementedError("Service must be provided via dependency_overrides")


@router.post("", response_model=IssueResponse, status_code=201)
def create_issue(payload: IssueCreate, service: IssueService = Depends(get_service)):
    try:
        return service.create_issue(payload.title, payload.body)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[IssueResponse])
def list_issues(service: IssueService = Depends(get_service)):
    return service.list_issues()


@router.get("/{issue_id}", response_model=IssueResponse)
def get_issue(issue_id: int, service: IssueService = Depends(get_service)):
    issue = service.get_issue(issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.patch("/{issue_id}/close", response_model=IssueResponse)
def close_issue(issue_id: int, service: IssueService = Depends(get_service)):
    issue = service.close_issue(issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.patch("/{issue_id}/reopen", response_model=IssueResponse)
def reopen_issue(issue_id: int, service: IssueService = Depends(get_service)):
    issue = service.reopen_issue(issue_id)
    if issue is None:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue


@router.delete("/{issue_id}", status_code=204)
def delete_issue(issue_id: int, service: IssueService = Depends(get_service)):
    if not service.delete_issue(issue_id):
        raise HTTPException(status_code=404, detail="Issue not found")
