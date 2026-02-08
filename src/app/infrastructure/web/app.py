from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.infrastructure.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.infrastructure.database import get_db
from app.infrastructure.persistence.sqlalchemy_repository import SQLAlchemyIssueRepository
from app.interfaces.api.issue_api import router as issues_router
from app.interfaces.dependencies import get_issue_service
from app.application.issue_use_cases import IssueService


def create_app(init_db: bool = True) -> FastAPI:
    app = FastAPI(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
    )

    def issue_service_provider(db: Session = Depends(get_db)) -> IssueService:
        repo = SQLAlchemyIssueRepository(db)
        return IssueService(repo)

    app.dependency_overrides[get_issue_service] = issue_service_provider

    app.include_router(issues_router)

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    app.mount("/ui", StaticFiles(directory="src/app/infrastructure/web/static", html=True), name="ui")

    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse(url="/ui", status_code=302)

    if init_db:
        from app.infrastructure.database import init_db as _init_db
        _init_db()

    return app


app = create_app()