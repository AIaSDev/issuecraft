# PHASE 5 – DEPLOY

Goal: Deliver the **validated container artifact** to a cloud runtime via **Continuous Deployment (CD)**.

## Inputs
- Release workflow from Phase 4 (build + E2E + publish image to GHCR)
- Deployment target definition (Render Web Service or equivalent)
- Required secrets configured in GitHub

## Outputs
- `.github/workflows/deploy.yml` (CD)
- Cloud service configured to run the published image
- Production URL + basic health verification

---

## Deployment Strategy (recommended)

### Option A — Deploy on Release/Tag (preferred)
Trigger CD when a release artifact exists (tag or GitHub Release), after Phase 4 gates succeeded.

### Option B — Deploy on main (only if course allows)
Trigger on pushes to `main` but still require green CI and a successful release build.

---

## Actions

### Step 1 — Define target (Render)
Actions:
- Create a Render Web Service (or Blueprint) using a **Docker image** from GHCR.
- Configure runtime settings:
  - `PORT` mapping (Render provides port via env var)
  - DB connection env vars (if applicable)
  - health endpoint (recommended: `GET /health`)

Agent must ask (once) for:
- service type (web service vs background worker)
- runtime port and start command (or Docker CMD/ENTRYPOINT)
- required environment variables (DB, secrets)
- deployment trigger (tag/release vs main)

---

### Step 2 — GitHub Actions CD workflow (deploy.yml)
Actions:
- Authenticate to the target (Render Deploy Hook or Render API key).
- Trigger deployment after a successful release build.
- (Optional) run a smoke check: call `/health` and fail if not 200.

Minimal responsibilities of CD:
- Deploy the exact released image tag (avoid “latest” if possible).
- Provide traceability: commit SHA ↔ image tag ↔ deployment.

---

## Guardrails
- CD MUST deploy only artifacts that already passed Phase 4 (container E2E).
- Rollback path must be possible (previous image tag).
- Do not store credentials in repo; use GitHub Secrets.

---

## Completion Criteria
- Cloud deployment succeeded
- Service reachable
- `/health` returns 200
- Deployment references a concrete image tag from GHCR

Next: set `docs/TASKS.md` CURRENT PHASE = 1 for the next UC, or proceed with a new iteration.