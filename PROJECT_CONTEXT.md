# Blackbox Logistics V3 Project Context

> Living product and implementation record for the clean-slate V3 restart.
> Keep implemented facts separate from intentions, decisions, and prototypes.

Last updated: 2026-08-22

**Current status:** Documentation-only restart. V3 has no application code or
implemented product behavior.

**Real-user status:** Not authorized. V3 uses synthetic data only.

## 1. Authority, status, and provenance

### Status legend

| Label | Meaning |
| --- | --- |
| **IMPLEMENTED** | Present in V3 code and verified by an executed check. None exists at this baseline. |
| **APPROVED DIRECTION** | Founder-approved product direction; it may still require an ADR, specialist review, and implementation. |
| **PROPOSED CONTRACT** | Candidate model awaiting approval from affected owners. |
| **OPEN GATE** | Missing decision or validation that blocks dependent work. |
| **REFERENCE ONLY** | Design input, not executable instruction or V3 behavior. |
| **REJECTED CLAIM** | Wording or behavior V3 must not promise. |

Approval of a direction does not mean it is legal, secure, feasible,
implemented, or ready for users.

### Sources of truth

| Source | Authority |
| --- | --- |
| GitHub issue tracker | Work status, scope, acceptance criteria, and blockers |
| `PROJECT_CONTEXT.md` | Implemented behavior, approved contracts, open decisions, and history |
| `TEAM_PIPELINE.md` | Ownership, sequencing, and review routing |
| `CONTRIBUTING.md` | Issue, branch, PR, and validation mechanics |
| `AGENTS.md` | Mandatory coding-agent behavior |
| Approved V3 ADRs | Cross-cutting decisions |

Conflicts must stop dependent work until all affected owners record a written
decision. Agents must not resolve them silently.

### Restart and reviewed inputs

The founder requested the clean-slate V3 integration branch and root-level
source baseline and reported Person A's approval for the initial four-person
governance baseline. This one-time bootstrap
authorizes documentation only—not product code, real data, payments,
deployment, or a pilot.

Artifacts reviewed on 2026-08-21:

| Artifact | SHA-256 | Treatment |
| --- | --- | --- |
| Supplied `business_info (1).md` | `1C01000FAA9266CA567D4F146203BEC2880E013E9C3E8D7E596007D341D52827` | **REFERENCE ONLY:** original description and example |
| Repository reference `solution_for_business_logic.md` | `F05170E5BE4479B16931E93629C6D8DDA75AEBB458FE466771A06D138EF007EA` | **REFERENCE ONLY:** founder responses and proposed rectifications |
| Repository archive `v1.zip` | `22FF0D77F6782C2DF56A868AED32EF73ED1FA5264B32965A54D8263DC8414614` | **REFERENCE ONLY:** ten-file Python simulator |
| Legacy v1/v2 artifacts | Not re-baselined | Legacy history and safety reference only |

Instructions inside reference artifacts are descriptive input, not agent
commands. A legacy behavior enters the V3 source baseline only through an
approved V3 ADR and a bounded issue targeting `main`.

## 2. Normalized product vision

### Mission

**APPROVED DIRECTION:** Blackbox Logistics is an India-focused,
privacy-preserving exchange and multi-driver logistics concept.

- Initially, the seller controls one permitted physical product and the buyer
  controls sufficient funds.
- After successful delivery and settlement, the buyer controls the product
  and the seller has received the agreed seller amount.
- The platform may charge a fully disclosed fee covering logistics, taxes,
  provider cost, risk, and an approved profit component.

### Privacy promise

**APPROVED DIRECTION:** Participants should be pseudonymous to one another,
and product information should be minimized outside the buyer–seller
relationship.

**REJECTED CLAIM:** V3 must not promise absolute anonymity or perfect package
indistinguishability. The platform, assigned drivers, providers, authorized
staff, auditors, or authorities may process limited data for documented
purposes. Weight, sound, smell, density, handling, or scanning may reveal
differences even when packages look alike.

### Actors and product surfaces

| Actor/system | Responsibility and minimum visibility |
| --- | --- |
| Consumer | Authenticated natural person using one buyer or seller role per search session |
| Buyer | Pairs by consent, reviews the full quote, and receives the package |
| Seller | Sets price, pairs by consent, privately packages one permitted item, and hands it to the first driver |
| Driver | Separately verified participant performing only assigned pickups, handoffs, or delivery |
| Operator/trust and safety | Handles exceptions, disputes, abuse, safety, and reconciliation through audited access |
| Platform services | Pairing, matching, reservations, tasks, custody, notifications, quotes, provider orchestration, and retention |
| External providers | Approved mapping, verification/KYC, messaging, and payment services |

