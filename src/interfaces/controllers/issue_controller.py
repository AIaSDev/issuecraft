"""FastAPI controllers for issue management."""
from typing import List

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.frameworks.sqlalchemy_repository import SQLAlchemyIssueRepository
from src.use_cases.create_issue import CreateIssue
from src.use_cases.get_issue import GetIssue
from src.use_cases.list_issues import ListIssues


class IssueCreate(BaseModel):
    """Request model for creating an issue."""
    title: str
    description: str
    status: str = "open"


class IssueResponse(BaseModel):
    """Response model for an issue."""
    id: int
    title: str
    description: str
    status: str
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class IssueController:
    """Controller for issue endpoints."""
    
    @staticmethod
    def create_issue(issue_data: IssueCreate, db: Session = Depends(get_db)) -> IssueResponse:
        """Create a new issue."""
        repository = SQLAlchemyIssueRepository(db)
        use_case = CreateIssue(repository)
        
        try:
            issue = use_case.execute(
                title=issue_data.title,
                description=issue_data.description,
                status=issue_data.status
            )
            return IssueResponse(
                id=issue.id,
                title=issue.title,
                description=issue.description,
                status=issue.status,
                created_at=issue.created_at.isoformat(),
                updated_at=issue.updated_at.isoformat()
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @staticmethod
    def list_issues(db: Session = Depends(get_db)) -> List[IssueResponse]:
        """List all issues."""
        repository = SQLAlchemyIssueRepository(db)
        use_case = ListIssues(repository)
        
        issues = use_case.execute()
        return [
            IssueResponse(
                id=issue.id,
                title=issue.title,
                description=issue.description,
                status=issue.status,
                created_at=issue.created_at.isoformat(),
                updated_at=issue.updated_at.isoformat()
            )
            for issue in issues
        ]
    
    @staticmethod
    def get_issue(issue_id: int, db: Session = Depends(get_db)) -> IssueResponse:
        """Get an issue by ID."""
        repository = SQLAlchemyIssueRepository(db)
        use_case = GetIssue(repository)
        
        issue = use_case.execute(issue_id)
        if not issue:
            raise HTTPException(status_code=404, detail="Issue not found")
        
        return IssueResponse(
            id=issue.id,
            title=issue.title,
            description=issue.description,
            status=issue.status,
            created_at=issue.created_at.isoformat(),
            updated_at=issue.updated_at.isoformat()
        )
