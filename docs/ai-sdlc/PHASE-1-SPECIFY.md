# PHASE 1 – SPECIFY

Goal: Turn a user story into an executable use case specification.

## Inputs
- User story / Epic / Issue
- Constraints (time, scope, stakeholders)

## Outputs
- `docs/specs/UC-XXX.md` (new or updated)
- `docs/TASKS.md` updated:
  - set CURRENT PHASE = 2
  - set CURRENT UC = UC-XXX

## Actions
- Define scope (IN / OUT)
- Define actors and preconditions
- Define main flow + key error flows
- Define acceptance criteria (testable, unambiguous)
- Define minimal NFRs (only what matters now)
- Define test intent mapping (Unit / Integration / E2E) at a high level

## Rules
- No coding in this phase
- No architecture decisions beyond constraints (those belong to Phase 2)
- Prefer small, vertical UCs (one capability end-to-end)

## UC Template
Use: `docs/specs/UC-TEMPLATE.md`

### Minimal example (structure only)
- Business Intent: …
- Actors: …
- Preconditions: …
- Main Flow: 1) … 2) … 3) …
- Alternative / Error Flows: …
- Acceptance Criteria:
  - Given … When … Then …
- NFRs: …
- Test Mapping:
  - Unit: domain rule(s)
  - Integration: endpoint + persistence
  - E2E: critical user flow

Next: proceed to **PHASE 2 – DESIGN** after UC-XXX is reviewed.