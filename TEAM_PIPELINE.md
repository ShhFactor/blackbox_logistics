# Three-Person Delivery Pipeline

This playbook coordinates three developers who each use a separate LLM coding
instance. It is the operating agreement for turning the simulator into a
production marketplace without overlapping work or losing architectural
context.

## 1. Shared product assumption

The first release is an India-focused marketplace for physical goods with a
single driver responsible for each delivery. Multi-driver handoffs remain a
simulation/research feature until the single-driver workflow is stable.

The first production architecture is a modular Django monolith backed by
PostgreSQL. Do not create independently deployed microservices during the MVP.

## 2. Ownership

### Person A — Platform and data owner

Owns:

- Django project scaffold and settings
- Accounts, authentication, roles, and permissions
- Shared domain conventions and database schema governance
- Payment records, provider webhooks, refunds, and payout records
- Security-sensitive code and migration review
- Architectural decision records

Primary directories once the Django project exists:

- `config/`
- `apps/accounts/`
- `apps/core/`
- `apps/payments/`
- `docs/architecture/`

Person A is the migration coordinator. Other people may propose model changes,
but only one migration-bearing PR may be in flight at a time unless Person A
explicitly confirms the migrations are independent.

### Person B — Marketplace and user experience owner

Owns:

- Product catalog, categories, images, and inventory screens
- Buyer cart and checkout experience
- Seller dashboard and order-management experience
- Order presentation, cancellation, return, and review flows
- Templates, frontend assets, accessibility, and responsive behavior
- End-to-end acceptance scenarios for buyers and sellers

Primary directories:

- `apps/catalog/`
- `apps/orders/`
- `apps/sellers/`
- `templates/`
- `static/`

Person B must not duplicate authorization or payment logic in views. Those
capabilities are consumed through interfaces owned by Person A.

### Person C — Logistics, quality, and operations owner

Owns:

- Extraction and tests for the existing simulator
- Drivers, availability, deliveries, assignments, and status events
- Driver-facing responsive/PWA screens
- Concurrency and assignment invariant tests
- CI, deployment configuration, health checks, logging, and runbooks
- Staging smoke tests, backups, restoration checks, and observability

Primary directories:

- `apps/drivers/`
- `apps/deliveries/`
- `simulation/`
- `tests/`
- `.github/workflows/`
- `deploy/`
- `docs/runbooks/`

Person C does not independently change shared user or order semantics. Changes
to those contracts are agreed with the owning person before implementation.

## 3. Delivery waves

Every numbered item below becomes its own GitHub issue and normally its own
pull request. Do not combine an entire wave into one PR.

### Wave 0 — Team foundation

Work can begin immediately:

| Owner | Work item | Depends on | Exit condition |
|---|---|---|---|
| A | A0.1 Django 5.2 LTS project, environment-based settings, PostgreSQL, Docker | None | Server starts; initial checks pass |
| B | B0.1 Buyer, seller, driver, and operator journeys plus initial wireframes | None | Journeys and acceptance criteria are documented |
| C | C0.1 Move the simulator into an importable module and add deterministic regression tests | None | Existing behavior is covered without changing it |
| C | C0.2 Add CI for formatting, linting, tests, and Django deployment checks | A0.1 | Required checks run on pull requests |

Merge order: A0.1 and C0.1 may merge in either order if they touch separate
paths. C0.2 follows A0.1. B0.1 is documentation-only and can merge at any time.

### Wave 1 — Identity and catalog

| Owner | Work item | Depends on | Exit condition |
|---|---|---|---|
| A | A1.1 Custom user model, roles, profiles, addresses, login, logout, password reset | A0.1 | Permission tests cover all roles |
| A | A1.2 Audit-event foundation and reusable authorization helpers | A1.1 | Sensitive actions create audit records |
| B | B1.1 Categories, products, images, and public catalog | A1.1 | Buyer can browse product detail pages |
| B | B1.2 Seller product and inventory management | B1.1 | Seller can manage only their own records |
| C | C1.1 Driver profile and availability workflow | A1.1 | Verified driver can go online/offline |
| C | C1.2 Staging deployment, health endpoint, and smoke test | C0.2 | Every merge to main deploys to staging |

