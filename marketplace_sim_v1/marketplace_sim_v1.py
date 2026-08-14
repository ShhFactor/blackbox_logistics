"""
Marketplace Transaction Simulator
----------------------------------
- Picks 6 unique people from a 100-name pool to form 3 (Buyer, Seller) pairs.
- Picks 5 more unique people (disjoint from the above) to be delivery drivers.
- Builds a hashmap {driver_label: 0} for the 5 drivers.
- Builds 3 delivery chains (one per transaction), each chain using exactly
  3 distinct drivers: Seller -> Driver -> Driver -> Driver -> Buyer.
- Every time a driver appears in a chain, their hashmap value is incremented
  by 1. No driver's total value is ever allowed to exceed 2.

Only dependency: the Python standard library (`random`).
"""

import math
import random

# ---------------------------------------------------------------------------
# 1. Pool of 100 unique Indian names
# ---------------------------------------------------------------------------
NAME_POOL = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan",
    "Krishna", "Ishaan", "Rohan", "Kabir", "Aryan", "Dhruv", "Karthik", "Manav",
    "Nikhil", "Rahul", "Rajesh", "Sanjay", "Amit", "Vikram", "Suresh", "Ramesh",
    "Anil", "Deepak", "Gaurav", "Harsh", "Varun", "Yash", "Siddharth", "Tarun",
    "Uday", "Vikas", "Abhishek", "Ashwin", "Chirag", "Devendra", "Girish", "Hemant",
    "Jatin", "Kunal", "Lakshay", "Mohit", "Naveen", "Omkar", "Pranav", "Rajat",
    "Saurabh", "Tanmay", "Aanya", "Diya", "Ira", "Kiara", "Myra", "Pari",
    "Riya", "Saanvi", "Sara", "Zara", "Ananya", "Bhavya", "Chitra", "Divya",
    "Esha", "Falguni", "Gauri", "Hema", "Isha", "Jaya", "Kavya", "Lakshmi",
    "Meera", "Nandini", "Ojasvi", "Pooja", "Radhika", "Sneha", "Tanvi", "Uma",
    "Vidya", "Yamini", "Anjali", "Bela", "Charu", "Deepika", "Ekta", "Farah",
    "Geeta", "Hina", "Indira", "Janvi", "Kiran", "Leela", "Madhavi", "Neha",
    "Pallavi", "Priya", "Ritika", "Simran",
]

assert len(NAME_POOL) == len(set(NAME_POOL)) == 100, "Name pool must have exactly 100 unique names"

NUM_TRANSACTIONS = 3
NUM_DRIVERS = 5
DRIVERS_PER_TRANSACTION = 3
MAX_VALUE_PER_DRIVER = 2


def pick_people(pool):
    """Select 6 unique buyer/seller names + 5 unique driver names (all disjoint)."""
    chosen = random.sample(pool, 2 * NUM_TRANSACTIONS + NUM_DRIVERS)  # 6 + 5 = 11
    buyer_seller_names = chosen[:2 * NUM_TRANSACTIONS]
    driver_names = chosen[2 * NUM_TRANSACTIONS:]
    return buyer_seller_names, driver_names


def build_transactions(buyer_seller_names):
    """Build 3 transactions, each with a labeled buyer and seller."""
    transactions = []
    for i in range(NUM_TRANSACTIONS):
        buyer_name = buyer_seller_names[2 * i]
        seller_name = buyer_seller_names[2 * i + 1]
        transactions.append({
            "id": i + 1,
            "buyer_label": f"B{i + 1}",
            "buyer_name": buyer_name,
            "seller_label": f"S{i + 1}",
            "seller_name": seller_name,
        })
    return transactions


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
    Build the hashmap {driver_label: (x, y)} described by the spec:

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
    in that same original order, exactly as the spec asks.
    """
    ordered_labels = sorted(driver_labels, key=lambda label: driver_values[label])

    linked_list = DriverPriorityLinkedList()
    for label in ordered_labels:
        linked_list.append(label, driver_xy[label], driver_values[label])
    return linked_list


def main():
    buyer_seller_names, driver_names = pick_people(NAME_POOL)
    transactions = build_transactions(buyer_seller_names)

    driver_labels = [f"D{i + 1}" for i in range(NUM_DRIVERS)]
    driver_label_to_name = dict(zip(driver_labels, driver_names))

    # Hashmap: 5 driver keys, all initialized to 0
    driver_counts = {label: 0 for label in driver_labels}

    chains = assign_drivers_to_transactions(driver_labels)

    # Apply the chosen chains to the transactions and update the hashmap
    for txn, chain in zip(transactions, chains):
        txn["driver_chain"] = chain
        for label in chain:
            driver_counts[label] += 1

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------
    print("=== People Pool Selected ===")
    for txn in transactions:
        print(f"  {txn['buyer_label']}: {txn['buyer_name']}   |   {txn['seller_label']}: {txn['seller_name']}")
    for label in driver_labels:
        print(f"  {label}: {driver_label_to_name[label]}")

    print("\n=== Initial Hashmap (driver -> deliveries) ===")
    print({label: 0 for label in driver_labels})

    print("\n=== Transactions ===")
    for txn in transactions:
        chain_str = " -> ".join(
            f"{label}({driver_label_to_name[label]})" for label in txn["driver_chain"]
        )
        full_chain = (
            f"{txn['seller_label']}({txn['seller_name']}) -> {chain_str} -> "
            f"{txn['buyer_label']}({txn['buyer_name']})"
        )
        print(f"  Transaction {txn['id']}: {full_chain}")

    print("\n=== Final Hashmap (driver -> total deliveries) ===")
    print(driver_counts)

    for label, value in driver_counts.items():
        assert value <= MAX_VALUE_PER_DRIVER, f"{label} exceeded max value of {MAX_VALUE_PER_DRIVER}"

    # ------------------------------------------------------------------
    # Driver priority linked list, built from the transaction output above
    # ------------------------------------------------------------------
    driver_xy = compute_driver_positions(transactions, driver_labels)
    print("\n=== Driver Position Hashmap (driver -> (x, y)) ===")
    print(driver_xy)

    driver_values = compute_priority_values(driver_xy)
    print("\n=== Driver Priority Values: sqrt(x^2 + y^2) ===")
    for label in driver_labels:
        print(f"  {label}{driver_xy[label]} -> {driver_values[label]:.4f}")

    priority_list = build_priority_linked_list(driver_labels, driver_xy, driver_values)
    print("\n=== Driver Priority Linked List (ascending) ===")
    print("  " + str(priority_list))


if __name__ == "__main__":
    main()