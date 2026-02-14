# SPECS.md - BAIssue Minimal Spec

## Goals
- Create issues and close issues via REST API.

## Scope
IN:
- Create Issue, Close Issue
OUT:
- Auth, labels, comments

## NFRs
- Response time: typical requests < 100ms locally
- API documented via OpenAPI (/docs)

## Architecture (Clean Architecture)
- Domain: Issue entity (status rules)
- Application: IssueUseCases (create, close)
- Interfaces: FastAPI routes (REST)
- Infrastructure: SQLAlchemy repository + relational DB (SQLite dev/CI, PostgreSQL prod)

## API Contract
- POST /issues
- PATCH /issues/{id}/close
- GET /health

## Data Model (minimal)
- Issue: id, title, status (open|closed)