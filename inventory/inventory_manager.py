# ============================================================
# FILE: inventory/inventory_manager.py
# MEMBER: Digvijay [202512008]
# STATUS: Complete (Subtask 2)
# ============================================================

import json
import os


class InventoryManager:
    """
    Core inventory store.
    Holds all products and their current stock levels.

    IMPORTANT: This class is never accessed directly by the kiosk.
    All access goes through InventoryAccessProxy (Proxy pattern).

    Storage: dict mapping product_id → ProductComponent

    TODO (Final Submission):
    - load_from_json() — restore inventory on kiosk startup
    - Reserve items during active transactions (prevent oversell)
    - Mark items unavailable when required hardware module is offline
    """

    def __init__(self):
        self._products = {}   # product_id (str) → ProductComponent

    # ── registration ────────────────────────────────────────

    def add_product(self, product):
        """Register a Product or ProductBundle in the inventory."""
        self._products[product.product_id] = product
        print(f"[InventoryManager] Registered '{product.get_name()}' (id: {product.product_id})")

    # ── read ─────────────────────────────────────────────────

    def get_product(self, product_id: str):
        """Return ProductComponent for given id, or None."""
        return self._products.get(product_id)

    def get_available_stock(self, product_id: str) -> int:
        """
        DERIVED ATTRIBUTE — not stored directly, computed on demand.
        Returns current quantity for the product.
        Returns 0 if product not found.

        TODO (Final Submission):
        - Subtract items reserved in active transactions
        - Return 0 if required hardware module is unavailable
        """
        product = self._products.get(product_id)
        if product is None:
            return 0
        return product.get_quantity()

    # ── write ─────────────────────────────────────────────────

    def add_stock(self, product_id: str, quantity: int):
        """Increase stock for a product (restock operation)."""
        if product_id in self._products:
            self._products[product_id].quantity += quantity
        else:
            print(f"[InventoryManager] WARNING: '{product_id}' not found — cannot restock.")

    def reduce_stock(self, product_id: str, quantity: int):
        """Decrease stock after a confirmed purchase."""
        if product_id in self._products:
            self._products[product_id].quantity -= quantity
        else:
            print(f"[InventoryManager] WARNING: '{product_id}' not found — cannot reduce stock.")

    # ── display ───────────────────────────────────────────────

    def list_all(self):
        """Print all registered products and their current stock."""
        print("[InventoryManager] Current stock:")
        for pid, p in self._products.items():
            print(f"  {pid}  {p.get_name():<35} qty: {p.get_quantity():<6} ₹{p.get_price():.2f}")

    # ── persistence ───────────────────────────────────────────

    def save_to_json(self, filepath: str = "persistence/inventory.json"):
        """Save current inventory snapshot to JSON file."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data = {}
        for pid, p in self._products.items():
            data[pid] = {
                "name": p.get_name(),
                "price": p.get_price(),
                "quantity": p.get_quantity()
            }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[InventoryManager] Saved to '{filepath}'")

    def load_from_json(self, filepath: str = "persistence/inventory.json"):
        """
        TODO (Final Submission):
        Restore inventory from JSON on kiosk startup.
        Will need to reconstruct Product objects from saved data.
        """
        pass  # skeleton — implement in Final Submission
