"""
Marketplace Transaction Simulator -- entry point.

Run with:  python3 main.py

Only dependency: the Python standard library (random, math).
See PROJECT_CONTEXT.md (in the project root) for the full spec and history.
"""

from pathlib import Path
import sys


# Preserve ``python marketplace_sim_v1/main.py`` while using package-safe
# imports everywhere else. This path adjustment runs only for direct script
# execution; normal package imports do not modify ``sys.path``.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from marketplace_sim_v1 import display
from marketplace_sim_v1.simulator import run_simulation


def main():
    result = run_simulation()

    # Print the mapped output
    print("\n=== Map Output ===")
    for num, corner in result.corner_positions.items():
        print(f"Number {num}: {corner}")
    print("\n")

    # ------------------------------------------------------------------
    # Output: people, transactions, delivery counts
    # ------------------------------------------------------------------
    display.print_people_pool(
        result.transactions,
        result.driver_labels,
        result.driver_label_to_name,
        result.addresses,
    )
    display.print_initial_hashmap(result.driver_labels)
    display.print_transactions(result.transactions, result.driver_label_to_name)
    display.print_final_hashmap(result.driver_counts)

    # ------------------------------------------------------------------
    # Driver priority linked list
    # ------------------------------------------------------------------
    display.print_driver_positions(result.driver_xy)
    display.print_priority_values(
        result.driver_labels, result.driver_xy, result.driver_values
    )
    display.print_priority_linked_list(result.priority_list)

    # ------------------------------------------------------------------
    # Driver tasks hashmap (key order == priority linked list order)
    # ------------------------------------------------------------------
    display.print_driver_tasks(result.driver_tasks)


if __name__ == "__main__":
    main()
