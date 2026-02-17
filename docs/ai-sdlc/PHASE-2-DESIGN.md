# PHASE 2 – DESIGN

Goal: Define architecture and testing strategy for the current use case.

## Inputs
- `docs/specs/UC-XXX.md`
- `docs/PROJECT.md` (constraints + stack, if present)
- `docs/TASKS.md` (CURRENT UC)

## Outputs
- `docs/PROJECT.md` updated (architecture + stack decisions)
- `docs/TASKS.md` updated (task slicing, CURRENT PHASE = 3)

## Actions
1. **Confirm stack constraints (ask first)**
   - Frameworks: API, DB/ORM, migrations, testing
   - Runtime/tooling: Python/Node, package manager, container/runtime
   - Target environment: local + CI + production
   - If constraints are missing, ask concise questions before proceeding.

2. **Validate Clean Architecture boundaries**
   Dependency direction: `domain ← application ← interfaces ← infrastructure`

3. **Define project structure (minimal)**
   - `src/domain/`
   - `src/application/`
   - `src/interfaces/`
   - `src/infrastructure/`
   - `tests/unit/` `tests/integration/` `tests/e2e/`

4. **Define API contract surface**
   - Confirm endpoints, status codes, error shapes (from UC acceptance criteria)
   - Link or create minimal OpenAPI reference in `docs/PROJECT.md`

5. **Slice tasks in `docs/TASKS.md`**
   - Vertical slices per UC:
     - Integration tests
     - Unit tests (domain + use case)
     - Implementation
     - Validation steps (CI)
   - Keep tasks small and reviewable.

6. **Review dependencies**
   - Ensure domain/application are framework-free
   - Keep infra/framework choices at the edge
   - Avoid adding libraries unless justified by UC or CI needs.

## Clean Architecture rules (enforced)
- Domain has **no** framework imports.
- Application depends only on domain (use cases orchestrate domain logic).
- Interfaces adapt external I/O (HTTP, CLI) to application.
- Infrastructure implements ports/adapters (DB, messaging, external APIs).
- No circular dependencies; refactor violations immediately.

## Agent prompts (required behaviour)
Before writing plans, the agent MUST ask (if not already specified):
- API framework? (e.g., FastAPI / Spring / .NET / Express)
- ORM + DB? (e.g., SQLAlchemy + Postgres)
- Migrations? (e.g., Alembic / Flyway)
- Unit/integration test stack? (e.g., pytest + httpx + testcontainers)
- Coverage target and CI constraints? (GitHub Actions, required checks)

Next: proceed to **PHASE 3 – DEVELOP** after architecture is reviewed and tasks are sliced.