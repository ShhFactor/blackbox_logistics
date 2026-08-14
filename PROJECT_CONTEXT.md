# PROJECT_CONTEXT.md

> Living context file for the **Marketplace Transaction Simulator** project.
> Multiple people (and multiple separate chat instances) work on this — **update
> this file whenever the script changes** so anyone can pick up full context
> without re-reading old conversations. Append to the Change Log, don't delete
> old entries.

Last updated: 2026-08-15

---

## 1. What this project is

A single-file Python script, `marketplace_simulator.py`, that simulates a small
marketplace with buyers, sellers, and delivery drivers, then derives a
"priority" ordering of the drivers from how the deliveries played out.

No third-party dependencies — only the standard library (`random`, `math`).

---

## 2. Current spec (as of the latest version)

1. **Name pool**: `NAME_POOL` — exactly 100 unique Indian names, hardcoded.
2. **Buyers/Sellers**: pick 6 unique names from the pool to form 3 pairs:
   `(B1, S1)`, `(B2, S2)`, `(B3, S3)`.
3. **Drivers**: pick 5 more unique names from the pool (disjoint from the
   6 above) — labeled `D1`..`D5`.
4. **Initial hashmap**: `{D1: 0, D2: 0, D3: 0, D4: 0, D5: 0}`.
5. **Transactions**: build exactly 3 transactions. Each is a chain of the form
   `S_i -> D -> D -> D -> B_i`, using exactly 3 **distinct** drivers chosen at
   random for that transaction.
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

---

## 3. Explicitly NOT in the current version (rolled back)

A **deadlock / circular-wait bug** was identified and is currently
**unresolved by design** (per explicit user instruction to roll back):

- Because each transaction's 3 chosen drivers are ordered via
  `random.shuffle()` **independently per transaction**, it's possible for two
  transactions to create opposite-direction hand-offs between the same pair
  of drivers — e.g. `D3 -> D5` in one chain and `D5 -> D3` in another. If the
  simulation is ever extended to model synchronous hand-offs (a driver must
  physically meet the next driver to pass the parcel), this is a genuine
  circular-wait deadlock.
- A fix was designed and fully implemented: assign each driver a single fixed
  random priority rank once per run, and always sort each transaction's
  chosen drivers into that same rank order — guaranteeing the combined
  hand-off graph is a DAG (classic fixed-resource-ordering deadlock
  prevention, same idea as consistent lock ordering). A `is_acyclic()`
  Kahn's-algorithm check was added as a verifying assertion.
- **This fix was rolled back at the user's request.** The current script uses
  plain `random.shuffle()` per transaction and has no deadlock protection.
  See Change Log Update 2 for details. **If this resurfaces as a real
  problem, the fix described above is the known solution — it doesn't need
  to be redesigned, just re-added.**

---

## 4. Key functions in `marketplace_simulator.py`

| Function / Class | Purpose |
|---|---|
| `NAME_POOL` | The 100 unique Indian names, asserted unique at load time. |
| `pick_people(pool)` | Draws 11 unique names in one `random.sample` call: 6 for buyer/seller pairs + 5 for drivers. |
| `build_transactions(buyer_seller_names)` | Builds the 3 transaction dicts with `B{i}`/`S{i}` labels and names. |
| `assign_drivers_to_transactions(driver_labels)` | Retry-based random search: for each transaction, samples 3 drivers with remaining capacity > 0, shuffles their order, decrements capacity. Retries the whole draw if it paints itself into a corner. **No deadlock protection** (see §3). |
| `DriverNode` | A node in the singly linked priority list (`label`, `xy`, `value`, `next`). |
| `DriverPriorityLinkedList` | Minimal singly linked list with `append()` and iteration. |
| `compute_driver_positions(transactions, driver_labels)` | Builds the `{driver: (x, y)}` hashmap per §2.7. |
| `compute_priority_values(driver_xy)` | `{driver: sqrt(x^2 + y^2)}`. |
| `build_priority_linked_list(driver_labels, driver_xy, driver_values)` | Builds the final sorted linked list (stable sort → ties preserve `D1..D5` order). |
| `main()` | Orchestrates everything and prints all output sections below. |

---

## 5. Output sections, in order

1. People Pool Selected (buyers, sellers, drivers with real names)
2. Initial Hashmap (`{D1: 0, ..., D5: 0}`)
3. Transactions (`S_i(name) -> D(name) -> D(name) -> D(name) -> B_i(name)`)
4. Final Hashmap (delivery counts, each ≤ 2)
5. Driver Position Hashmap (`{driver: (x, y)}`)
6. Driver Priority Values (`sqrt(x^2 + y^2)` per driver)
7. Driver Priority Linked List (ascending, printed via traversal)

---

## 6. How to run

```bash
python3 marketplace_simulator.py
```

No install step, no dependencies beyond the Python standard library
(`random`, `math`).

---

## 7. Change Log

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
NOT in the current script. See §3 for details on what the fix was, in case
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

---

## 8. Open items for future contributors

- Deadlock protection (§3) is currently **off**. Decide whether/when to
  re-add it, and whether it should be default-on or opt-in.
- No automated test suite yet — verification so far has been manual
  (multiple runs + one hand-worked example check).
- Consider whether buyer/seller pairs should also be checked for any
  structural constraints (currently unconstrained beyond uniqueness).