"""
Randomly assigns delivery drivers to each transaction, respecting the
per-driver delivery-count cap.

KNOWN ISSUE (left unresolved by explicit project decision -- see
PROJECT_CONTEXT.md, "Deadlock protection"): each transaction's driver order
is shuffled independently here, so two transactions can end up creating
opposite-direction hand-offs between the same pair of drivers (e.g.
D3 -> D5 in one chain, D5 -> D3 in another). A fix (a fixed global driver
priority ranking + a cycle check) was designed, implemented, and verified,
then rolled back at the user's request. If this becomes a real problem
again, that fix is the known solution -- see PROJECT_CONTEXT.md for details
rather than re-deriving it from scratch.
"""

import random

from config import NUM_TRANSACTIONS, DRIVERS_PER_TRANSACTION, MAX_VALUE_PER_DRIVER


def assign_drivers_to_transactions(driver_labels, max_attempts=10000):
    """
    For each transaction, randomly pick DRIVERS_PER_TRANSACTION distinct
    drivers (in random chain order) such that no driver's running total
    ever exceeds MAX_VALUE_PER_DRIVER. Uses retry-based random search,
    which is trivial for this problem size (5 drivers, capacity 2 each,
    9 total assignments needed out of 10 available "slots").
    """
    for _ in range(max_attempts):
        remaining_capacity = {label: MAX_VALUE_PER_DRIVER for label in driver_labels}
        chains = []
        ok = True

        for _ in range(NUM_TRANSACTIONS):
            available = [d for d in driver_labels if remaining_capacity[d] > 0]
            if len(available) < DRIVERS_PER_TRANSACTION:
                ok = False
                break

            chosen = random.sample(available, DRIVERS_PER_TRANSACTION)
            random.shuffle(chosen)  # random order within the delivery chain
            for d in chosen:
                remaining_capacity[d] -= 1
            chains.append(chosen)

        if ok:
            return chains

    raise RuntimeError("Could not find a valid driver assignment; try again.")
