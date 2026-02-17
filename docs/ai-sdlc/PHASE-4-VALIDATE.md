# PHASE 4 – VALIDATE

Goal: Produce a **release-ready, automatically verified** artifact (tests + container + pipelines).

## Inputs
- `docs/PROJECT.md` (stack, architecture, commands)
- `docs/specs/UC-XXX.md` (E2E scenarios + acceptance criteria)
- `docs/TASKS.md` (CURRENT UC + tasks)
- Code + unit/integration tests from Phase 3

## Outputs
- `tests/e2e/` (E2E tests)
- `Dockerfile` (+ optional `.dockerignore`)
- GitHub Actions:
  - CI workflow (unit + integration)
  - Release workflow (build image + run E2E against image + publish package)

---

## Order (mandatory)

### Step 1 — E2E tests (tests/e2e/)
Purpose: Verify critical user flows end-to-end.

Actions:
- Derive E2E scenarios from `docs/specs/UC-XXX.md` acceptance criteria.
- Keep E2E small and risk-based (Testing Pyramid target: ~10%).
- Ensure tests can run headless in CI.

Review checkpoint:
- Agent lists covered flows + missing edge cases.
- Human approves before moving on.

---

### Step 2 — Containerize (Dockerfile)
Purpose: Ensure the deployable artifact can be built and executed consistently.

Actions:
- Create `Dockerfile` aligned with `docs/PROJECT.md` stack.
- Prefer minimal images, deterministic builds, and non-root runtime where feasible.
- Add `.dockerignore` to reduce build context.

Review checkpoint:
- Agent explains entrypoint/ports/env vars.
- Human approves before moving on.

---

### Step 3 — GitHub Actions: CI (unit + integration)
Purpose: Fast quality gates on every push/PR.

Actions:
- Add `.github/workflows/ci.yml`:
  - install deps
  - run `tests/unit` and `tests/integration`
  - (recommended) coverage report, target ≥ 80%
- CI must be green before merge.

Review checkpoint:
- Agent lists jobs + runtimes + how to run locally.
- Human approves before moving on.

---

### Step 4 — GitHub Actions: Release (image + E2E + package)
Purpose: Verify **the built container** and publish a release artifact.

Actions:
- Add `.github/workflows/release.yml`:
  1. build Docker image (tagged)
  2. run container
  3. execute `tests/e2e` against the running container
  4. publish image to GitHub Packages (GHCR)

Notes:
- E2E MUST run in the release pipeline (not only in CI).
- If E2E fails: fix and repeat Phase 3/4 as needed.

Review checkpoint:
- Agent documents tags, triggers (tag/release), and secrets required.
- Human approves before enabling publishing.

---

## Quality Gates (recommended)
- Full test suite green locally and in CI
- Coverage ≥ 80% (recommended; enforce if module requires)
- Testing Pyramid guideline:
  - Unit ~70%
  - Integration ~20%
  - E2E ~10%
- No release publish without successful container E2E

Next: set `docs/TASKS.md` CURRENT PHASE = 5 and proceed to **PHASE 5 – DEPLOY**.