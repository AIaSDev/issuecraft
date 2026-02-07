"""Main FastAPI application with route registration."""
from fastapi import FastAPI

from app.core.config import Config
from app.core.database import init_db
from app.interfaces.controllers.issue_controller import IssueController


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    # Initialize database
    init_db()
    
    # Create FastAPI app
    app = FastAPI(
        title=Config.API_TITLE,
        version=Config.API_VERSION,
        description=Config.API_DESCRIPTION
    )
    
    # Register routes
    app.post("/issues")(IssueController.create_issue)
    app.get("/issues")(IssueController.list_issues)
    app.get("/issues/{issue_id}")(IssueController.get_issue)
    
    @app.get("/health")
    def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    return app


# Create the app instance
app = create_app()
