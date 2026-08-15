"""
Turns finished transactions into a driver priority linked list:

  1. compute_driver_positions()   -> {driver: (x, y)} hashmap
  2. compute_priority_values()    -> {driver: sqrt(x^2 + y^2)}
  3. build_priority_linked_list() -> ascending singly linked list
"""

import math


class DriverNode:
    """A single node in the driver priority linked list."""

    def __init__(self, label, xy, value):
        self.label = label      # e.g. "D3"
        self.xy = xy            # the (x, y) tuple this node was scored from
        self.value = value      # sqrt(x^2 + y^2)
        self.next = None


class DriverPriorityLinkedList:
    """A minimal singly linked list of DriverNode, built once and traversed in order."""

    def __init__(self):
        self.head = None
        self._tail = None

    def append(self, label, xy, value):
        node = DriverNode(label, xy, value)
        if self.head is None:
            self.head = node
        else:
            self._tail.next = node
        self._tail = node

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __str__(self):
        return " -> ".join(f"{n.label}{n.xy}={n.value:.4f}" for n in self)


def compute_driver_positions(transactions, driver_labels):
    """
    Build the hashmap {driver_label: (x, y)}:

    Scan Transaction 1 -> Transaction 2 -> Transaction 3, left to right
    within each transaction's chain. A driver's "position in transaction"
    is its index in the full S -> D -> D -> D -> B chain, indexed from 0
    (so the seller is always 0, and the three drivers are always at
    positions 1, 2, 3).

    x = the position of the driver's FIRST occurrence found while scanning.
    y = the position of the driver's SECOND occurrence, if one exists;
        otherwise 0.
    """
    occurrences = {label: [] for label in driver_labels}

    for txn in transactions:
        for index_in_chain, label in enumerate(txn["driver_chain"]):
            position_in_transaction = index_in_chain + 1  # +1: seller sits at position 0
            occurrences[label].append(position_in_transaction)

    driver_xy = {}
    for label in driver_labels:
        seen = occurrences[label]
        x = seen[0] if len(seen) >= 1 else 0
        y = seen[1] if len(seen) >= 2 else 0
        driver_xy[label] = (x, y)

    return driver_xy


def compute_priority_values(driver_xy):
    """Convert each (x, y) tuple to a single float via the Pythagorean theorem."""
    return {
        label: math.sqrt(x ** 2 + y ** 2)
        for label, (x, y) in driver_xy.items()
    }


def build_priority_linked_list(driver_labels, driver_xy, driver_values):
    """
    Build the DriverPriorityLinkedList in ascending order of driver_values.
    Python's sort is stable, and driver_labels is iterated in a fixed
    D1..D5 order, so ties naturally end up "appended one after the other"
    in that same original order.
    """
    ordered_labels = sorted(driver_labels, key=lambda label: driver_values[label])

    linked_list = DriverPriorityLinkedList()
    for label in ordered_labels:
        linked_list.append(label, driver_xy[label], driver_values[label])
    return linked_list
