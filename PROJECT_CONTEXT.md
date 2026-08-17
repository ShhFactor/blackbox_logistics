# PROJECT_CONTEXT.md

> Living context file for the **Marketplace Transaction Simulator** project.
> Multiple people (and multiple separate chat instances) work on this — **update
> this file whenever the project changes** so anyone can pick up full context
> without re-reading old conversations. Append to the Change Log, don't delete
> old entries.

Last updated: 2026-08-18

---

## 1. What this project is

A small Python project that simulates a marketplace with buyers, sellers,
and delivery drivers. It derives a "priority" ordering of the drivers from
how deliveries played out, builds each driver's task list (who they receive
each product from, who they hand it on to, and now each party's address),
and separately hosts an unrelated rectangle-corner-value utility.

No third-party dependencies — the project uses only the Python standard
library.

---

## 2. Repo layout

```
blackbox_logistics/
├── PROJECT_CONTEXT.md
├── AGENTS.md
├── TEAM_PIPELINE.md
├── CONTRIBUTING.md
├── .github/
│   ├── ISSUE_TEMPLATE/implementation-task.md
│   ├── ISSUE_TEMPLATE/bug-report.md
│   └── PULL_REQUEST_TEMPLATE.md
├── marketplace_sim_v1/
    ├── __init__.py         # public package API: SimulationResult, run_simulation
    ├── simulator.py        # computation-only orchestration for one full run
    ├── config.py           # shared constants
    ├── names.py            # the 100-name pool
    ├── people.py           # picks buyers/sellers/drivers, builds transaction records
    ├── addresses.py        # NEW: unique random address letter per person node
    ├── assignment.py       # capacity-constrained random driver assignment
    ├── priority.py         # position hashmap -> priority value -> priority linked list
    ├── tasks.py            # driver task hashmap (hand-off tuples, now with addresses)
    ├── rectangle_value.py  # random rectangle corner value assignment (see §5)
    ├── display.py          # all console-output formatting
    └── main.py             # compatibility-preserving console entry point
└── tests/
    └── test_simulator.py   # deterministic standard-library regression suite
```

**As of Update 6, the project is no longer a single file.** It was
previously one script (`marketplace_sim_v1.py`); that file was replaced by
the module set above and should be deleted locally if it still exists.

---

## 3. Team delivery workflow

- `TEAM_PIPELINE.md` is the source of truth for the three-person work split,
  delivery order, review routing, and merge gates.
- `CONTRIBUTING.md` is the source of truth for issue, branch, commit, and
  pull-request mechanics used by all contributors.
- `AGENTS.md` contains mandatory instructions for every LLM coding instance.
- `.github/ISSUE_TEMPLATE/implementation-task.md` defines bounded work items.
- `.github/ISSUE_TEMPLATE/bug-report.md` defines reproducible defect reports.
- `.github/PULL_REQUEST_TEMPLATE.md` standardizes acceptance evidence, testing,
  risk disclosure, and review readiness.
- C0.1 exposes the simulator through `marketplace_sim_v1.run_simulation()`;
  this structured API is the behavioral source for future application work.
- `rectangle_value.py` and its `main.py` integration (§5) have not been
  reviewed or tested by Claude — only the spec is documented there. Worth
  a review pass against the acceptance tests in §5 when convenient.

---

## 4. Current spec

1. **Name pool**: `NAME_POOL` (`names.py`) — exactly 100 unique Indian
   names, hardcoded.
2. **Buyers/Sellers**: pick 6 unique names from the pool to form 3 pairs:
   `(B1, S1)`, `(B2, S2)`, `(B3, S3)`.
3. **Drivers**: pick 5 more unique names from the pool (disjoint from the
   6 above) — labeled `D1`..`D5`.
