from app.use_cases.issue_service import IssueService


def get_issue_service() -> IssueService:
    raise RuntimeError("get_issue_service is not wired")