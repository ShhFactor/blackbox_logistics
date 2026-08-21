# GitHub Collaboration Workflow

This repository is developed collaboratively. Follow this workflow for all
non-trivial changes.

## Issue-first development

Before implementing a feature, bug fix, refactor, or significant task:

1. Identify the GitHub issue associated with the work.
2. Read its description, acceptance criteria, comments, dependencies, and
   linked issues or pull requests.
3. Do not expand the scope beyond the issue without documenting why and
   obtaining agreement from the affected owners.
4. If no appropriate issue exists, create or recommend one before beginning
   substantial work.

Small typo fixes, trivial documentation corrections, and similarly
insignificant changes may be handled without a dedicated issue.

## Issue scope

Each issue represents one primary unit of work. Prefer:

```text
one issue -> one main task
one issue -> one working branch
one branch -> one pull request
```

Do not combine unrelated changes. Split an issue when its parts can be
delivered and reviewed independently.

## Branch naming

Create branches from an up-to-date `main` and include the issue number:

```text
feature/<issue-number>-<short-description>
bugfix/<issue-number>-<short-description>
refactor/<issue-number>-<short-description>
docs/<issue-number>-<short-description>
test/<issue-number>-<short-description>
```

Examples:

```text
feature/42-jwt-auth
bugfix/57-login-crash
refactor/61-database-layer
docs/72-api-documentation
test/81-assignment-regression
```

Never make feature-development changes directly on `main`.

## Commits

Keep commits focused and logically grouped. Commit messages explain what
changed rather than merely stating that files were modified. Reference the
issue where useful:

```text
Add JWT validation middleware (#42)
```

Do not mix unrelated refactoring, formatting, dependency upgrades, and feature
work unless they are required for the task.

## Pull requests

All significant changes go through a pull request. A pull request must:

- Address one primary issue.
- Explain what changed.
- Explain important implementation decisions.
- List relevant tests and their results.
- Call out limitations and known risks.
- Link the associated issue.

When the pull request completely satisfies an issue, include:

```text
Closes #<issue-number>
```

Do not close an issue until its acceptance criteria are satisfied.

## Code review

Before marking a pull request ready:

- Run relevant tests.
- Run linting and type checking when configured.
- Inspect the complete diff for accidental changes.
- Verify every acceptance criterion.
- Check for regressions.
- Remove debugging code and unnecessary generated files.
- Verify that no secrets or credentials were introduced.

Do not bypass failing checks to make a pull request mergeable. Follow the
review routing and merge gates in `TEAM_PIPELINE.md`.

## Issue labels

Prefer structured labels. Create these labels in GitHub before relying on them
in automation.

### Type

```text
type: bug
type: feature
type: task
type: refactor
type: documentation
type: testing
```

### Area

```text
area: frontend
area: backend
area: database
area: devops
area: ai
```

Add repository-specific areas as the application grows.

### Priority

```text
priority: high
priority: medium
priority: low
```

High priority means the issue blocks important development, creates a serious
reliability or security problem, or breaks core functionality. Do not classify
everything as high priority.

### Status and contribution

```text
status: blocked
good first issue
help wanted
```

## Issue quality

An issue must contain enough information for another contributor and their LLM
instance to implement it without guessing. Use this structure:

```markdown
## Goal

What needs to be accomplished?

## Context

Why is this change needed?

## Requirements

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Acceptance criteria

- [ ] Observable condition proving the task is complete
- [ ] Relevant tests pass
- [ ] No known regression introduced

## Dependencies

List blocking or related issues when applicable.
```

## Bug reports

Bug reports should include:

```markdown
## Description

Describe the failure.

## Steps to reproduce

1.
2.
3.

## Expected behavior

What should happen?

## Actual behavior

What happens instead?

## Environment

Relevant OS, runtime, package, browser, API, or deployment information.

## Logs or evidence

Relevant logs, stack traces, screenshots, requests, or responses. Remove
secrets and unnecessary personal data.

## Acceptance criteria

- [ ] Root cause identified
- [ ] Bug fixed
- [ ] Regression test added when practical
- [ ] Existing tests pass
```

## Dependencies and blocked work

Before starting an issue, check whether it depends on unfinished work. Do not
implement downstream functionality by inventing assumptions about unfinished
dependencies.

When blocked:

1. Identify the dependency.
2. Document the blocker.
3. Link the blocking issue.
4. Work only on independent portions that will not create unnecessary rework.

## GitHub Project status

When a GitHub Project is used, work progresses through:

```text
Backlog -> Todo -> In Progress -> Review -> Done
```

`Done` means the implementation has been reviewed and merged and all required
acceptance criteria are satisfied. Code merely being written is not `Done`.

## Coding-agent behavior

When a coding agent is asked to implement a GitHub issue, it must:

1. Read `AGENTS.md`, the issue, and the relevant repository instructions.
2. Inspect the existing implementation before editing.
3. Determine the smallest correct change satisfying the acceptance criteria.
4. Identify dependencies and affected components.
5. Implement only necessary changes.
6. Add or update tests.
7. Run relevant tests and static analysis.
8. Review the complete diff.
9. Report what changed, files changed, checks run and their results, and
   remaining risks or limitations.
10. Prepare the change to become a clean pull request linked to the issue.

When requirements are ambiguous, prefer established repository conventions
and state significant assumptions explicitly.

## Core repository rules

```text
NO SIGNIFICANT FEATURE WITHOUT AN ISSUE
NO FEATURE WORK DIRECTLY ON MAIN
NO SIGNIFICANT CHANGE WITHOUT A PULL REQUEST
NO MERGE WITHOUT REQUIRED REVIEW
NO CLAIM OF COMPLETION WITHOUT VERIFICATION
```

Correctness and maintainability take priority over producing the largest
possible diff.

