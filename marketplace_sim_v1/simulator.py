"""Core orchestration for one marketplace simulation run.

This module performs computation only. Console formatting remains in
``display.py`` and the command-line entry point remains in ``main.py``.
"""

from dataclasses import dataclass, field
import random

from .addresses import assign_addresses
from .assignment import assign_drivers_to_transactions
from .config import MAX_VALUE_PER_DRIVER, NUM_DRIVERS
from .names import NAME_POOL
from .people import build_transactions, pick_people
from .priority import (
    DriverPriorityLinkedList,
    build_priority_linked_list,
    compute_driver_positions,
    compute_priority_values,
)
from .rectangle_value import get_corner_positions
from .tasks import compute_driver_tasks


@dataclass
class SimulationResult:
    """Structured output from one complete simulation run.

    ``priority_list`` is excluded from equality because linked-list nodes use
    identity equality. Its complete observable ordering and values are already
    represented by ``ordered_driver_labels``, ``driver_xy``, and
    ``driver_values``.
    """

    corner_positions: dict
    transactions: list
    driver_labels: list
    driver_label_to_name: dict
    addresses: dict
    driver_counts: dict
    driver_xy: dict
    driver_values: dict
    ordered_driver_labels: list
    driver_tasks: dict
    priority_list: DriverPriorityLinkedList = field(compare=False, repr=False)


def _resolve_random_source(seed=None, rng=None):
    if seed is not None and rng is not None:
        raise ValueError("Provide either seed or rng, not both.")
    if rng is not None:
        return rng
    if seed is not None:
        return random.Random(seed)
    return random


def run_simulation(seed=None, rng=None):
    """Run the simulator and return a :class:`SimulationResult`.

    Args:
        seed: Optional seed used to create an isolated ``random.Random``
            instance. Reusing a seed produces the same result without changing
            global random state.
        rng: Optional random-compatible object supporting ``sample`` and
            ``shuffle``. This enables explicit dependency injection in tests.

    With neither argument, the existing CLI behavior is preserved by using
    Python's process-global ``random`` module.
    """

    random_source = _resolve_random_source(seed=seed, rng=rng)
    corner_positions = get_corner_positions(rng=random_source)

    buyer_seller_names, driver_names = pick_people(NAME_POOL, rng=random_source)
    transactions = build_transactions(buyer_seller_names)

    driver_labels = [f"D{i + 1}" for i in range(NUM_DRIVERS)]
    driver_label_to_name = dict(zip(driver_labels, driver_names))

    node_labels = []
    for transaction in transactions:
        node_labels.append(transaction["buyer_label"])
        node_labels.append(transaction["seller_label"])
    node_labels.extend(driver_labels)
    addresses = assign_addresses(node_labels, rng=random_source)

    driver_counts = {label: 0 for label in driver_labels}
    chains = assign_drivers_to_transactions(driver_labels, rng=random_source)

    for transaction, chain in zip(transactions, chains):
        transaction["driver_chain"] = chain
        for label in chain:
            driver_counts[label] += 1

    for label, value in driver_counts.items():
        assert value <= MAX_VALUE_PER_DRIVER, (
            f"{label} exceeded max value of {MAX_VALUE_PER_DRIVER}"
        )

    driver_xy = compute_driver_positions(transactions, driver_labels)
    driver_values = compute_priority_values(driver_xy)
    priority_list = build_priority_linked_list(
        driver_labels, driver_xy, driver_values
    )
    ordered_driver_labels = [node.label for node in priority_list]
    driver_tasks = compute_driver_tasks(
        transactions, ordered_driver_labels, addresses
    )

    return SimulationResult(
        corner_positions=corner_positions,
        transactions=transactions,
        driver_labels=driver_labels,
        driver_label_to_name=driver_label_to_name,
        addresses=addresses,
        driver_counts=driver_counts,
        driver_xy=driver_xy,
        driver_values=driver_values,
        ordered_driver_labels=ordered_driver_labels,
        driver_tasks=driver_tasks,
        priority_list=priority_list,
    )