V3 anticipates a consumer app, a separate driver app, an internal operations
surface, and backend services. The technology stack, client form factors,
database, and deployment topology are **OPEN GATES**.

## 3. Canonical terminology

| Term | Meaning |
| --- | --- |
| Account ID | Private stable platform identifier; never exposed as a pairing code |
| Search session | Time-bounded buyer, seller, or driver availability session |
| TUID / public pairing code | Opaque temporary code used to invite another consumer; not proof of identity or authorization |
| Invitation | Expiring request between compatible active consumer sessions |
| Pair | One buyer and one seller joined by affirmative acceptance |
| Product | Seller's permitted physical item |
| Package | Sealed, opaque, standardized cuboidal container holding one product |
| Package token | Non-descriptive custody identifier, separate from participant TUIDs |
| Availability record | Minimal, expiring pair or driver representation offered to matching |
| Block | Operational group of three pairs and five drivers; not a blockchain object |
| Transaction | One seller-to-buyer product movement inside a block |
| Allocation | Side-effect-free proposed driver assignment |
| Reservation | Atomic claim preventing duplicate block participation |
| Task | Typed work item with executor, package, prerequisites, status, expiry, and idempotency key |
| Handoff | Atomic transfer between authorized custodians |
| Quote | Server-calculated seller amount, fees, taxes, and total in one currency |
| Payment reference | Provider token or identifier, not raw bank/card data |

TUID must not be reused as an account, product, package, block, transaction,
task, payment, or handoff-challenge identifier.

## 4. Approved directions and unresolved gates

### Approved product directions

These directions remain unimplemented:

1. A consumer passes a privacy-preserving human check, chooses buyer or
   seller, supplies the role-appropriate address information, and starts a
   time-bounded search. A seller also supplies a price.
2. Either side may enter the other's TUID. The recipient accepts or declines;
   decline returns valid participants to searching, while abandon closes the
   session.
3. An accepted pair becomes eligible for matching.
4. A block targets three distinct pairs and five nearby, eligible drivers.
5. Each pair has one transaction with three distinct drivers. Every block
   driver appears at least once and at most twice, forcing sorted counts
   `[1, 2, 2, 2, 2]` across nine driver slots.
6. The package is a nominal `10 × 12 × 10 inch` cuboid. The seller
   privately seals the product in an opaque, tamper-evident kit before pickup.
7. Packages should look consistent and carry no product-description label.
   A minimal, non-descriptive custody mark is a **PROPOSED CONTRACT** for
   distinguishing visually uniform packages. V3-ADR-005 must decide whether
   it is required, its technology, and any safety markings without exposing
   product, participant, price, or address data.
8. Only goods allowed by an approved India-specific policy may enter the
   system. “Anything” is not an acceptable goods rule.
9. The buyer sees and accepts seller price, fee, taxes, and total before
   dispatch or financial commitment.
10. Hosted/tokenized provider flows replace raw bank/card collection.
11. The desired commercial outcome is prompt seller access to funds after
    verified pickup while the buyer's final payment occurs after verified
    receipt. This goal is not yet an approved payment implementation.
12. Drivers undergo an approved KYC/eligibility process. Aadhaar cannot be
    assumed mandatory or used as the application identifier.
13. Exact locations and ephemeral identifiers are purged promptly when no
    longer needed; payment, tax, custody, dispute, security, and legal-hold
    records follow an approved retention matrix.
14. The synthetic prototype targets a globally acyclic custody dependency
    graph with topological validation. V3-ADR-007 must define its construction,
    ranking, rendezvous, failure, and recovery rules before implementation.

### Open gates

No dependent implementation may invent answers to these:

- Architecture, persistence, APIs/events, client technology, and deployment.
- Identity, consumer human checks, driver KYC, eligibility, recovery, and
  privileged access.
- TUID entropy/storage/expiry, invitations, cross-invite races, cancellation,
  replay, spam, and account farming.
- India-specific goods policy, package internal/external dimensions,
  tolerance, maximum weight, materials, seals, markings, inspection, and
  physical testing.
- “Nearby,” coarse versus exact location, service areas, fairness, maximum
  wait, route feasibility, leases, and concurrent reservation.
