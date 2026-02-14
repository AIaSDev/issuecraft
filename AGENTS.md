# AGENTS.md - Lean SDD Workflow

This file defines the development workflow and guardrails.
Do not store project status here. Status lives in TASKS.md.

## Artifacts (must exist at repo root)
- SPECS.md  : Living specification (what/why + architecture intent)
- TASKS.md  : Task list + current phase + progress tracking

## Expected structure

### SPECS.md sections (required)
- Goals
- Scope (in/out)
- Non-Functional Requirements (NFRs) - minimal
- Architecture (Clean Architecture mapping)
- API Contract (OpenAPI link or endpoint list)
- Data Model (entities overview)

### TASKS.md sections (required)
- CURRENT PHASE (single source of truth for phase)
- Task list with per-task test breakdown:
  - Unit
  - Integration
  - E2E
- Definition of Done checklist (per task or global)
- Coverage / quality targets (optional but recommended)

## Phases
1 SPECIFY  : Update SPECS.md (goals/scope/NFRs/contracts). Then set TASKS.md CURRENT PHASE = 2.
2 DESIGN   : Validate architecture + slice tasks in TASKS.md. Then set CURRENT PHASE = 3.
3 DEVELOP  : Implement strictly test-first per task (TDD). Keep Clean Architecture boundaries. Then set CURRENT PHASE = 4.
                ↺ If spec or architecture mismatch → return to 1 or 2
4 VALIDATE : Run full test suite locally and in CI. Fix failures. Then set CURRENT PHASE = 5.
                ↺ If failing → return to 3
5 DEPLOY   : Container build + E2E against container artifact, then release/deploy.
                ↺ If deployment issues → return to 3 or 4

## Rules (guardrails)
- TDD FIRST: write tests before implementation (tests/unit/ → src/)
- Testing Pyramid guideline: Unit ~70%, Integration ~20%, E2E ~10%
- Clean Architecture layering: domain / application / interfaces / infrastructure
- No merge without green CI
- Prefer small vertical slices (one use case end-to-end) over horizontal layers

## Agent Interaction Model

Agents may:
- Propose architectural changes (Phase 2)
- Generate tests (Phase 3 - Red)
- Generate implementation (Phase 3 - Green)
- Suggest refactoring

Agents must NOT:
- Skip TDD
- Merge without green CI