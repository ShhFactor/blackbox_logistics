"""
All console-output formatting lives here, kept separate from the
computation logic in the other modules so either side can be edited
without touching the other.
"""


def _format_tuple_list(pairs):
    """
    Render a list of 2-tuples without the quote marks Python's default
    repr would add, e.g. [('P1', 'S1')] -> '[(P1, S1)]'.
    """
    return "[" + ", ".join(f"({a}, {b})" for a, b in pairs) + "]"


def print_people_pool(transactions, driver_labels, driver_label_to_name):
    print("=== People Pool Selected ===")
    for txn in transactions:
        print(f"  {txn['buyer_label']}: {txn['buyer_name']}   |   {txn['seller_label']}: {txn['seller_name']}")
    for label in driver_labels:
        print(f"  {label}: {driver_label_to_name[label]}")


def print_initial_hashmap(driver_labels):
    print("\n=== Initial Hashmap (driver -> deliveries) ===")
    print({label: 0 for label in driver_labels})


def print_transactions(transactions, driver_label_to_name):
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


def print_final_hashmap(driver_counts):
    print("\n=== Final Hashmap (driver -> total deliveries) ===")
    print(driver_counts)


def print_driver_positions(driver_xy):
    print("\n=== Driver Position Hashmap (driver -> (x, y)) ===")
    print(driver_xy)


def print_priority_values(driver_labels, driver_xy, driver_values):
    print("\n=== Driver Priority Values: sqrt(x^2 + y^2) ===")
    for label in driver_labels:
        print(f"  {label}{driver_xy[label]} -> {driver_values[label]:.4f}")


def print_priority_linked_list(priority_list):
    print("\n=== Driver Priority Linked List (ascending) ===")
    print("  " + str(priority_list))


def print_driver_tasks(driver_tasks):
    print("\n=== Driver Tasks ===")
    for label, pairs in driver_tasks.items():
        print(f"  {label} -> {_format_tuple_list(pairs)}")
