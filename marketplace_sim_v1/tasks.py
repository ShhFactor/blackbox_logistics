"""
Builds the "Driver Tasks" hashmap: for each driver, a 1D list of 3-tuples
of strings describing every product hand-off that driver is involved in,
now including the relevant node's address letter (see addresses.py).

For a given driver, in a given transaction it appears in, the full chain is
  [seller, D_a, D_b, D_c, buyer]
and the driver sits at some index in that chain with a predecessor (the
node handing the product TO the driver) and a successor (the node the
driver hands the product ON to). Transaction i's product is always "Pi".

Ordering rules (unchanged from the 2-tuple version):
  - INCOMING tuples come first, one per transaction the driver appears in,
    scanned in transaction order 1 -> 3.
  - OUTGOING tuples come second, same scan order.

Address rule (the third element of every tuple) -- three tuple shapes,
where "the key driver" means the driver whose task list is being built:

  i)   (Px, Sx|Dx, address) -- INCOMING. address = the address of the
       predecessor (Sx or Dx) -- i.e. whoever is sending the product.
  ii)  (Dx, Px, address)    -- OUTGOING to another driver. address = the
       KEY driver's OWN address (the key driver is the one sending here).
  iii) (Bx, Px, address)    -- OUTGOING to a buyer. address = that buyer's
       own address.

These were reverse-engineered from a worked example and verified against
all 18 tuples it contained; see PROJECT_CONTEXT.md for the check.

Key order in the returned dict matches `ordered_driver_labels` exactly --
this is meant to be fed the traversal order of the driver priority linked
list from priority.py, so the driver with the lowest priority value has
its task list built (and appears in the dict) first.
"""


def compute_driver_tasks(transactions, ordered_driver_labels, addresses):
    tasks = {}

    for driver_label in ordered_driver_labels:
        incoming = []
        outgoing = []

        for txn in transactions:
            full_chain = [txn["seller_label"], *txn["driver_chain"], txn["buyer_label"]]
            if driver_label not in full_chain:
                continue

            index = full_chain.index(driver_label)
            product = f"P{txn['id']}"
            predecessor = full_chain[index - 1]
            successor = full_chain[index + 1]

            # Rule (i): incoming -- address of the sender (predecessor).
            incoming.append((product, predecessor, addresses[predecessor]))

            if successor.startswith("D"):
                # Rule (ii): outgoing to another driver -- address of the
                # key driver itself (the one doing the sending).
                outgoing.append((successor, product, addresses[driver_label]))
            else:
                # Rule (iii): outgoing to a buyer -- address of that buyer.
                outgoing.append((successor, product, addresses[successor]))

        tasks[driver_label] = incoming + outgoing

    return tasks
