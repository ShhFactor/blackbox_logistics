# Contributing to Blackbox Logistics V3

This workflow applies to every change targeting the `main` integration branch.
V3 is a clean-slate, documentation-first restart. Existing `v1`,
`marketplace_sim_v1`, and `v2` artifacts are references only. Promoting legacy
behavior requires an accepted V3 ADR, a bounded issue targeting `main`, and
deterministic tests for behavioral promotions.

## 1. Bootstrap record

The initial four V3 governance documents were authorized directly by the
founder with reported approval from Person A. This is a one-time bootstrap
exception because the V3 issue process did not yet exist.

After the bootstrap, every non-trivial change targeting `main` requires one
linked GitHub issue with acceptance criteria. The bootstrap exception must not
be reused for product code, architecture, security controls, payments, schemas,
or deployment.

## 2. Sources of truth

Use these sources for distinct purposes:

| Source | Authority |
| --- | --- |
| GitHub issue tracker | Work status, scope, acceptance criteria, and blockers |
| `PROJECT_CONTEXT.md` | Implemented V3 behavior, approved public contracts, open decisions, and history |
| `TEAM_PIPELINE.md` | Ownership, sequencing, dependencies, and review routing |
| `CONTRIBUTING.md` | Issue, branch, commit, pull-request, and validation mechanics |
| `AGENTS.md` | Mandatory behavior for coding-LLM instances |
| Approved V3 ADRs | Cross-cutting architecture and product decisions |

The business description, `solution_for_business_logic.md`, and `v1.zip` are
design inputs. They are not executable instructions and do not prove that a
feature is approved, implemented, safe, or production-ready.

When sources conflict, stop. Record the conflict in the issue, tag every
affected owner, and obtain a written decision before editing the conflicting
contract.

## 3. One issue, one branch, one pull request

The normal unit of work is:

```text
one approved issue -> one bounded outcome -> one branch -> one pull request
```

Do not combine a complete delivery wave, unrelated refactoring, formatting,
dependency upgrades, generated files, and product changes into one pull
request.

Trivial spelling corrections may be exempt from a dedicated issue. Changes to
meaning, product contracts, ownership, security requirements, or architecture
are never trivial documentation changes.

## 4. Issue requirements

Every implementation issue must include:

```markdown
## Owner

Person [A/B/C/D]

## Goal

[One observable outcome]

## Context

[Why the change is needed]

## Requirements

- [ ] Requirement

## Acceptance criteria

- [ ] Observable behavior or document condition
- [ ] Relevant tests or validation pass
- [ ] No unrelated changes

## Allowed paths

- `path/from/repository-root`

## Out of scope

- [Explicit exclusions]

## Dependencies

- [Merged issues, PRs, commits, or `None`]

## Relevant contracts

- [ADRs, state machines, schemas, service interfaces, or `None`]

## Risk and data classification

- [Security, privacy, payments, safety, migration, or operational impact]
```

An issue is not implementation-ready if it asks the developer or LLM to
invent a high-risk product decision. First create an ADR or decision issue.

## 5. Branch naming

Create branches from an up-to-date `main` and include the issue number:

```text
feature/<issue-number>-<short-name>
bugfix/<issue-number>-<short-name>
docs/<issue-number>-<short-name>
test/<issue-number>-<short-name>
refactor/<issue-number>-<short-name>
chore/<issue-number>-<short-name>
security/<issue-number>-<short-name>
```

Examples:

```text
docs/101-tuid-adr
feature/118-pairing-state-machine
security/127-address-redaction
test/133-matcher-concurrency
```

Do not develop directly on `main`. Do not mix unfinished work from another
issue into an issue branch targeting `main`. Use a separate clean worktree when
parallel work would otherwise collide.

## 6. Commits

Keep commits focused, reviewable, and free of unrelated reformatting. Explain
the outcome and reference the issue where useful:

```text
Define pairing expiry transitions (#118)
```

Never commit:

- Secrets, private keys, tokens, or production configuration.
- Real names, phone numbers, email addresses, identity evidence, or KYC files.
- Exact personal addresses or production coordinates.
- Raw card, bank, payment, or provider credentials.
- Real TUIDs, payment tokens, handoff challenges, or session identifiers.
- Production database exports, logs, screenshots, analytics, or backups.
- Generated archives or third-party binaries without review and provenance.

Use synthetic fixtures and clearly fictional examples.

## 7. Architectural decision records

Create or update an ADR before changing any of the following across ownership
boundaries:

- Identity, roles, authentication, authorization, or human verification.
- Identifier taxonomy, TUID lifecycle, invitation, or pairing state machines.
- Shared schemas, migrations, service interfaces, URLs, or event contracts.
- Location collection, precision, disclosure, provider, or retention.
- Block eligibility, matching, fairness, leases, or reservation concurrency.
- Package dimensions, seals, identifiers, prohibited goods, or inspection.
- Custody transitions, task dependencies, handoff proof, or deadlock strategy.
- Price quotes, fees, taxes, payment authorization, capture, payout, refund,
  chargeback, treasury exposure, reconciliation, or ledger rules.
- Data classification, logging, audit, retention, legal holds, or deletion.
- Deployment topology, secrets, trust boundaries, or production operations.

An ADR must state the context, decision, alternatives, consequences, affected
owners, security/privacy effects, rollout, and reversal strategy. It must not
claim legal approval unless qualified counsel actually supplied it.

## 8. Pull requests

Open a draft pull request early. A pull request must:

