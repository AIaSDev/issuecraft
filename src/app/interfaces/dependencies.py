from app.application.issue_use_cases import IssueService


def get_issue_service() -> IssueService:
    raise RuntimeError("get_issue_service is not wired")