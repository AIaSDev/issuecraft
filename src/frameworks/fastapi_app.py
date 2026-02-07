"""Main FastAPI application."""
from fastapi import FastAPI

from src.core.config import Config
from src.core.database import init_db
from src.interfaces.controllers.issue_controller import IssueController

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