Person A merges A1.1 before B1.1 or C1.1 begins implementation. B and C may
prepare designs and test cases while waiting.

### Wave 2 — Orders and delivery

| Owner | Work item | Depends on | Exit condition |
|---|---|---|---|
| A | A2.1 Order and order-item schema, money rules, state-transition service | B1.2 | Invalid transitions are rejected and audited |
| B | B2.1 Cart and checkout preparation | A2.1 | Cart produces a server-validated order quote |
| B | B2.2 Seller order acceptance and packing workflow | A2.1 | Seller sees and updates only owned orders |
| C | C2.1 Delivery, status event, and assignment schema | A2.1, C1.1 | Order can create one delivery safely |
| C | C2.2 Transactional driver assignment service | C2.1 | Concurrent tests prove capacity is not exceeded |
| C | C2.3 Driver pickup, transit, OTP delivery, and failure screens | C2.2 | Full delivery lifecycle works in staging |

A2.1 establishes the order contract. B and C should review it before it merges
because their work depends on it.

### Wave 3 — Payments and operational completeness

| Owner | Work item | Depends on | Exit condition |
|---|---|---|---|
| A | A3.1 Payment provider sandbox checkout and signed webhook ingestion | B2.1 | Duplicate webhooks are safe and tested |
| A | A3.2 Refund, transfer, commission, and reconciliation records | A3.1 | Refund and payout states reconcile |
| B | B3.1 Buyer order timeline, cancellation, returns, reviews, and support tickets | B2.1, C2.3 | Buyer lifecycle is complete |
| B | B3.2 Seller sales, fees, refunds, and payout views | A3.2 | Seller can reconcile an order |
| C | C3.1 Notifications and retryable background jobs | A3.1, C2.3 | Failed jobs retry without duplicate effects |
| C | C3.2 Operations dashboards and exception-handling runbooks | B3.1, C3.1 | Operators can resolve documented failures |

### Wave 4 — Production readiness and beta

| Owner | Work item | Depends on | Exit condition |
|---|---|---|---|
| A | A4.1 Security review, privacy controls, retention, export, and deletion | Wave 3 | Security checklist and tests pass |
| B | B4.1 Accessibility, responsive QA, empty/error states, and onboarding polish | Wave 3 | Critical journeys pass manual QA |
| C | C4.1 Production deployment, monitoring, alerts, backups, and restore drill | Wave 3 | Restore and rollback are demonstrated |
| All | A4.2/B4.2/C4.2 Limited beta and incident rotation | A4.1, B4.1, C4.1 | Beta exit metrics are reviewed |

No multi-driver handoff work enters the roadmap before Wave 4 is complete.

## 4. Daily development loop

Each person follows this sequence:

1. Select one assigned GitHub issue with written acceptance criteria.
2. Confirm that its dependencies have merged into `main`.
3. Pull `main`, then create `feature/<issue-number>-<short-name>` or
   `bugfix/<issue-number>-<short-name>` as defined in `CONTRIBUTING.md`.
4. Start the LLM instance with the prompt contract in section 5.
5. Ask the LLM to inspect existing code and propose a short plan before edits.
6. Implement only the issue scope and add tests with the implementation.
7. Run the repository's complete local validation command.
8. Review the diff manually. Remove unrelated, generated, or speculative work.
9. Push and open a draft PR early.
10. Mark it ready only when CI passes and the PR checklist is complete.
11. Address review comments in focused commits and re-request review.
12. Squash-merge after approval; delete the branch; update local `main`.

Never give an LLM permission to merge its own pull request.

## 5. Prompt contract for every LLM instance

Copy this structure into each new coding conversation:

```text
Read AGENTS.md, PROJECT_CONTEXT.md, TEAM_PIPELINE.md, and CONTRIBUTING.md
completely.

My role: Person [A/B/C]
GitHub issue: #[number] — [title]
Objective: [one outcome]
Acceptance criteria:
- [criterion]
- [criterion]

Allowed paths: [directories]
Out-of-scope paths: [directories or concerns]
Dependencies already merged: [PRs/commits]
Relevant contracts: [models/services/ADRs]

Before editing, inspect the repository and give me:
1. files you expect to change,
2. tests you will add or update,
3. risks or contract conflicts.

Do not change unrelated files, create speculative abstractions, alter public
contracts silently, commit secrets, merge the PR, or claim a test passed unless
you ran it. Update PROJECT_CONTEXT.md only when implemented behavior changes.
```

Keep one LLM conversation per issue. A new issue starts with a fresh instance
and current repository context; do not rely on memory from an earlier chat.

## 6. Pull request routing

| PR author | Required primary reviewer | Additional reviewer when needed |
|---|---|---|
| Person A | Person B | Person C for deployment/operations impact |
| Person B | Person C | Person A for schema, permissions, or payments |
| Person C | Person A | Person B for user-facing behavior |

An author cannot approve their own PR. Any PR touching authentication,
authorization, payments, shared models, migrations, CI, or production deployment
requires review from that area's owner.

Target PR size is under 400 changed lines excluding migrations, snapshots, and
generated lock files. Above that size, split by schema, service, UI, or tests.

## 7. Contract-change protocol

Before changing a model, state machine, service signature, URL contract, or
shared template context:

1. Open or update the issue with the proposed before/after contract.
2. Tag affected owners.
3. Obtain written agreement from at least one affected owner.
4. Record a durable architectural decision under `docs/architecture/` if the
   choice affects multiple future features.
5. Merge the contract/schema PR before dependent implementation PRs.

Database migrations are append-only after reaching shared staging. Never edit a
migration that another person's branch may already depend on; create a new one.

## 8. Merge gates

A PR may merge only when:

- It links exactly one primary issue.
- Acceptance criteria are demonstrably satisfied.
- Tests were added or the PR explains why none are needed.
- Formatting, lint, unit, integration, and security checks pass.
- New migrations apply from a clean database and against the current schema.
- Authorization and object ownership were tested where relevant.
- User-facing changes include screenshots or a short recording.
- Operational changes include rollback and observability notes.
- Documentation and `PROJECT_CONTEXT.md` are current when behavior changed.
- All blocking conversations are resolved.
- The required human reviewer approved the latest revision.

Use squash merge so one issue produces one coherent commit on `main`.

## 9. GitHub repository settings

Protect `main` with:

- Pull requests required before merging
- One approving review
- Dismiss stale approvals after new code is pushed
- Approval of the most recent reviewable push
- Required status checks
- All conversations resolved
- No force pushes or branch deletion
- No administrator bypass during normal work
- Squash merge enabled; direct pushes disabled

Add `CODEOWNERS` after the three GitHub usernames are known. Map the primary
directories in section 2 to their owners and protect `.github/CODEOWNERS`
itself with the repository administrator as owner.

## 10. Coordination cadence

- Ten-minute daily sync: merged yesterday, issue today, blocker/contract change.
- Twice-weekly integration review on staging using complete user journeys.
- Weekly backlog and architecture review; no architecture decisions in private
  LLM chats only.
- Weekly third-party dependency, security, and production-readiness review once
  Wave 3 begins.

The issue tracker is the source of truth for work status. This file is the
source of truth for ownership and delivery order. `CONTRIBUTING.md` is the
source of truth for repository-wide issue, branch, commit, and pull-request
mechanics. `PROJECT_CONTEXT.md` is the source of truth for implemented product
behavior and history.

