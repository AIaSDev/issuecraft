"""SQLAlchemy implementation of IssueRepository."""
from typing import Optional

from sqlalchemy.orm import Session

from app.entities.issue import Issue
from app.frameworks.persistence.models import IssueModel
from app.interfaces.gateways.issue_repository import IssueRepository


class SQLAlchemyIssueRepository(IssueRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, issue: Issue) -> Issue:
        model = IssueModel(
            title=issue.title,
            body=issue.body,
            created_at=issue.created_at,
            updated_at=issue.updated_at,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, issue_id: int) -> Optional[Issue]:
        model = (
            self.session.query(IssueModel)
            .filter(IssueModel.id == issue_id)
            .first()
        )
        return self._to_entity(model) if model else None

    def list_all(self) -> list[Issue]:
        models = (
            self.session.query(IssueModel)
            .order_by(IssueModel.id.asc())
            .all()
        )
        return [self._to_entity(m) for m in models]

    @staticmethod
    def _to_entity(model: IssueModel) -> Issue:
        return Issue(
            id=model.id,
            title=model.title,
            body=model.body,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )