"""
Selects the people involved in a simulation run (buyers, sellers, drivers)
and builds the transaction records that other modules fill in further.
"""

import random

from .config import NUM_TRANSACTIONS, NUM_DRIVERS


def pick_people(pool, rng=None):
    """Select 6 unique buyer/seller names + 5 unique driver names (all disjoint)."""
    random_source = rng if rng is not None else random
    chosen = random_source.sample(
        pool, 2 * NUM_TRANSACTIONS + NUM_DRIVERS
    )  # 6 + 5 = 11
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
