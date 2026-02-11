# BAIssue

A minimal **FastAPI** issue tracker (Business AI wordplay) demonstrating **Clean Architecture** with **SQLite** (development & CI) and **PostgreSQL** (production) support.

## What is this?

**BAIssue** is a small REST API for managing issues (a minimal subset of GitHub Issues). It is designed primarily for **education** and demonstrates:

- Clean Architecture terminology and layering
- Clear separation of concerns
- Testability (unit tests + integration tests + optional E2E tests)
- Minimal configuration and tooling
- CI, tag-based releases, and manual CD with Docker + Render

## Architecture overview

The project follows **Clean Architecture**, with dependencies pointing inward.

```
src/app/
├── domain/                         # Pure domain entities
│   └── issue.py                    # Issue entity with validation and status
├── application/                    # Application services (business logic)
│   ├── issue_use_cases.py          # Issue use cases / business logic
│   └── repositories/               # Repository interfaces
│       └── issue_repository.py
├── interfaces/
│   └── api/                        # HTTP layer (FastAPI router)
│       └── issue_api.py            # API routes with service creation
├── infrastructure/
│   ├── config.py                   # Environment-based configuration (.env optional)
│   ├── database.py                 # SQLAlchemy engine, session, Base
│   ├── persistence/                # Database implementations
│   │   ├── sqlalchemy_models.py    # SQLAlchemy ORM models
│   │   └── sqlalchemy_repository.py
│   └── web/                        # FastAPI application wiring
│       ├── app.py                  # App factory and wiring
│       └── static/                 # Minimal static web UI
│           └── index.html
└── main.py                         # Application entry point
```

### Dependency rule

- **Domain** and **application** layers do not depend on FastAPI or SQLAlchemy.
- **Interfaces** define boundaries and dependency injection points.
- **Infrastructure** implements technical details (web server, database, persistence).

## Architecture Diagrams

### Clean Architecture: Concentric Layers

The following diagram shows the Clean Architecture concentric view with our terminology. Dependencies point **inward** – outer layers depend on inner layers, but inner layers never depend on outer layers.

```mermaid
graph TB
    subgraph Infrastructure["Infrastructure (Outer Layer)"]
        persistence["infrastructure.persistence<br/>(SQLAlchemy models & repository)"]
        web["infrastructure.web<br/>(FastAPI app factory)"]
        config["infrastructure.config<br/>(Environment configuration)"]
        database["infrastructure.database<br/>(Database setup)"]
    end
    
    subgraph Interfaces["Interfaces"]
        api["interfaces.api<br/>(FastAPI routes & DTOs)"]
    end
    
    subgraph Application["Application (Use Cases)"]
        use_cases["application.issue_use_cases<br/>(Business logic)"]
        repo_interface["application.repositories<br/>(Repository interfaces)"]
    end
    
    subgraph Domain["Domain (Core)"]
        entities["domain.issue<br/>(Issue entity & status enum)"]
    end
    
    persistence --> repo_interface
    persistence --> entities
    web --> use_cases
    web --> persistence
    web --> api
    config -.-> web
    database -.-> persistence
    
    api --> use_cases
    api --> entities
    
    use_cases --> repo_interface
    use_cases --> entities
    
    repo_interface --> entities
    
    style Domain fill:#ffd700
    style Application fill:#87ceeb
    style Interfaces fill:#90ee90
    style Infrastructure fill:#ffb6c1
```

**Key principle**: Arrows point **inward**. The outer layers (Infrastructure, Interfaces) depend on inner layers (Application, Domain), never the reverse.

### Hexagonal Architecture: Request and Data Flow

This diagram shows how requests flow through the layers in practice, from the browser to the domain and back. Both the **Browser** and **Database** are external systems that the application connects to through infrastructure adapters.

```mermaid
graph LR
    Browser["Browser / UI"]
    Database[("Database<br/>(PostgreSQL over HTTP)")]
    
    subgraph Infrastructure
        web["infrastructure.web.app<br/>(FastAPI app)"]
        persistence["infrastructure.persistence<br/>(SQLAlchemy repository)"]
    end
    
    subgraph Interfaces
        api["interfaces.api<br/>(API routes)"]
    end
    
    subgraph Application
        use_cases["application.use_cases<br/>(IssueService)"]
        repo_interface["application.repositories<br/>(IssueRepository ABC)"]
    end
    
    subgraph Domain
        entities["domain<br/>(Issue entity)"]
    end
    
    Browser -->|HTTP Request| web
    web --> api
    api --> use_cases
    use_cases --> repo_interface
    repo_interface -.->|implements| persistence
    use_cases --> entities
    persistence --> entities
    persistence -->|SQL| Database
    
    style Domain fill:#ffd700
    style Application fill:#87ceeb
    style Interfaces fill:#90ee90
    style Infrastructure fill:#ffb6c1
```

**Request flow**:
1. Browser sends HTTP request to `infrastructure.web`
2. FastAPI routes in `interfaces.api` receive the request
3. API layer calls `application.use_cases` (business logic)
4. Use cases manipulate `domain` entities
5. Use cases call `application.repositories` interface
6. `infrastructure.persistence` implements the repository interface
7. Persistence layer communicates with external Database via SQL
8. Response flows back through the layers

