"""Main FastAPI application with route registration."""
from fastapi import FastAPI

from app.core.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.interfaces.controllers.issues_api import router as issues_router


def create_app(init_db: bool = True) -> FastAPI:
    app = FastAPI(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
    )

    app.include_router(issues_router)

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    if init_db:
        from app.core.database import init_db as _init_db
        _init_db()

    return app


app = create_app()