4. **Initial hashmap**: `{D1: 0, D2: 0, D3: 0, D4: 0, D5: 0}`.
5. **Transactions**: build exactly 3 transactions. Each is a chain of the
   form `S_i -> D -> D -> D -> B_i`, using exactly 3 **distinct** drivers
   chosen at random for that transaction.
6. **Capacity constraint**: every time a driver appears in any chain, their
   hashmap count is incremented by 1. **No driver's total count may ever
   exceed 2** across all 3 transactions. (Math note: 3 transactions × 3
   driver-slots = 9 total assignments over 5 drivers with a max of 2 each —
   always feasible, and it forces exactly one driver to end at count 1 while
   the other four end at count 2.)
7. **Driver position hashmap** `{driver: (x, y)}` — derived from the
   transaction output above:
   - Scan Transaction 1 → 2 → 3, left to right within each chain.
   - A driver's "position in transaction" = its index in the full 5-slot
     chain `S(0) -> D(1) -> D(2) -> D(3) -> B(4)`, indexed from 0. (So a
     driver is always at position 1, 2, or 3.)
   - `x` = position of that driver's **first** occurrence found while
     scanning.
   - `y` = position of the **second** occurrence, if one exists; otherwise
     `0`.
8. **Priority value**: convert each `(x, y)` to a single float via the
   Pythagorean theorem: `sqrt(x^2 + y^2)`.
9. **Driver priority linked list**: a real singly linked list (not just a
   Python list) of the 5 drivers, sorted **ascending** by that float value.
   Ties are broken by keeping the original `D1..D5` relative order (achieved
   via a stable sort — no special-case tie-breaking code needed).
10. **Node addresses** (NEW, Update 10) — `{node_label: letter}`:
    - Every one of the 11 people-pool nodes (`B1, S1, B2, S2, B3, S3, D1..D5`)
      gets a unique random letter from the fixed 11-letter set
      `{a, b, c, d, e, f, g, h, i, j, k}` — a random bijection (built by
      shuffling the letter set and zipping it against the 11 labels).
    - Printed alongside each name in the People Pool section, e.g.
      `B1: Gaurav - g`.
