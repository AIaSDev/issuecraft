# PHASE 3 – DEVELOP

Goal: Implement the current use case using **tests-first** and respecting **PROJECT.md architecture**.

## Inputs
- `docs/PROJECT.md` (architecture, stack, boundaries)
- `docs/TASKS.md` (CURRENT UC + task list)
- `docs/specs/UC-XXX.md` (acceptance criteria + test mapping)

## Outputs
- Tests + code for the current UC
- `docs/TASKS.md` updated (progress + notes)

## Order (mandatory)
1. **Integration test (first)**
2. **Unit tests (second)**
3. **Code (Red → Green → Refactor)**
4. **Review checkpoint after each step**

---

## Step 1 — Integration tests (tests/integration/)
Purpose: Verify interfaces + infrastructure wiring (API + DB) for the UC.

Actions:
- Derive scenarios from UC acceptance criteria (happy path + key errors).
- Test API contract behaviour: status codes, payload shape, persistence effects.
- Keep integration tests deterministic (isolated DB, fixtures, clean state).

**Review checkpoint (required):**
- Agent summarizes: covered scenarios + missing cases.
- Human approves or adjusts before continuing.

---

## Step 2 — Unit tests (tests/unit/)
Purpose: Specify domain rules and use case behaviour without frameworks.

Actions:
- Domain tests: entities/value objects (rules, invariants, transitions).
- Application tests: use case/service orchestration (ports mocked).
- No framework imports in domain/application tests unless explicitly allowed by PROJECT.md.

**Review checkpoint (required):**
- Agent shows test intent mapping to UC sections (Main/Alt flows).
- Human approves or adjusts before continuing.

---

## Step 3 — Code (src/*) with strict TDD
**Red → Green → Refactor**
- RED: ensure new tests fail for the right reason
- GREEN: minimal implementation to pass tests
- REFACTOR: clean up while keeping tests green

**Mandatory execution:**
- After code generation, run **unit tests locally** (fast feedback).
- Fix until green before proceeding.

**Clean Architecture guardrails (from PROJECT.md)**
- `domain` has no framework imports
- dependencies flow inward: `domain ← application ← interfaces ← infrastructure`
- no circular deps; refactor immediately if violated

**Review checkpoint (required):**
- Agent provides diff summary (what changed, why, risks).
- Human reviews before commit.

---

## AI-assisted test creation (two variants)

### Variant 1 — Spec → Agent → Review
- Agent reads `UC-XXX.md` + PROJECT.md constraints
- Agent writes complete tests
- Human reviews in chat; agent applies changes

### Variant 2 — Comment → Completion → Refine
- Human writes a structured test comment skeleton
- IDE completion generates the test body
- Human refines; agent helps patch/fix

---

## Completion criteria (per task)
- Integration tests written and meaningful
- Unit tests written (domain + application)
- Unit tests green locally
- Changes recorded in `docs/TASKS.md` (status + notes)

Next: set `docs/TASKS.md` CURRENT PHASE = 4 and proceed to **PHASE 4 – VALIDATE**.