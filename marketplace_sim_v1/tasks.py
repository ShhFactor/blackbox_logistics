"""
Builds the "Driver Tasks" hashmap: for each driver, a 1D list of 2-tuples
of strings describing every product hand-off that driver is involved in.

For a given driver, in a given transaction it appears in, the full chain is
  [seller, D_a, D_b, D_c, buyer]
and the driver sits at some index in that chain with a predecessor (the
node handing the product TO the driver) and a successor (the node the
driver hands the product ON to). Transaction i's product is always "Pi".

Ordering rules (derived from the worked example):
  - INCOMING tuples come first: (product, predecessor_label)
      e.g. ('P1', 'S1')  -- P1 is arriving from S1
  - OUTGOING tuples come second: (successor_label, product)
      e.g. ('D1', 'P1')  -- P1 is leaving towards D1
  - Within each group, entries are ordered by scanning the transactions
    1 -> 2 -> 3 (only the transactions the driver actually appears in).

Key order in the returned dict matches `ordered_driver_labels` exactly --
this is meant to be fed the traversal order of the driver priority linked
list from priority.py, so the driver with the lowest priority value has
its task list built (and appears in the dict) first.
"""


def compute_driver_tasks(transactions, ordered_driver_labels):
    tasks = {}

    for label in ordered_driver_labels:
        incoming = []
        outgoing = []

        for txn in transactions:
            full_chain = [txn["seller_label"], *txn["driver_chain"], txn["buyer_label"]]
            if label not in full_chain:
                continue

            index = full_chain.index(label)
            product = f"P{txn['id']}"
            predecessor = full_chain[index - 1]
            successor = full_chain[index + 1]

            incoming.append((product, predecessor))
            outgoing.append((successor, product))

        tasks[label] = incoming + outgoing

    return tasks