11. **Driver Tasks hashmap** — `{driver: [(str, str, str), ...]}`:
    - **Key order** matches the traversal order of the driver priority
      linked list from item 9 (lowest priority value first).
    - For each driver, in each transaction it appears in, it has a
      *predecessor* (the node handing it the product) and a *successor*
      (the node it hands the product on to). Transaction `i`'s product is
      always labeled `Pi`.
    - **Incoming entries come first**, one per transaction the driver
      appears in (scanned in transaction order 1→3).
    - **Outgoing entries come second**, same transaction scan order.
    - As of Update 10, every tuple has a **third element**: an address
      letter, per one of three rules (`Dy` below means the driver whose
      task list this is — i.e. the dict key — as distinct from `Dx`, some
      *other* driver named inside a specific tuple):
      - **(i) Incoming** `(Px, Sx|Dx, address)` — address of the
        predecessor `Sx`/`Dx` (whoever is sending the product).
      - **(ii) Outgoing to another driver** `(Dx, Px, address)` — address
        of `Dy` itself (the key driver — it's the one sending here).
      - **(iii) Outgoing to a buyer** `(Bx, Px, address)` — address of
        that buyer `Bx`.
    - These three rules were verified against a full worked example (18
      tuples across 5 drivers) — every single tuple matched.

---

## 5. Random Rectangle Corner Assignment — Implementation Context

> **Note:** this feature was implemented directly by a collaborator, in
> `rectangle_value.py`, with `main.py` updated to use it. Claude did not
> write or review that code — only this spec section, copied in verbatim
> from the collaborator's requirements, is being tracked here so future
> contributors (human or AI) have the full spec without needing to reread
> old chat history.

### Goal

Implement a utility that randomly assigns the values `1`, `2`, and `3` to
three of a rectangle's four corners. The one remaining corner must receive
the value `0`.

The assignment happens automatically. The user must not be asked to select a
value or a corner.

### Canonical data model

Represent the four corners as dictionary/map keys:

| Key | Corner | Coordinate |
| --- | --- | --- |
| `a` | bottom-left | `(min_x, min_y)` |
| `b` | top-left | `(min_x, max_y)` |
| `c` | top-right | `(max_x, max_y)` |
| `d` | bottom-right | `(max_x, min_y)` |

Return a dictionary whose keys are `a`, `b`, `c`, and `d`, and whose values
are a random permutation of `[0, 1, 2, 3]`.

Example result:

```json
{
  "a": 2,
  "b": 0,
  "c": 3,
  "d": 1
}
```

The result can differ on every call.

### Required behavior

1. Use only the four corners. Do not use the center or edge midpoints.
2. Assign each of `1`, `2`, and `3` exactly once.
3. Assign `0` exactly once to the leftover corner.
4. Include all four corner keys in every result.
5. Choose the assignment randomly without user input.
6. Do not assign the same value to multiple corners.

### Language-neutral algorithm

```text
corners = ["a", "b", "c", "d"]
values = shuffle([0, 1, 2, 3])
result = map each corner to the value at the same index
return result
```

Use the platform's secure/system random generator when unpredictability is
important. Allow an optional seeded random generator when deterministic tests
are needed.

### Suggested API

```text
assignRandomCornerValues(optionalRandomGenerator) -> Dictionary<Corner, Integer>
```

If coordinates are also needed, expose them separately:

```text
getCorners(minX, minY, maxX, maxY) -> Dictionary<Corner, Point>
```

Keeping coordinates and random values separate makes the assignment reusable
for rectangles of any size.

### Rectangle validation

When coordinates are accepted, require:

```text
min_x < max_x
min_y < max_y
```

Reject zero-width, zero-height, or reversed rectangles.

### Acceptance tests

For every generated assignment:

```text
keys(result) == {"a", "b", "c", "d"}
sorted(values(result)) == [0, 1, 2, 3]
count(value == 0) == 1
count(value in [1, 2, 3]) == 3
```

With a seeded random generator, repeated calls using the same seed should
produce the same result. Tests should not expect a particular unseeded order.

### Out of scope

- User-selected assignments
- Points inside the rectangle
- The rectangle's center
- Edge midpoints
- Duplicate assigned values

---

## 6. Explicitly NOT in the current version (rolled back)

A **deadlock / circular-wait bug** was identified and is currently
**unresolved by design** (per explicit user instruction to roll back):

- Because each transaction's 3 chosen drivers are ordered via
  `random.shuffle()` **independently per transaction** (in
  `assignment.py`), it's possible for two transactions to create
  opposite-direction hand-offs between the same pair of drivers — e.g.
  `D3 -> D5` in one chain and `D5 -> D3` in another. If the simulation is
  ever extended to model synchronous hand-offs (a driver must physically
  meet the next driver to pass the parcel), this is a genuine
  circular-wait deadlock.
- A fix was designed and fully implemented: assign each driver a single
  fixed random priority rank once per run, and always sort each
  transaction's chosen drivers into that same rank order — guaranteeing
  the combined hand-off graph is a DAG (classic fixed-resource-ordering
  deadlock prevention, same idea as consistent lock ordering). An
  `is_acyclic()` Kahn's-algorithm check was added as a verifying
  assertion.
- **This fix was rolled back at the user's request.** The current code in
  `assignment.py` uses plain `random.shuffle()` per transaction and has no
  deadlock protection. See Change Log Update 2 for details. **If this
  resurfaces as a real problem, the fix described above is the known
  solution — it doesn't need to be redesigned, just re-added.**

---

## 7. Module reference

| File | Contents | Purpose |
|---|---|---|
| `__init__.py` | `SimulationResult`, `run_simulation` | Side-effect-free public package interface. |
| `simulator.py` | `SimulationResult`, `run_simulation(seed=None, rng=None)` | Runs all computation without printing; supports deterministic seeds or explicit random-generator injection. |
| `config.py` | `NUM_TRANSACTIONS`, `NUM_DRIVERS`, `DRIVERS_PER_TRANSACTION`, `MAX_VALUE_PER_DRIVER` | Single source of truth for shared constants. |
| `names.py` | `NAME_POOL` | The 100 unique Indian names, asserted unique at import time. |
| `people.py` | `pick_people(pool)`, `build_transactions(buyer_seller_names)` | Draws 11 unique names (6 buyer/seller + 5 drivers); builds the 3 transaction dicts with `B{i}`/`S{i}` labels and names. |
| `addresses.py` | `assign_addresses(node_labels)` | **NEW.** Shuffles the fixed 11-letter set `{a..k}` and zips it against the 11 node labels, returning `{label: letter}`. Raises if given anything other than exactly 11 labels. |
| `assignment.py` | `assign_drivers_to_transactions(driver_labels)` | Retry-based random search: for each transaction, samples 3 drivers with remaining capacity > 0, shuffles their order, decrements capacity. **No deadlock protection** (see §6). |
| `priority.py` | `DriverNode`, `DriverPriorityLinkedList`, `compute_driver_positions()`, `compute_priority_values()`, `build_priority_linked_list()` | Builds the `{driver: (x, y)}` hashmap, converts to `sqrt(x^2+y^2)`, builds the ascending singly linked list. |
| `tasks.py` | `compute_driver_tasks(transactions, ordered_driver_labels, addresses)` | Builds the `{driver: [(str, str, str), ...]}` hand-off task hashmap per §4.11. **Updated in Update 10** to take `addresses` and emit 3-tuples instead of 2-tuples. |
| `rectangle_value.py` | (implemented by collaborator, not by Claude) | Random rectangle corner value assignment — full spec in §5. |
| `display.py` | `print_people_pool()`, `print_initial_hashmap()`, `print_transactions()`, `print_final_hashmap()`, `print_driver_positions()`, `print_priority_values()`, `print_priority_linked_list()`, `print_driver_tasks()` | All console-output formatting, kept separate from computation so either can be edited independently. `print_people_pool()` and the tuple formatter were updated in Update 10 for addresses. |
| `main.py` | `main()` | Thin console renderer over `run_simulation()`; preserves direct script execution. **Run this file.** |
| `tests/test_simulator.py` | 12 `unittest` regression tests | Covers import safety, seeded determinism, people/address/assignment invariants, priority ordering, driver tasks, CLI execution, and output-section order. |

---

## 8. Output sections, in order

1. Rectangle "Map Output" (unrelated feature, printed first — see §5)
2. People Pool Selected (buyers, sellers, drivers with real names **and address letters**, e.g. `B1: Gaurav - g`)
3. Initial Hashmap (`{D1: 0, ..., D5: 0}`)
4. Transactions (`S_i(name) -> D(name) -> D(name) -> D(name) -> B_i(name)`)
5. Final Hashmap (delivery counts, each ≤ 2)
6. Driver Position Hashmap (`{driver: (x, y)}`)
7. Driver Priority Values (`sqrt(x^2 + y^2)` per driver, printed in `D1..D5` order)
8. Driver Priority Linked List (ascending, printed via traversal)
9. Driver Tasks (printed in priority-linked-list order, 3-tuples including
   address, e.g. `D4 -> [(P1, S1, i), (P3, S3, j), (D1, P1, f), (D3, P3, f)]`)

---

## 9. How to run

```bash
cd marketplace_sim_v1
python3 main.py
```

(Also works as `python3 marketplace_sim_v1/main.py` from the repo root. The
entry point adds the repository root to `sys.path` only when executed directly,
so package imports remain side-effect-free.)

No install step, no dependencies beyond the Python standard library
(including `random`, `math`, `dataclasses`, and `unittest`).

The simulator can also be imported without producing console output:

```python
from marketplace_sim_v1 import run_simulation

result = run_simulation(seed=2026)
```

Run the deterministic regression suite from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

---

## 10. Change Log

> Note: this file had accumulated some duplicate section numbers and
> duplicate/garbled paragraphs (two "Update 5" entries, two "§4" headers,
> a stale description of a since-deleted single-file script) from earlier
> hand-edits. Update 10 below cleaned up structure and numbering only —
> no historical entry's content was deleted, only renumbered/deduplicated
> for readability.

**Update 1 — Initial build**
Built the core simulator: 100-name pool, 3 buyer/seller pairs, 5 drivers,
capacity-constrained random driver assignment (max 2 deliveries/driver),
transaction chain printing. Verified across multiple runs.

**Update 2 — Deadlock identified, fix built, then rolled back**
User spotted a real circular-wait deadlock in sample output (D3 and D5
waiting on each other's product across two transactions). Implemented a
fix: fixed global driver priority ranking + `is_acyclic()` Kahn's-algorithm
verification. Verified working across 8 runs. **User then asked to roll
this back entirely** before proceeding with Update 3 — the deadlock fix is
NOT in the current code. See §6 for details on what the fix was, in case
it needs to be reintroduced later.

**Update 3 — Driver position hashmap + priority linked list**
Added, on top of the rolled-back (original) script: `{driver: (x, y)}`
position hashmap parsed from the transaction chains, `sqrt(x^2+y^2)`
priority value per driver, and a real singly linked list
(`DriverNode`/`DriverPriorityLinkedList`) sorted ascending by that value,
with ties resolved via stable sort (original `D1..D5` order). Verified
against the user's own worked example (`D3 -> (1,2)`, `D1 -> (1,0)`,
final list `D1 -> D3 -> D5 -> D2 -> D4`) — matched exactly.

**Update 4 — PROJECT_CONTEXT.md created**
This file was created to give any collaborator or new chat instance full
context on the spec, current implementation, and history without needing
the original conversation.

**Update 5 — Three-person development pipeline added**
Added `TEAM_PIPELINE.md` with role ownership, dependency-ordered delivery
waves, LLM prompt and handoff rules, PR routing, merge gates, and
repository settings. Added root `AGENTS.md` so separate coding instances
follow the same context and safety rules, plus GitHub implementation-issue
and pull-request templates. Simulator behavior was not changed.

**Update 6 — Split into a multi-file project**
The single `marketplace_sim_v1.py` script was broken up into
`config.py`, `names.py`, `people.py`, `assignment.py`, `priority.py`,
`display.py`, and a `main.py` entry point, all inside `marketplace_sim_v1/`
(per the user's actual local folder layout). No logic changed in this
step — pure reorganization for readability, verified by re-running the
program multiple times after the split.

**Update 7 — Driver Tasks feature added**
Added `tasks.py` with `compute_driver_tasks()`, producing the
`{driver: [(str, str), ...]}` hashmap described in §4.11, in driver
priority order. Verified against the user's worked example: matched 4 of
5 drivers exactly and 3 of 4 entries on the 5th (see Update 8 for the one
flagged discrepancy, believed to be a typo in the example). `display.py`
got a new `print_driver_tasks()` function to render it without quote
marks, matching the requested output format.

**Update 8 — D5 tuple-order discrepancy confirmed as a prompt typo**
User confirmed a flagged `D5` entry from Update 7 (`('P2', 'D2')` vs. the
rule's `('D2', 'P2')`) was a typo in their original prompt, not an
exception to the rule. No code changes required — `tasks.py` was already
correct.

**Update 9 — Random Rectangle Corner Assignment spec added (docs only)**
User implemented a new, separate feature directly (`rectangle_value.py`,
plus an update to `main.py`) without Claude's involvement in the code.
Per explicit request, only this file was touched that session: the
collaborator's full spec was added verbatim (now §5), and
`rectangle_value.py` was added to the repo layout diagram and module
reference table. Claude has not written or verified `rectangle_value.py`
or its `main.py` integration — §5 describes the *intended* spec only.

**Update 10 — Node addresses added to People Pool and Driver Tasks**
Added `addresses.py` (`assign_addresses()`), giving every one of the 11
people-pool nodes a unique random letter from `{a..k}`. Wired into
`main.py` right after buyer/seller/driver labels are known. Updated:
- `display.py`'s `print_people_pool()` to print `Name - letter` for every
  node, and its tuple formatter to render 3-tuples instead of 2-tuples.
- `tasks.py`'s `compute_driver_tasks()` to take an `addresses` dict and
  return 3-tuples per the three address rules in §4.11 (incoming = sender's
  address; outgoing-to-driver = the key driver's own address;
  outgoing-to-buyer = that buyer's address).

Verified two ways: (1) reconstructed the user's exact worked example
(hardcoded transactions + addresses) and reproduced their expected
`Driver Tasks (UPDATED)` output tuple-for-tuple, exact match; (2) ran the
full program end-to-end multiple times with fresh random data and manually
traced every tuple in one full run against the three rules — all correct.

This update also cleaned up structural issues in this file that had
accumulated from earlier hand-edits (duplicate "Update 5" entries,
duplicate "§4"/"§9" headers, a stale description of the deleted
single-file script, duplicate "How to run" commands) — see the note at
the top of this Change Log section.

**Update 11 — GitHub collaboration workflow implemented**
Added `CONTRIBUTING.md` as the canonical issue-first collaboration workflow,
including issue scope, issue-numbered branches, commit and pull-request rules,
review readiness, structured labels, blocked-work handling, project statuses,
and coding-agent behavior. Aligned `AGENTS.md` and `TEAM_PIPELINE.md` with it,
expanded the implementation issue and pull-request templates, and added a bug
report template. Simulator behavior was not changed.

**Update 12 — Importable simulator and deterministic regression suite**
Added side-effect-free package exports in `__init__.py` and computation-only
orchestration in `simulator.py`. The public `run_simulation(seed=None,
rng=None)` entry point returns a structured `SimulationResult`; a seed creates
an isolated deterministic generator, while the no-argument path preserves the
existing global-random CLI behavior. Added backward-compatible optional RNG
injection to people selection, addresses, driver assignment, and the existing
rectangle helper. Converted internal imports to package-safe imports while
keeping `python marketplace_sim_v1/main.py` working through a thin compatibility
wrapper. Added 12 standard-library `unittest` regression tests for imports,
determinism, core invariants, priority stability, driver tasks, CLI execution,
and output-section order. Deadlock and rectangle semantics were not changed.

---

## 11. Open items for future contributors

- Deadlock protection (§6) is currently **off**. Decide whether/when to
  re-add it, and whether it should be default-on or opt-in.
- The local regression suite exists, but automated CI enforcement remains a
  separate C0.2 task.
- Consider whether buyer/seller pairs should also be checked for any
  structural constraints (currently unconstrained beyond uniqueness).
- `rectangle_value.py` and its `main.py` integration (§5) have not been
  reviewed or tested by Claude — only the spec is documented there. Worth
  a review pass against the acceptance tests in §5 when convenient.


---

## Marketplace v2 — Django foundation

A separate `marketplace-v2/` directory now contains the new Django 5.2 LTS
application foundation. It is intentionally isolated from `marketplace_sim_v1/`;
the v1 simulator has not been moved, rewritten, or modified.

The v2 foundation currently provides environment-based Django settings,
PostgreSQL configuration, Docker Compose services for the web application and
PostgreSQL, a `/health/` endpoint, and initial project smoke tests. Domain apps,
models, authentication roles, payments, and logistics are intentionally not
implemented in this foundation step and remain owned by their scheduled
pipeline issues.
