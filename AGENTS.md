# AGENTS.md – AI-SDLC Router

This file defines the orchestration rules for AI-assisted development.
Do not store project status here.

Project status lives in: docs/TASKS.md

---

## Current Phase

Single source of truth: → docs/TASKS.md

Valid phases:
1 SPECIFY
2 DESIGN
3 DEVELOP
4 VALIDATE
5 DEPLOY

Never skip phases.
Phase transitions must update docs/TASKS.md.

---

## Context Load Order (strict)

1. docs/PROJECT.md
2. docs/TASKS.md
3. docs/ai-sdlc/PHASE-[X].md
4. docs/specs/UC-XXX.md

Load only what is required for the current task.
Minimize token usage.

---

## Guardrails

- TDD first (tests before implementation)
- Testing Pyramid guideline: Unit ~70%, Integration ~20%, E2E ~10%
- Clean Architecture required
- Green CI required before phase transition
- Vertical slice per use case
- No code without matching tests

---

## Architecture Rule

Dependency direction:

domain ← application ← interfaces ← infrastructure

Rules:
- Domain has no framework imports
- Infrastructure depends inward
- No circular dependencies
- Violations must be refactored immediately

---

## Deployment Rule

DEPLOY (Phase 5) allowed only if:
- CI is green
- Release build succeeded
- Container artifact validated