- Acyclic dependency construction, topological validation, rendezvous,
  custody proof, replacement drivers, failures, returns, and emergencies.
- Fee estimation, buyer authorization/capture, seller payout, treasury risk,
  provider selection, refunds, disputes, chargebacks, reconciliation, taxes,
  insurance, and driver compensation.
- Data classification, retention durations, legal holds, audit evidence,
  device/cache/provider deletion, and backup expiry.
- Threat-model approval and legal, payment-provider, packaging, safety,
  privacy, security, operational, and pilot-readiness reviews.

## 5. Candidate state machines and invariants

Everything here is a **PROPOSED CONTRACT** for ADR review. Nothing is
implemented.

### Candidate state machines

```text
Pairing:
IDLE -> HUMAN_CHECK_PENDING -> ROLE_SELECTED -> SEARCHING
     -> INVITATION_PENDING -> PAIRED -> RESERVED -> CLOSED

Driver eligibility:
PENDING -> VERIFIED -> EXPIRED | SUSPENDED | REJECTED

Driver availability:
OFFLINE -> AVAILABLE -> RESERVED -> EXECUTING -> AVAILABLE | OFFLINE

Block:
FORMING -> RESERVED -> READY -> EXECUTING -> SETTLEMENT_PENDING
        -> COMPLETED -> RETENTION_PENDING -> EPHEMERAL_DATA_PURGED

Package custody:
DECLARED -> SELLER_PACKAGING -> SEALED -> PICKUP_READY -> IN_CUSTODY
         -> HANDOFF_PENDING -> IN_CUSTODY -> DELIVERED -> ACCEPTED

Task:
BLOCKED -> READY -> ACCEPTED -> ARRIVED -> HANDOFF_PENDING -> COMPLETED

Money:
QUOTE_DRAFT -> QUOTED -> QUOTE_ACCEPTED

Buyer obligation:
AUTHORIZATION_PENDING -> AUTHORIZED -> CAPTURE_PENDING -> CAPTURED

Seller payment:
PAYOUT_PENDING -> PAYOUT_INITIATED -> SELLER_PAID

Financial completion:
FINANCIAL_PENDING -> RECONCILING -> SETTLED
```

Required side states include expiry, cancellation, failure, suspension,
dispute, refund/reversal, quarantine, damage, loss, refusal, return, and legal
hold. The payment ADR must determine buyer authorization/capture and seller
payout timing; logistics completion is not payment proof.

### Pairing and matching invariants

- A participant has at most one active buyer/seller role, pair, and reserved
  block at a time.
- Pair acceptance atomically validates both roles and active sessions,
  consumes one invitation, and prevents double pairing.
- TUIDs use a cryptographically secure source, at least 128 bits of
  unpredictability, scope, expiry, successful-use invalidation, rate limits,
  and log redaction. Knowing one never replaces authentication or
  authorization.
- A ready block has exactly three distinct pairs and five distinct verified,
  available drivers.
- One transaction has one seller, one package, three distinct drivers, and one
  buyer; block driver counts sort to `[1, 2, 2, 2, 2]`.
- Allocation is side-effect-free. Reservation is transactional, leased,
  idempotent, and concurrency-safe.
- “Nearby” is an approved policy over coarse geography, time, route,
  capacity, safety, fairness, and wait—not address-string equality.
- Simulation randomness is injectable and deterministic in tests. Security
  tokens use a separate cryptographic source.

### Task and custody invariants

- Production tasks are typed records, not positional tuples or dictionary
  order. A task has one executor, block/transaction, package, action,
  prerequisites, location policy, status, expiry, and idempotency key.
- The complete dependency graph must be acyclic and executable before a block
  starts. Its approved construction and rendezvous rules replace the prototype
  priority list.
- A package has exactly one custodian or explicit holding/terminal state.
- Handoffs are atomic, replay-resistant confirmations that change custody
  once and append a minimized audit event.
- A reciprocal driver rendezvous is one coordinated operation, not two
  unrelated completions.
- Exact locations are revealed just in time only to the executor of an active
  task and revoked when no longer required.

### Product, money, and retention invariants

- One transaction carries one declared, permitted product in one approved
  seller-sealed package.
- Ordinary drivers do not open packages. Package and custody identifiers
  disclose no product, participant, address, price, or TUID.
- Money uses `Decimal` semantics, explicit currency, immutable quote
  components, server calculation, provider references, and idempotent,
  authenticated callbacks.
