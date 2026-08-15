# Repository Instructions for Coding Agents

These instructions apply to every LLM or coding agent working in this
repository.

## Required context

Before planning or editing, read these files completely:

1. `PROJECT_CONTEXT.md`
2. `TEAM_PIPELINE.md`
3. The GitHub issue or task supplied by the developer

If the task conflicts with either context file, stop and identify the conflict
before editing.

## Scope and ownership

- Work only on the supplied issue and within the stated allowed paths.
- Inspect current code; never assume another conversation's repository state.
- Preserve unrelated work and do not reformat unrelated files.
- Do not silently change shared models, state machines, service interfaces,
  URLs, permissions, payment behavior, or deployment contracts.
- Only one migration-bearing change should be in flight unless the human
  migration coordinator confirms otherwise.
- Do not merge pull requests or push directly to `main`.

## Implementation standards

- Keep business rules in domain/service functions rather than duplicating them
  across views, templates, tasks, or commands.
- Enforce critical invariants in both application logic and database
  constraints where practical.
- Use `Decimal`, never floating point, for money.
- Make external callbacks, payments, notifications, and assignment operations
  idempotent and retry-safe.
- Check authorization and object ownership server-side for every protected
  action.
- Do not log secrets, authentication tokens, payment data, identity documents,
  or unnecessary personal data.
- Add or update tests with each behavior change.
- Do not claim checks passed unless they were executed successfully.

## Before handoff

- Review the complete diff for unrelated or generated changes.
- Run the repository validation commands documented by the project.
- State exactly what changed, what was tested, and any known risk.
- Update `PROJECT_CONTEXT.md` and append its change log when implemented script
  or application behavior changes. Do not delete historical entries.
- Update architecture or runbook documentation when a contract or operational
  procedure changes.