**Note**: Both Browser and Database are external to the application. The infrastructure layer provides adapters to connect to these external systems.

### What Lives in Each Layer

- **Domain** (`domain/`): Pure business entities and domain logic. No external dependencies. Contains `Issue` entity and `IssueStatus` enum.

- **Application** (`application/`): Business use cases and repository interfaces. Depends only on domain. Contains `IssueService` for orchestrating business operations and `IssueRepository` abstract interface.

- **Interfaces** (`interfaces/`): Adapters that expose application functionality. Contains `issue_api` with FastAPI routes and Pydantic DTOs for HTTP communication. Depends on application and domain.

- **Infrastructure** (`infrastructure/`): Technical implementations and frameworks. Contains database setup, SQLAlchemy models, repository implementations, web server configuration, and environment configuration. Depends on all other layers.

### Dependency Rule

**The Dependency Rule**: Source code dependencies must point only inward, toward higher-level policies.

- **Inner layers** (Domain, Application) define interfaces; **outer layers** (Interfaces, Infrastructure) implement them.
- **Domain** knows nothing about databases, web frameworks, or APIs.
- **Application** defines repository interfaces (ports) that Infrastructure implements (adapters).
- **Interfaces** translate between external protocols (HTTP) and application use cases.
- **Infrastructure** contains all framework-specific code and wires everything together.

This structure ensures testability (mock outer layers), flexibility (swap frameworks), and maintainability (business logic isolated from technical details).

## Web UI and API docs

| Path | Purpose |
|------|---------|
| `/ui` | Minimal web interface (HTML + JavaScript) |
| `/docs` | Swagger / OpenAPI documentation |
| `/` | Redirects to `/ui` |
| `/health` | Simple health check |

The UI is intentionally minimal and exists only to demonstrate API consumption.

## API endpoints

### Issues

- `POST /issues` – Create an issue
- `GET /issues` – List all issues
- `GET /issues/{issue_id}` – Get a single issue
- `DELETE /issues/{issue_id}` – Delete an issue
- `PATCH /issues/{issue_id}/close` – Close an issue
- `PATCH /issues/{issue_id}/reopen` – Reopen an issue

Issue status is represented using an enum:

```
open | closed
```

## Environment configuration

Configuration is done **exclusively via environment variables**. A `.env` file is optional; if present, it can be loaded via `python-dotenv`. If it does not exist, the app still runs with defaults.

### Example `.env`

```dotenv
# -------------------------------------------------
# Database configuration
# -------------------------------------------------
# Development (SQLite file)
# DATABASE_URL=sqlite:///./app.db

# CI / Integration tests (SQLite in-memory)
# DATABASE_URL=sqlite:///:memory:

# Production (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/baissue
```

Notes:
- Many providers use `postgresql://...` (or legacy `postgres://...`). The app normalizes these to SQLAlchemy’s driver URL internally.
- **Never commit `.env`** (keep it in `.gitignore`).

## Running locally

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Start the application

By default, SQLite is used (`app.db`):

```bash
export PYTHONPATH=$PWD/src
uvicorn app.main:app --reload
```

Open:
- UI: http://localhost:8000/ui
- API docs: http://localhost:8000/docs

## Testing

### Unit tests
- No FastAPI
- No SQLAlchemy
- Uses a fake in-memory repository

```bash
export PYTHONPATH=$PWD/src
pytest -q tests/unit
```

### Integration tests
- FastAPI TestClient (requires `httpx`)
- SQLite in-memory database

```bash
export PYTHONPATH=$PWD/src
export DATABASE_URL=sqlite:///:memory:
pytest -q tests/integration
```

### E2E tests (Docker-based)
E2E tests run against a **running Docker container** via real HTTP (using `httpx`).

```bash
export BASE_URL=http://127.0.0.1:8001
pytest -q tests/e2e
```

In CI, the E2E job:
1) builds the Docker image  
2) runs the container on port 8001  
3) executes `pytest -q tests/e2e`  

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
  -e DATABASE_URL=postgresql://user:password@host:5432/baissue \
  baissue
```

## CI, releases, and CD

### Continuous integration
Workflow: **`.github/workflows/ci.yml`**
- Unit tests
- Integration tests (SQLite in-memory)
- Optional E2E tests (Docker-based)

### Releases & images (GHCR)
Workflow: **`.github/workflows/release.yml`**
- Tag-based releases: push a tag `vX.Y.Z`
- Creates a GitHub Release (auto-generated notes)
- Publishes Docker images to **GitHub Container Registry (GHCR)**

```bash
git tag v0.1.0
git push origin v0.1.0
```

Images:
- `ghcr.io/<owner>/baissue:v0.1.0`
- `ghcr.io/<owner>/baissue:latest`

### Manual continuous deployment (Render)
Workflow: **`.github/workflows/cd-render.yml`**
- Deployment is **manual** (`workflow_dispatch`)
- Render deploys the **latest GHCR image**
- Triggered via a **Render Deploy Hook** URL stored as a GitHub secret

## License

This project is intended for **educational use**.