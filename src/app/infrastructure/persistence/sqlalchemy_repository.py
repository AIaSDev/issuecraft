from typing import Optional

from sqlalchemy.orm import Session

from app.domain.issue import Issue, IssueStatus
from app.infrastructure.persistence.sqlalchemy_models import IssueModel
from app.application.repositories.issue_repository import IssueRepository


class SQLAlchemyIssueRepository(IssueRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, issue: Issue) -> Issue:
        model = IssueModel(
            title=issue.title,
            body=issue.body,
            status=issue.status.value,
            created_at=issue.created_at,
            updated_at=issue.updated_at,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, issue_id: int) -> Optional[Issue]:
        model = self.session.get(IssueModel, issue_id)
        return self._to_entity(model) if model else None

    def list_all(self) -> list[Issue]:
        models = self.session.query(IssueModel).order_by(IssueModel.id.asc()).all()
        return [self._to_entity(m) for m in models]

    def set_status(self, issue_id: int, status: IssueStatus) -> Optional[Issue]:
        model = self.session.get(IssueModel, issue_id)
        if model is None:
            return None
        model.status = status.value
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def delete(self, issue_id: int) -> bool:
        model = self.session.get(IssueModel, issue_id)
        if model is None:
            return False
        self.session.delete(model)
        self.session.commit()
        return True

    @staticmethod
    def _to_entity(model: IssueModel) -> Issue:
        return Issue(
            id=model.id,
            title=model.title,
            body=model.body,
            status=IssueStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )