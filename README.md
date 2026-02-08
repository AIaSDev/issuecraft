# BAIssue

A minimal **FastAPI** Business AI issue tracker demonstrating Clean Architecture **Clean Architecture** with **SQLite** (development & CI) and **PostgreSQL** (production) support.

---

## What is this?

**BAIssue** is a small REST API for managing issues (a minimal subset of GitHub Issues).  
It is designed primarily for **education** and demonstrates:

- Clean Architecture terminology and layering
- Clear separation of concerns
- Testability (unit tests + integration tests)
- Minimal configuration and tooling
- CI, Release, and manual CD with Docker

---

## Architecture Overview

The project follows **Clean Architecture**, with dependencies pointing inward.

```
src/app/
├── domain/                         # Pure domain entities
│   └── issue.py                    # Issue entity with validation and status
├── application/                    # Application services (business logic)
│   ├── issue_use_cases.py          # Issue use cases / business logic
│   └── repositories/               # Repository interfaces (ports)
│       └── issue_repository.py
├── interfaces/
│   ├── api/                        # HTTP layer (FastAPI routers)
│   │   └── issue_api.py
│   └── dependencies.py             # Interface-level dependency definitions (ports → use cases)
├── infrastructure/
│   ├── config.py                   # Environment-based configuration (.env optional)
│   ├── database.py                 # SQLAlchemy engine, session, Base
│   ├── persistence/                # Database implementations
│   │   ├── sqlalchemy_models.py    # SQLAlchemy ORM models
│   │   └── sqlalchemy_repository.py
│   └── web/                        # FastAPI application wiring
│       ├── app.py                  # App factory and dependency wiring
│       └── static/                 # Minimal static web UI
│           └── index.html
└── main.py                         # Application entry point
```

### Dependency Rule

- **Domain** and **application** layers do not depend on FastAPI or SQLAlchemy
- **Interfaces** define boundaries (ports)
- **Infrastructure** implements technical details (web, database)

---

## Web UI and API Docs

BAIssue provides two ways to interact with the system:

| Path | Purpose |
|-----|---------|
| `/ui` | Minimal web interface (HTML + JavaScript) |
| `/docs` | Swagger / OpenAPI documentation |
| `/` | Redirects to `/ui` |

The web UI is intentionally minimal and exists only to demonstrate how the API can be consumed.

---

## API Endpoints

### Issues

- `POST /issues` – Create an issue
- `GET /issues` – List all issues
- `GET /issues/{issue_id}` – Get a single issue
- `DELETE /issues/{issue_id}` – Delete an issue
- `PATCH /issues/{issue_id}/close` – Close an issue
- `PATCH /issues/{issue_id}/reopen` – Reopen an issue

### Other

- `GET /docs` – OpenAPI / Swagger UI
- `GET /health` – Simple health check

Issue status is represented using an enum:

```
open | closed
```

---

## Environment Configuration

Configuration is done **exclusively via environment variables**.

### Example `.env`

```dotenv
# -------------------------------------------------
# Application environment
# -------------------------------------------------
ENV=production

# -------------------------------------------------
# Database configuration
# -------------------------------------------------
# Development (SQLite file)
# DATABASE_URL=sqlite:///./app.db

# CI / Integration tests (SQLite in-memory)
# DATABASE_URL=sqlite:///:memory:

# Production (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/database
```

> `.env` files must never be committed to version control.

---

## Running Locally

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Start the Application

By default, SQLite is used (`app.db`):

```bash
export PYTHONPATH=$PWD/src
uvicorn app.main:app --reload
```

Open in your browser:

- UI: http://localhost:8000/ui
- API docs: http://localhost:8000/docs

---

## Testing

### Unit Tests

- No FastAPI
- No SQLAlchemy
- Uses a fake in-memory repository

```bash
export PYTHONPATH=$PWD/src
pytest -q tests/unit
```

### Integration Tests

- FastAPI TestClient
- SQLite in-memory database

```bash
export PYTHONPATH=$PWD/src
export DATABASE_URL=sqlite:///:memory:
pytest -q tests/integration
```

---

## Docker

### Build

```bash
docker build -t baissue .
```

### Run (SQLite)

```bash
docker run -p 8000:8000 baissue
```

### Run (PostgreSQL)

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg://user:password@host:5432/database \
  baissue
```

---

## CI, Releases, and CD

### Continuous Integration

- **ci.yml**
- Runs unit tests and integration tests on every push and PR

### Releases & Images

- **Tag-based releases**
- Push a tag `vX.Y.Z` to trigger:
  - GitHub Release (auto-generated changelog)
  - Docker image published to **GitHub Container Registry (GHCR)**

```bash
git tag v0.1.0
git push origin v0.1.0
```

Images:
- `ghcr.io/<owner>/baissue:v0.1.0`
- `ghcr.io/<owner>/baissue:latest`

### Manual Continuous Deployment (Render)

- Deployment is **manual**
- Render pulls the **latest GHCR image**
- Deployment is triggered via **Render Deploy Hook**
- GitHub Action: `cd-render.yml`
- Triggered using **workflow_dispatch**

---

## License

This project is intended for **educational use**.