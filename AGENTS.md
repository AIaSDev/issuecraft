# AGENTS.md

## Agents and Automation

This repository may be used with various automated assistants (“agents”) that help with coding, testing, documentation, release, or deployment tasks.

An *agent* can be any system that:
- suggests or generates code,
- reviews or refactors existing code,
- automates tests, releases, or deployments,
- or assists developers during development (locally or in CI).

Agents are supporting tools, not decision-makers.

---

## Goals of Using Agents

Agents may be used to:
- reduce repetitive or mechanical work,
- suggest simplifications or cleanups,
- support testing and CI/CD workflows,
- keep documentation up to date.

They should not replace understanding of the code, architecture, or domain.

---

## Architectural Boundaries

When using agents, the following rules apply:

- Domain entities and use cases must remain framework-independent.
- Framework-specific code stays in outer layers.
- Agents must not introduce cross-layer dependencies.
- All changes must keep existing tests passing.

---

## Human-in-the-Loop Principle

All agent-generated changes must be:
1. Reviewed by a human,
2. Understood before merging,
3. Verified by running tests and CI.

Do not blindly accept agent suggestions.

---

## Scope and Limitations

Agents may:
- refactor code for clarity,
- suggest tests or documentation updates,
- automate release or deployment steps.

Agents should not:
- introduce hidden complexity,
- bypass architectural decisions,
- modify business logic without explicit intent.

---

## Summary

Agents are optional helpers that can improve productivity and learning outcomes when used responsibly.  
Final responsibility for correctness, architecture, and design always lies with the developer.