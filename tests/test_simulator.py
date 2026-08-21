import contextlib
import io
import math
import os
from pathlib import Path
import subprocess
import sys
import unittest

import marketplace_sim_v1
from marketplace_sim_v1.addresses import ADDRESS_LETTERS
from marketplace_sim_v1.priority import (
    build_priority_linked_list,
    compute_driver_positions,
    compute_priority_values,
)
from marketplace_sim_v1.tasks import compute_driver_tasks


REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_PATH = REPO_ROOT / "marketplace_sim_v1" / "main.py"


class ImportAndDeterminismTests(unittest.TestCase):
    def test_import_has_no_console_output(self):
        command = [
            sys.executable,
            "-c",
            "import marketplace_sim_v1; import marketplace_sim_v1.main",
        ]
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=True,
        )

        self.assertEqual(completed.stdout, "")
        self.assertEqual(completed.stderr, "")

    def test_same_seed_produces_same_result(self):
        self.assertEqual(
            marketplace_sim_v1.run_simulation(seed=2026),
            marketplace_sim_v1.run_simulation(seed=2026),
        )

    def test_different_seeds_can_produce_different_results(self):
        self.assertNotEqual(
            marketplace_sim_v1.run_simulation(seed=1),
            marketplace_sim_v1.run_simulation(seed=2),
        )

    def test_seed_and_rng_are_mutually_exclusive(self):
        with self.assertRaises(ValueError):
            marketplace_sim_v1.run_simulation(seed=1, rng=object())


class SimulationInvariantTests(unittest.TestCase):
    def setUp(self):
        self.result = marketplace_sim_v1.run_simulation(seed=2026)

    def test_people_are_unique_and_role_sets_are_disjoint(self):
        buyer_names = {txn["buyer_name"] for txn in self.result.transactions}
        seller_names = {txn["seller_name"] for txn in self.result.transactions}
        driver_names = set(self.result.driver_label_to_name.values())

        self.assertEqual(len(buyer_names), 3)
        self.assertEqual(len(seller_names), 3)
        self.assertEqual(len(driver_names), 5)
        self.assertTrue(buyer_names.isdisjoint(seller_names))
        self.assertTrue(buyer_names.isdisjoint(driver_names))
        self.assertTrue(seller_names.isdisjoint(driver_names))
        self.assertEqual(len(buyer_names | seller_names | driver_names), 11)

    def test_transaction_and_driver_capacity_invariants(self):
        self.assertEqual(len(self.result.transactions), 3)

        all_assignments = []
        for transaction in self.result.transactions:
            chain = transaction["driver_chain"]
            self.assertEqual(len(chain), 3)
            self.assertEqual(len(set(chain)), 3)
            all_assignments.extend(chain)

        self.assertEqual(len(all_assignments), 9)
        self.assertEqual(sum(self.result.driver_counts.values()), 9)
        self.assertTrue(
            all(count <= 2 for count in self.result.driver_counts.values())
        )
        self.assertEqual(sorted(self.result.driver_counts.values()), [1, 2, 2, 2, 2])

    def test_addresses_are_a_bijection(self):
        self.assertEqual(len(self.result.addresses), 11)
        self.assertEqual(set(self.result.addresses.values()), set(ADDRESS_LETTERS))

    def test_priority_and_task_order_match(self):
        priority_values = [
            self.result.driver_values[label]
            for label in self.result.ordered_driver_labels
        ]
        self.assertEqual(priority_values, sorted(priority_values))
        self.assertEqual(
            list(self.result.driver_tasks), self.result.ordered_driver_labels
        )


