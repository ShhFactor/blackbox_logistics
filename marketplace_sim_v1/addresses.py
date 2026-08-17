"""
Assigns a unique random "address" letter to every node in the people pool
(the 6 buyer/seller labels + the 5 driver labels = 11 nodes total), drawn
from a fixed 11-letter set so every node gets exactly one letter and no two
nodes ever share one.
"""

import random

ADDRESS_LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]


def assign_addresses(node_labels):
    """
    Shuffle ADDRESS_LETTERS and zip it with node_labels, giving back
    {label: letter} with every letter from the set used exactly once.

    node_labels must contain exactly len(ADDRESS_LETTERS) entries -- with
    the current config (3 transactions -> 6 buyer/seller labels, 5 driver
    labels) that's always 11.
    """
    if len(node_labels) != len(ADDRESS_LETTERS):
        raise ValueError(
            f"Expected exactly {len(ADDRESS_LETTERS)} node labels to address, "
            f"got {len(node_labels)}"
        )

    shuffled_letters = random.sample(ADDRESS_LETTERS, len(ADDRESS_LETTERS))
    return dict(zip(node_labels, shuffled_letters))