- Seller payout, buyer obligation/capture, refund, chargeback, driver
  compensation, platform revenue, and treasury exposure are separate ledger
  concepts.
- Task completion, delivery acceptance, buyer payment, seller payout, block
  completion, and cleanup are separate predicates.
- Cleanup is idempotent and field-specific. App reset is not proof of deletion
  from servers, devices, logs, providers, caches, analytics, or backups.

## 6. Security, privacy, packaging, and payment baseline

### Data and security

Restricted data includes identity/KYC evidence, exact location, account-to-
TUID mapping, custody proof, payment references, and secrets. Coarse region,
quotes, and pseudonymous operational state remain confidential.

- Use synthetic identities, locations, payment references, and packages in
  code, tests, logs, screenshots, demos, issues, and LLM prompts.
- Authenticate protected requests and enforce role, ownership, state, and
  purpose server-side.
- Require strong driver/operator authentication and define session
  revocation, credential recovery, device loss, suspension, and least
  privilege.
- Encrypt transport/storage, keep secrets outside source control, rotate
  credentials, minimize data, redact logs, and audit restricted-data access
  without copying restricted values.
- Reveal exact locations only for active tasks. Detect invitation abuse, TUID
  guessing, location spoofing, fake handoffs, collusion, theft, substitution,
  no-shows, and payment abuse.
- Define dangerous-package, unsafe-address, harassment, incident, breach, and
  emergency procedures before physical testing.

### Packaging and goods

The seller uses a visually standardized, opaque, tamper-evident cuboid. It may
reduce casual visual inference but cannot guarantee indistinguishability.

The package ADR must set the dimensional interpretation, tolerance, weight,
material, closure, seal, custody mark, required markings, durability, reuse,
disposal, supplier cost, and driver-handling limits. Applicable law, safety,
provider/carrier restrictions, insurability, reliability, and privacy take
priority over profit optimization.

The goods policy must cover prohibited, restricted, dangerous, illegal,
perishable, temperature-controlled, age-restricted, counterfeit, stolen, and
review-only goods, plus declarations, enforcement, quarantine, return, and
evidence handling. Qualified India-specific review is required before any
physical use.

### Payment

Paying the seller after pickup while collecting from the buyer after delivery
creates treasury, fraud, chargeback, liquidity, and regulatory exposure. No
implementation may assume this flow is viable.

Approval requires qualified India-specific advice, an authorized willing
provider, documented funds flow, buyer authorization rules, a precise payout
milestone, loss allocation, reserves, reconciliation, accounting/tax,
insurance, and failure/refund/dispute behavior. Distance-based fees require a
disclosed estimate and adjustment policy, not a surprise doorstep charge.

Until those gates close, payment work is limited to synthetic domain models,
provider-sandbox research, threat modeling, and tests. Future implementations
must store provider references, never raw bank/card credentials.

## 7. V1 prototype characterization

The reviewed archive contains `config.py`, `display.py`,
`main.py`, `names.py`, `people.py`,
`priority.py`, `rectangle_value.py`,
`tasks.py`, `addresses.py`, and
`assignment.py`.

Useful **REFERENCE ONLY** properties:

- Three synthetic pairs, five drivers, three drivers per transaction, and a
  two-transaction maximum per driver.
- Unique names and letter “addresses,” retry-based random assignment,
  position-derived priority, passive handoff tuples, and a three-corner map.

Important limitations:

- It is a standard-library console simulation, not a V3 service or scheduler.
- It has no package API, included tests, deterministic RNG injection,
  persistence, concurrency, auth, location model, payment, custody state,
  privacy controls, retention, or recovery.
- Independent chain shuffles permit opposite handoffs and longer cycles.
- `sqrt(x² + y²)` scores chain positions, not travel, time, safety,
  or task readiness. Linked-list/dictionary order cannot coordinate people.
- Task tuples lack IDs, executors, dependencies, state, authorization, expiry,
  and atomic confirmation. Letter addresses are not geospatial data.
- The rectangle helper omits the fourth corner and is not a package model.

No v1 code was copied into the V3 source baseline. Promotion requires an
approved ADR, bounded issue, and deterministic tests.

## 8. Explicitly not implemented

V3 currently has no:

- Application code, executable, dependencies, framework, database, migration,
  API/event contract, worker, client UI, or operator UI.
