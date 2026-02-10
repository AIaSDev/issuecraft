from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.infrastructure.config import API_TITLE, API_VERSION, API_DESCRIPTION
from app.interfaces.api.issue_api import router as issues_router


def create_app(init_db: bool = True) -> FastAPI:
    """
    Application factory that creates and configures the FastAPI application.
    
    This function:
    1. Creates the FastAPI app with metadata
    2. Registers API routers
    3. Adds health check and static file endpoints
    4. Optionally initializes the database
    
    Dependency injection is handled via the Depends mechanism in route handlers.
    The actual wiring is defined in app.interfaces.dependencies.
    
    Args:
        init_db: Whether to initialize database tables on startup
        
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
    )

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