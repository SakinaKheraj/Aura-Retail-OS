# ============================================================
# FILE: persistence/persistence_manager.py
# MEMBER: Kalagi [202512037]
# STATUS: Skeleton (Subtask 2)
# ============================================================

import json
import csv
import os


class PersistenceManager:
    """
    Handles reading and writing system state to files.

    Files used:
        persistence/inventory.json    ← product stock data
        persistence/transactions.csv  ← transaction history
        persistence/config.json       ← CentralRegistry config

    TODO (Final Submission):
    - load_inventory()   → restore products on startup
    - load_config()      → restore CentralRegistry settings on startup
    - save_transaction() → called after every purchase/refund
    - All methods should handle file-not-found gracefully
    """

    def __init__(self, base_dir: str = "persistence"):
        self._base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def save_inventory(self, data: dict, filename: str = "inventory.json"):
        """Save inventory dict to JSON file."""
        filepath = os.path.join(self._base_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[PersistenceManager] Inventory saved → {filepath}")

    def load_inventory(self, filename: str = "inventory.json") -> dict:
        """Load inventory dict from JSON file. Returns {} if file not found."""
        filepath = os.path.join(self._base_dir, filename)
        if not os.path.exists(filepath):
            return {}
        with open(filepath, "r") as f:
            return json.load(f)

    def save_transaction(self, transaction: dict, filename: str = "transactions.csv"):
        """
        Append a transaction record to CSV.
        Expected keys: transaction_id, product_id, quantity, amount, status, timestamp

        TODO (Final Submission): call this after every successful purchase/refund
        """
        filepath = os.path.join(self._base_dir, filename)
        fieldnames = ["transaction_id", "product_id", "quantity", "amount", "status", "timestamp"]
        write_header = not os.path.exists(filepath)
        with open(filepath, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if write_header:
                writer.writeheader()
            writer.writerow(transaction)
        print(f"[PersistenceManager] Transaction saved → {filepath}")

    def save_config(self, config: dict, filename: str = "config.json"):
        """Save CentralRegistry config to JSON."""
        filepath = os.path.join(self._base_dir, filename)
        with open(filepath, "w") as f:
            json.dump(config, f, indent=2)
        print(f"[PersistenceManager] Config saved → {filepath}")

    def load_config(self, filename: str = "config.json") -> dict:
        """Load CentralRegistry config from JSON. Returns {} if not found."""
        filepath = os.path.join(self._base_dir, filename)
        if not os.path.exists(filepath):
            return {}
        with open(filepath, "r") as f:
            return json.load(f)
