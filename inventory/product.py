# ============================================================
# FILE: inventory/product.py
# MEMBER: Digvijay [202512008]
# ============================================================

from abc import ABC, abstractmethod
from persistence.persistence_manager import PersistenceManager


# ============================================================
# COMPOSITE PATTERN
# ============================================================
#
# Goal: Treat individual products and bundles of products
#       through the same interface.
#
# Structure:
#   ProductComponent  ← abstract base (the "component")
#   Product           ← leaf node (single item)
#   ProductBundle     ← composite node (contains other components)
#
# Key benefit: A bundle can contain other bundles (nested).
# The kiosk calls get_price() on any ProductComponent and
# gets the correct total — whether it's a single item or a
# deeply nested bundle — without any special-case logic.
# ============================================================


class ProductComponent(ABC):
    """
    Abstract component interface.
    Both Product (leaf) and ProductBundle (composite) implement this.
    """

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        """Returns the unit price of the component (computed recursively for bundles)."""
        pass

    @abstractmethod
    def add_stock(self, quantity: int):
        pass

    @abstractmethod
    def reduce_stock(self, quantity: int):
        pass

    @abstractmethod
    def display(self, indent: int = 0):
        pass


class Product(ProductComponent):
    """
    LEAF NODE in the Composite tree.
    Represents an individual item (e.g. Paracetamol).
    """

    def __init__(self, product_id: str, name: str, price: float, quantity: int, 
                 requires_refrigeration: bool = False, is_essential: bool = False):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.requires_refrigeration = requires_refrigeration
        self.is_essential = is_essential

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return self.price

    def get_quantity(self) -> int:
        return self.quantity

    def add_stock(self, quantity: int):
        self.quantity += quantity

    def reduce_stock(self, quantity: int):
        self.quantity -= quantity

    def display(self, indent: int = 0):
        pad = "    " * indent
        ref_tag = " [COLD]" if getattr(self, "requires_refrigeration", False) else ""
        print(f"{pad}└─ [Product] {self.name + ref_tag:<25} ₹{self.price:<8.2f} (Stock: {self.quantity})")


class ProductBundle(ProductComponent):
    """
    COMPOSITE NODE in the Composite tree.
    Can contain Products or other ProductBundles.
    """

    def __init__(self, bundle_id: str, name: str):
        self.product_id = bundle_id  # Bundle also acts as a product
        self.name = name
        self._children = []  # List of child components

    def add(self, component: ProductComponent):
        self._children.append(component)

    def remove(self, component: ProductComponent):
        self._children.remove(component)

    def get_name(self) -> str:
        return self.name

    def get_price(self) -> float:
        return sum(item.get_price() for item in self._children)

    def get_quantity(self) -> int:
        if not self._children:
            return 0
        return min(item.get_quantity() for item in self._children)

    def add_stock(self, quantity: int):
        """Restocking a bundle restocks every item in it."""
        for item in self._children:
            item.add_stock(quantity)

    def reduce_stock(self, quantity: int):
        """Purchasing a bundle reduces stock for every item in it."""
        for item in self._children:
            item.reduce_stock(quantity)

    def display(self, indent: int = 0):
        pad = "    " * indent
        print(f"{pad}▼ [Bundle]  {self.name:<25} Total: ₹{self.get_price():.2f}")
        for item in self._children:
            item.display(indent + 1)


# ============================================================
# PROXY PATTERN
# ============================================================
#
# Goal: Control all access to InventoryManager.
#       No subsystem talks to InventoryManager directly —
#       everything goes through this proxy.
#
# Responsibilities:
#   1. Authorization — only allowed roles can read/write
#   2. Logging       — every access attempt is printed
#   3. Blocking      — raises PermissionError for unauthorized roles
# ============================================================


class InventoryAccessProxy:
    """
    Proxy for InventoryManager.
    """

    def __init__(self, inventory_manager, authorized_roles: list):
        self._manager = inventory_manager           # the real subject
        self._authorized_roles = authorized_roles   # e.g. ["admin", "user"]
        self._persistence = PersistenceManager()

    # ── internal helper ────────────────────────────────────
    def _check_auth(self, role: str):
        """Raise PermissionError if role is not in authorized list."""
        if role not in self._authorized_roles:
            raise PermissionError(
                f"[InventoryProxy] DENIED — role '{role}' is not authorized."
            )

    # ── proxy methods ───────────────────────────────────────
    def get_product(self, product_id: str, role: str = "user") -> ProductComponent:
        """
        Auth check + logging before fetching product.
        """
        self._check_auth(role)
        product = self._manager.get_product(product_id)
        if product:
            print(f"[InventoryProxy] GRANTED — get_product('{product_id}') for role '{role}'")
        return product

    def get_available_stock(self, product_id: str) -> int:
        """
        Derived attribute — computed from current inventory.
        """
        return self._manager.get_available_stock(product_id)

    def add_stock(self, product_id: str, quantity: int, role: str = "admin"):
        """
        Admin-only operation.
        """
        self._check_auth(role)
        print(f"[InventoryProxy] LOGGED — add_stock('{product_id}', {quantity}) by role '{role}'")
        self._manager.add_stock(product_id, quantity)
        # Persistent save
        self._manager.save_to_json()

    def reduce_stock(self, product_id: str, quantity: int):
        """
        Called internally after a successful purchase.
        """
        print(f"[InventoryProxy] Stock reduced — '{product_id}' by {quantity}")
        self._manager.reduce_stock(product_id, quantity)
        # Persistent save
        self._manager.save_to_json()