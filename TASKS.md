# TASKS.md - BAIssue Tasks

CURRENT PHASE: 5  # 1=Specify | 2=Design | 3=Develop | 4=Validate | 5=Deploy

## Definition of Done (global)
- [X] Unit tests green
- [X] Integration tests green
- [X] E2E tests green (if task has E2E)
- [X] CI green
- [X] Code follows Clean Architecture boundaries

## Tasks

### 1. Create Issue
1.1 Unit: domain Issue creation rules [DONE]
1.2 Unit: application IssueUseCases.create() [DONE]
1.3 Integration: POST /issues persists + returns 201 [DONE]
1.4 E2E: POST /issues works against container [DONE]

### 2. Close Issue
2.1 Unit: domain Issue.close() transitions open→closed [DONE]
2.2 Unit: application IssueUseCases.close() [DONE]
2.3 Integration: PATCH /issues/{id}/close [DONE]
2.4 E2E: close flow against container [DONE]