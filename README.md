# IssueCraft

A minimal FastAPI issue tracker demonstrating Clean Architecture with SQLite and PostgreSQL support.

## What is this?

IssueCraft is a simple issue tracking API built with FastAPI that demonstrates Clean Architecture principles. It supports SQLite for development/testing and PostgreSQL for production deployment.

## Architecture Overview

The project follows Clean Architecture with clear separation of concerns:

```
src/app/
├── core/                   # Configuration, database setup, dependencies
├── entities/               # Pure domain entities (Issue)
├── use_cases/              # Business logic (CreateIssue, ListIssues, GetIssue)
├── interfaces/
│   ├── controllers/        # FastAPI routers/handlers (HTTP concerns)
│   └── gateways/           # Repository interfaces (Protocol/ABC)
└── frameworks/
    ├── web/                # FastAPI app wiring
    └── persistence/        # SQLAlchemy ORM models + repository implementation
```

**Dependency Rule**: Entities and use_cases do not import from interfaces or frameworks. Dependencies point inward.

## API Endpoints

- `POST /issues` - Create an issue (title required, body optional)
- `GET /issues` - List all issues
- `GET /issues/{issue_id}` - Get a specific issue

## Running Locally

### Prerequisites

- Python 3.11+
- pip

### Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the Application

By default, the application uses SQLite (`app.db` file):

```bash
export PYTHONPATH=$PWD/src
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Example Usage

Create an issue:
```bash
curl -X POST http://localhost:8000/issues \
  -H "Content-Type: application/json" \
  -d '{"title":"Fix bug","body":"Description of the bug"}'
```

List all issues:
```bash
curl http://localhost:8000/issues
```

Get a specific issue:
```bash
curl http://localhost:8000/issues/1
```

## Running Tests

The project has two types of tests:

### Unit Tests

Unit tests use a fake in-memory repository (no FastAPI, no SQLAlchemy):

```bash
export PYTHONPATH=$PWD/src
pytest -q tests/unit
```

### Integration Tests

Integration tests use FastAPI TestClient with SQLite in-memory database:

```bash
export PYTHONPATH=$PWD/src
export DATABASE_URL=sqlite:///:memory:
pytest -q tests/integration
```

### Run All Tests

```bash
export PYTHONPATH=$PWD/src
export DATABASE_URL=sqlite:///:memory:
pytest -q
```

## Running with Docker

### Build the Image

```bash
docker build -t issuecraft .
```

### Run with SQLite (default)

```bash
docker run -p 8000:8000 issuecraft
```

### Run with PostgreSQL

```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg://user:pass@host:5432/dbname \
  issuecraft
```

## Deployment on Render

To deploy on Render or any other cloud platform:

1. Set the `DATABASE_URL` environment variable to your PostgreSQL connection string:
   ```
   postgresql+psycopg://user:password@host:5432/database
   ```

2. The application will automatically:
   - Connect to PostgreSQL using psycopg
   - Create tables on startup using `Base.metadata.create_all()`

## Database Configuration

The application uses a single environment variable for database configuration:

- **Development**: `sqlite:///./app.db` (file-based SQLite, default)
- **CI/Testing**: `sqlite:///:memory:` (in-memory SQLite)
- **Production**: `postgresql+psycopg://...` (PostgreSQL with psycopg)

No additional configuration files needed. Simply set `DATABASE_URL` to switch databases.

## Project Structure

```
issuecraft/
├── src/app/
│   ├── core/                      # Config, database, dependencies
│   │   ├── config.py             # Configuration from environment
│   │   └── database.py           # Database engine and session
│   ├── entities/                  # Domain entities
│   │   └── issue.py              # Issue entity
│   ├── use_cases/                 # Business logic
│   │   ├── create_issue.py       # Create issue use case
│   │   ├── list_issues.py        # List issues use case
│   │   └── get_issue.py          # Get issue use case
│   ├── interfaces/
│   │   ├── controllers/          # HTTP layer
│   │   │   └── issue_controller.py
│   │   └── gateways/             # Repository interfaces
│   │       └── issue_repository.py
│   ├── frameworks/
│   │   ├── web/                  # FastAPI app
│   │   │   └── app.py           # App factory and routes
│   │   └── persistence/          # Database layer
│   │       ├── models.py         # SQLAlchemy models
│   │       └── sqlalchemy_repository.py
│   └── main.py                   # Entry point
├── tests/
│   ├── unit/                     # Unit tests (fake repo)
│   └── integration/              # Integration tests (TestClient)
├── .github/workflows/ci.yml      # CI pipeline
├── Dockerfile                     # Docker configuration
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Development

### Clean Architecture Principles

1. **Entities** are pure Python dataclasses with validation
2. **Use Cases** contain business logic and depend only on repository interfaces
3. **Controllers** handle HTTP concerns (request/response)
4. **Gateways** define repository interfaces (ABC)
5. **Frameworks** contain SQLAlchemy and FastAPI implementations

### Adding New Features

1. Define entity in `entities/`
2. Create use case in `use_cases/`
3. Add repository interface in `interfaces/gateways/`
4. Implement repository in `frameworks/persistence/`
5. Add controller in `interfaces/controllers/`
6. Register routes in `frameworks/web/app.py`
7. Write unit tests (with fake repo) and integration tests

## License

This project is for educational purposes.