class FixedExampleRegressionTests(unittest.TestCase):
    def setUp(self):
        self.driver_labels = ["D1", "D2", "D3", "D4", "D5"]
        self.transactions = [
            {
                "id": 1,
                "seller_label": "S1",
                "buyer_label": "B1",
                "driver_chain": ["D3", "D2", "D5"],
            },
            {
                "id": 2,
                "seller_label": "S2",
                "buyer_label": "B2",
                "driver_chain": ["D4", "D2", "D5"],
            },
            {
                "id": 3,
                "seller_label": "S3",
                "buyer_label": "B3",
                "driver_chain": ["D1", "D4", "D3"],
            },
        ]
        self.addresses = {
            "S1": "a",
            "B1": "b",
            "S2": "c",
            "B2": "d",
            "S3": "e",
            "B3": "f",
            "D1": "g",
            "D2": "h",
            "D3": "i",
            "D4": "j",
            "D5": "k",
        }

    def test_positions_values_and_linked_list_order(self):
        driver_xy = compute_driver_positions(
            self.transactions, self.driver_labels
        )
        self.assertEqual(
            driver_xy,
            {
                "D1": (1, 0),
                "D2": (2, 2),
                "D3": (1, 3),
                "D4": (1, 2),
                "D5": (3, 3),
            },
        )

        driver_values = compute_priority_values(driver_xy)
        self.assertAlmostEqual(driver_values["D1"], 1.0)
        self.assertAlmostEqual(driver_values["D2"], math.sqrt(8))
        self.assertAlmostEqual(driver_values["D3"], math.sqrt(10))
        self.assertAlmostEqual(driver_values["D4"], math.sqrt(5))
        self.assertAlmostEqual(driver_values["D5"], math.sqrt(18))

        priority_list = build_priority_linked_list(
            self.driver_labels, driver_xy, driver_values
        )
        self.assertEqual(
            [node.label for node in priority_list],
            ["D1", "D4", "D2", "D3", "D5"],
        )

    def test_stable_ties_preserve_original_driver_order(self):
        driver_xy = {
            "D1": (1, 0),
            "D2": (0, 1),
            "D3": (2, 0),
            "D4": (0, 2),
            "D5": (3, 0),
        }
        driver_values = compute_priority_values(driver_xy)
        priority_list = build_priority_linked_list(
            self.driver_labels, driver_xy, driver_values
        )

        self.assertEqual(
            [node.label for node in priority_list],
            ["D1", "D2", "D3", "D4", "D5"],
        )

    def test_driver_tasks_follow_handoff_and_address_rules(self):
        ordered_labels = ["D1", "D4", "D2", "D3", "D5"]
        tasks = compute_driver_tasks(
            self.transactions, ordered_labels, self.addresses
        )

        self.assertEqual(list(tasks), ordered_labels)
        self.assertEqual(tasks["D1"], [("P3", "S3", "e"), ("D4", "P3", "g")])
        self.assertEqual(
            tasks["D4"],
            [
                ("P2", "S2", "c"),
                ("P3", "D1", "g"),
                ("D2", "P2", "j"),
                ("D3", "P3", "j"),
            ],
        )
        self.assertEqual(
            tasks["D2"],
            [
                ("P1", "D3", "i"),
                ("P2", "D4", "j"),
                ("D5", "P1", "h"),
                ("D5", "P2", "h"),
            ],
        )
        self.assertEqual(
            tasks["D3"],
            [
                ("P1", "S1", "a"),
                ("P3", "D4", "j"),
                ("D2", "P1", "i"),
                ("B3", "P3", "f"),
            ],
        )
        self.assertEqual(
            tasks["D5"],
            [
                ("P1", "D2", "h"),
                ("P2", "D2", "h"),
                ("B1", "P1", "b"),
                ("B2", "P2", "d"),
            ],
        )

        for driver, driver_tasks in tasks.items():
            occurrence_count = sum(
                driver in transaction["driver_chain"]
                for transaction in self.transactions
            )
            incoming = driver_tasks[:occurrence_count]
            outgoing = driver_tasks[occurrence_count:]
            self.assertTrue(all(item[0].startswith("P") for item in incoming))
            self.assertTrue(all(item[1].startswith("P") for item in outgoing))


class CommandLineRegressionTests(unittest.TestCase):
    def test_existing_cli_runs_and_sections_remain_ordered(self):
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        completed = subprocess.run(
            [sys.executable, str(CLI_PATH)],
            cwd=REPO_ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=True,
        )

        expected_headers = [
            "=== Map Output ===",
            "=== People Pool Selected ===",
            "=== Initial Hashmap (driver -> deliveries) ===",
            "=== Transactions ===",
            "=== Final Hashmap (driver -> total deliveries) ===",
            "=== Driver Position Hashmap (driver -> (x, y)) ===",
            "=== Driver Priority Values: sqrt(x^2 + y^2) ===",
            "=== Driver Priority Linked List (ascending) ===",
            "=== Driver Tasks ===",
        ]
        header_positions = [
            completed.stdout.index(header) for header in expected_headers
        ]
        self.assertEqual(header_positions, sorted(header_positions))


if __name__ == "__main__":
    unittest.main()
