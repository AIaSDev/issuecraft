from fastapi import Depends, FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.infrastructure.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.infrastructure.database import get_db
from app.infrastructure.persistence.sqlalchemy_repository import SQLAlchemyIssueRepository
from app.application.issue_use_cases import IssueService
from app.interfaces.api import issue_api


def create_app(init_db: bool = True) -> FastAPI:
    app = FastAPI(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
    )

    def service_factory(request: Request) -> IssueService:
        db_generator = app.dependency_overrides.get(get_db, get_db)
        db = next(db_generator())
        repo = SQLAlchemyIssueRepository(db)
        return IssueService(repo)

    app.state.service_factory = service_factory
    app.include_router(issue_api.router)

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