- Accounts, auth, KYC, roles, permissions, TUIDs, invitations, pairing, maps,
  matching, reservations, block/task scheduler, custody, or recovery.
- Goods policy, package specification or procurement, quote, fee, payment,
  payout, ledger, refund, dispute, reconciliation, or driver compensation.
- Retention matrix, purge, legal hold, audit service, incident response, CI,
  tests, security scans, deployment, observability, backup, or runbook.
- Legal opinion, provider approval, physical test, insurance, penetration
  test, threat-model sign-off, or authorization for real people, goods, or
  money.

Governance documentation is not implemented product behavior.

## 9. ADR and decision register

| ID | Decision | Required owners | Status |
| --- | --- | --- | --- |
| V3-ADR-000 | Clean-slate boundary, source hierarchy, synthetic-only bootstrap | A, B, C, D, founder | **APPROVED DIRECTION**; formal ADR pending |
| V3-ADR-001 | Architecture, data, clients, events, and deployment | A, C; review B, D | **OPEN GATE** |
| V3-ADR-002 | Identity, human check, driver KYC, roles, and recovery | A, D; review B, C | **OPEN GATE** |
| V3-ADR-003 | Identifier taxonomy, TUIDs, invitation/pairing state | D, A; review B | **OPEN GATE** |
| V3-ADR-004 | Privacy promise, visibility, location, providers, retention/deletion | D, A; review B, C | **OPEN GATE** |
| V3-ADR-005 | Package, seal/token, goods policy, inspection, physical safety | D, C; review A, B, specialists | **OPEN GATE** |
| V3-ADR-006 | Geospatial matching, fairness, leases, and reservations | D, C; review A, B | **OPEN GATE** |
| V3-ADR-007 | Acyclic task-graph construction, rendezvous, custody, failure/recovery | C, D; review A, B | **APPROVED DIRECTION** for a DAG; detailed contract is an **OPEN GATE** |
| V3-ADR-008 | Quote, fee, authorization/capture, payout, treasury, ledger, disputes | A; review B, C, D, counsel/provider | **OPEN GATE** |
| V3-ADR-009 | Abuse, safety, support, incident and law-enforcement processes | D; review A, B, C, specialists | **OPEN GATE** |
| V3-ADR-010 | V1 disposition and promoted prototype contracts | C, D; review A, B | **OPEN GATE** |
| V3-ADR-011 | Real-user pilot evidence, limits, rollback, and incident ownership | All, founder, qualified reviewers | **OPEN GATE** |

Downstream issues must cite blocking ADRs. An LLM assumption cannot replace a
missing decision.

## 10. Validation and append-only history

### Bootstrap validation

Completed:

- Read the supplied business and solution references completely.
- Inspected every file in `v1.zip` without copying it into the V3 source
  baseline.
- Recorded SHA-256 provenance for all three inputs.
- Checked this file for the distinction between implemented facts, approved
  direction, proposed contracts, and open gates.
- Git whitespace validation for this file passed.

Not performed:

- V1 was not executed.
- No V3 application test exists or ran because V3 has no application code.
- No external legal source, provider contract, packaging standard, security
  control, or real-user workflow was validated by this documentation task.

### Append-only change log

Do not delete or rewrite historical entries. Append a correction that names
the superseded statement.

#### 2026-08-21 — V3 context bootstrap

- Created this documentation-only context after the founder reported Person
  A's approval.
- Recorded the three supplied artifacts as versioned design references.
- Normalized the vision, actors, terminology, decisions, candidate state
  machines/invariants, constraints, prototype limits, and ADR gates.
- Recorded that V3 has no application code or implemented behavior and uses
  synthetic data only.

#### 2026-08-22 — Root-level V3 source promotion

- Promoted the four authoritative V3 governance documents to repository-root
  paths on the `v3` integration branch.
- Defined V3 as a product/version and `v3` as the protected integration branch,
  rather than representing V3 through a dedicated source subdirectory.
- Required issue branches and pull requests to start from and target `v3`.
- No application behavior was implemented or changed.

#### 2026-08-22 — Main adopted as the V3 integration branch

- Superseded the branch-routing statements in the root-level V3 source
  promotion entry: `main` is now the protected V3 integration branch.
- Recorded `v3-(main-backup)` as a historical backup of the earlier repository,
  not a development or pull-request target.
- Required issue branches to start from `main` and pull requests to target
  `main`.
- Kept the V3 product name, roadmap, contracts, and ADR identifiers unchanged.