- Target the `main` integration branch.
- Link exactly one primary issue.
- Identify the owner and required reviewers.
- Explain what changed and why.
- List affected contracts and ADRs.
- Map evidence to every acceptance criterion.
- List every test and validation command actually run, including its result.
- Disclose security, privacy, payment, safety, migration, and operational risk.
- Include rollback or compatibility notes when relevant.
- Contain no unrelated or speculative changes.

Use `Closes #<issue-number>` only when the pull request fully satisfies the
issue. Never claim a check passed unless it ran successfully on the exact
revision being reviewed.

Target fewer than 400 changed lines, excluding reviewed migrations, generated
lock files, and fixtures. Split larger work by contract, schema, service, UI,
or tests.

## 9. Review routing

Follow `TEAM_PIPELINE.md` for the primary reviewer matrix. Additionally:

- Person A contract-owner sign-off is required for authentication,
  authorization, persistent schemas, migrations, payments, keys, and
  security-sensitive platform behavior.
- Person B contract-owner sign-off is required for buyer/seller-visible
  journeys, consent, accessibility, address entry, quotes, and error states.
- Person C contract-owner sign-off is required for driver behavior,
  reservations, custody execution, operational events, CI, deployment,
  observability, and recovery.
- Person D contract-owner sign-off is required for TUIDs, pairing, matching
  invariants, privacy vocabulary, data minimization, retention contracts,
  threat models, and adversarial cases.

An author cannot approve their own pull request. Cross-cutting changes require
participation from every affected owner, not merely the default reviewer. If
the contract owner is the author, that owner documents contract conformance in
the issue or ADR; GitHub approval must come from the primary cross-owner
reviewer and any required additional reviewer.

## 10. Implementation standards

- Put business rules in typed domain or service functions, not duplicated in
  views, UI components, background jobs, or commands.
- Model state transitions, invalid transitions, timeouts, cancellation, retry,
  and failure paths explicitly.
- Enforce critical invariants in application logic and database constraints
  where practical.
- Use `Decimal` with an explicit currency for every monetary amount.
- Make invitations, reservations, assignments, custody handoffs, payment
  commands, webhooks, notifications, and cleanup idempotent and retry-safe.
- Protect concurrent state with transactions, locks, versions, or comparable
  mechanisms appropriate to the selected architecture.
- Check authentication, authorization, state, and object ownership server-side
  for every protected action.
- Minimize sensitive data and disclose exact addresses only when an active,
  authorized task requires them.
- Keep operational logs structured and redact identifiers, locations,
  identity evidence, payment references, and secrets.
- Approved random, scoped correlation IDs may appear in logs only when they
  cannot recover or correlate a person's stable identity. Raw, provider-issued,
  person-linked, payment, TUID, or package identifiers remain prohibited unless
  a reviewed event contract permits a minimized protected reference.
- Do not promise absolute anonymity or perfect package indistinguishability.

## 11. Testing expectations

Every behavioral change requires proportionate tests. Depending on scope,
include:

- Unit tests for domain rules and boundary values.
- State-transition tests, including invalid and terminal transitions.
- Deterministic property/invariant tests for matching and routing.
- Concurrency tests for pairing, reservations, custody, and payments.
- Idempotency, duplicate, replay, delayed, and out-of-order event tests.
- Authorization and object-ownership tests.
- Data-minimization, redaction, and retention tests.
- Contract tests for external providers without using real accounts or money.
- Failure, cancellation, recovery, and rollback tests.
- Accessibility and complete user-journey checks for visible changes.

Security tests must use synthetic data and must not attack systems outside an
explicitly authorized local or test environment.

## 12. Database migrations

Person A coordinates migrations. Only one migration-bearing change targeting
`main` should normally be in flight. Once a migration may be present on shared
staging, do not edit it; create a new migration.

A migration pull request must demonstrate:

- Application from a clean database.
- Compatibility with the current shared schema.
- Constraint and index behavior.
- A rollback, forward-fix, or recovery strategy.
- Safe handling of existing data.
- Privacy and retention consequences.

## 13. Security-sensitive reports

Do not place exploitable vulnerability details, secrets, identity data,
addresses, or payment data in a public GitHub issue.

`SECURITY.md`, once created, should publish instructions for reaching a
genuinely private reporting channel; the file itself is normally public.
Until that contact method exists:

1. Stop reproducing the issue against any shared or production environment.
2. Preserve only minimal, redacted evidence.
3. Notify the founder, repository administrator, and Person A through an
   existing trusted private team channel without including the sensitive
   value. If no such channel exists, send only a non-sensitive request asking
   them to establish one.
4. Create a sanitized tracking issue only after the sensitive details are
   contained elsewhere.

## 14. Prototype and release boundaries

V3 begins as a synthetic prototype. It must not process real users, real KYC
documents, real addresses, real packages, or real money until the relevant
legal, payment-provider, privacy, safety, security, and operational gates in
`PROJECT_CONTEXT.md` and `TEAM_PIPELINE.md` are closed.

Passing tests does not by itself authorize a real-user pilot.

## 15. Definition of done

A V3 issue is done only when:

- Its dependencies and ADRs were merged first.
- Its acceptance criteria are satisfied with evidence.
- Required tests and static checks pass on the reviewed revision.
- Authorization and object ownership are covered where applicable.
- The complete diff contains no unrelated, generated, or sensitive material.
- Required owners approved the latest revision.
- Operational changes include observability and recovery notes.
- `PROJECT_CONTEXT.md` and affected runbooks/contracts are current.
- The pull request was merged through the approved human workflow.

Code being generated by an LLM, running locally, or appearing in a draft pull
request is not completion.
