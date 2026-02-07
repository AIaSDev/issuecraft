# IssueCraft

A minimal **FastAPI** issue tracker demonstrating **Clean Architecture** with **SQLite** (development & CI) and **PostgreSQL** (production) support.

---

## What is this?

**IssueCraft** is a small REST API for managing issues (similar to a very small subset of GitHub Issues).  
It is designed for **educational purposes** and focuses on:

- Clean Architecture terminology and layering
- Clear separation of concerns
- Testability (unit tests + integration tests)
- Minimal configuration and tooling

---

## Architecture Overview

The project follows **Clean Architecture** with dependencies pointing inward.

```
src/app/
├── core/                      # Configuration and database setup
│   ├── config.py              # Environment-based configuration
│   └── database.py            # SQLAlchemy engine, session, Base
├── entities/                  # Pure domain entities
│   └── issue.py               # Issue entity with validation
├── use_cases/                 # Application services (use cases)
│   └── issue_service.py       # IssueService (business logic orchestration)
├── interfaces/
│   ├── controllers/           # HTTP layer (FastAPI routers)
│   │   └── issues_api.py
│   └── gateways/              # Repository interfaces (ports)
│       └── issue_repository.py
├── frameworks/
│   ├── web/                   # FastAPI application wiring
│   │   └── app.py
│   └── persistence/           # Database implementations
│       ├── models.py          # SQLAlchemy ORM models
│       └── sqlalchemy_repository.py
└── main.py                    # Application entry point
```

### Dependency Rule

- **Entities** and **use cases** do not depend on FastAPI or SQLAlchemy
- **Interfaces** define boundaries (ports)
- **Frameworks** implement technical details (web, database)

---

## API Endpoints

- `POST /issues` – Create an issue (title required, body optional)
- `GET /issues` – List all issues
- `GET /issues/{issue_id}` – Get a specific issue
- `GET /health` – Health check

---

## Running Locally

### Prerequisites

- Python 3.11+
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Run the Application

By default, the application uses **file-based SQLite** (`app.db`):

```bash
export PYTHONPATH=$PWD/src
uvicorn app.main:app --reload
```

---

## Running Tests

### Unit Tests

```bash
export PYTHONPATH=$PWD/src
pytest -q tests/unit
```

### Integration Tests

```bash
export PYTHONPATH=$PWD/src
export DATABASE_URL=sqlite:///:memory:
pytest -q tests/integration
```

---

## Running with Docker

```bash
docker build -t issuecraft .
docker run -p 8000:8000 issuecraft
```

---

## License

This project is intended for **educational use**.