"""
Marketplace Transaction Simulator -- entry point.

Run with:  python3 main.py

Only dependency: the Python standard library (random, math).
See PROJECT_CONTEXT.md (in the project root) for the full spec and history.
"""

from config import NUM_DRIVERS, MAX_VALUE_PER_DRIVER
from names import NAME_POOL
from people import pick_people, build_transactions
from assignment import assign_drivers_to_transactions
from priority import (
    compute_driver_positions,
    compute_priority_values,
    build_priority_linked_list,
)
from tasks import compute_driver_tasks
from addresses import assign_addresses
from rectangle_value import get_corner_positions
import display


def main():
    # ------------------------------------------------------------------
    # Rectangle positions
    # ------------------------------------------------------------------
    positions = get_corner_positions()
    
    # Print the mapped output
    print("\n=== Map Output ===")
    for num, corner in positions.items():
        print(f"Number {num}: {corner}")
    print("\n")

    # ------------------------------------------------------------------
    # People + transactions
    # ------------------------------------------------------------------
    buyer_seller_names, driver_names = pick_people(NAME_POOL)
    transactions = build_transactions(buyer_seller_names)

    driver_labels = [f"D{i + 1}" for i in range(NUM_DRIVERS)]
    driver_label_to_name = dict(zip(driver_labels, driver_names))

    # ------------------------------------------------------------------
    # Node addresses (one unique letter per buyer/seller/driver label)
    # ------------------------------------------------------------------
    node_labels = []
    for txn in transactions:
        node_labels.append(txn["buyer_label"])
        node_labels.append(txn["seller_label"])
    node_labels.extend(driver_labels)
    addresses = assign_addresses(node_labels)

    # ------------------------------------------------------------------
    # Driver assignment + delivery-count hashmap
    # ------------------------------------------------------------------
    driver_counts = {label: 0 for label in driver_labels}
    chains = assign_drivers_to_transactions(driver_labels)

    for txn, chain in zip(transactions, chains):
        txn["driver_chain"] = chain
        for label in chain:
            driver_counts[label] += 1

    # ------------------------------------------------------------------
    # Output: people, transactions, delivery counts
    # ------------------------------------------------------------------
    display.print_people_pool(transactions, driver_labels, driver_label_to_name, addresses)
    display.print_initial_hashmap(driver_labels)
    display.print_transactions(transactions, driver_label_to_name)
    display.print_final_hashmap(driver_counts)

    for label, value in driver_counts.items():
        assert value <= MAX_VALUE_PER_DRIVER, f"{label} exceeded max value of {MAX_VALUE_PER_DRIVER}"

    # ------------------------------------------------------------------
    # Driver priority linked list
    # ------------------------------------------------------------------
    driver_xy = compute_driver_positions(transactions, driver_labels)
    display.print_driver_positions(driver_xy)

    driver_values = compute_priority_values(driver_xy)
    display.print_priority_values(driver_labels, driver_xy, driver_values)

    priority_list = build_priority_linked_list(driver_labels, driver_xy, driver_values)
    display.print_priority_linked_list(priority_list)

    # ------------------------------------------------------------------
    # Driver tasks hashmap (key order == priority linked list order)
    # ------------------------------------------------------------------
    ordered_driver_labels = [node.label for node in priority_list]
    driver_tasks = compute_driver_tasks(transactions, ordered_driver_labels, addresses)
    display.print_driver_tasks(driver_tasks)


if __name__ == "__main__":
    main()
