# ============================================================
# FILE: core/kiosk.py
# MEMBER: Kalagi [202512037]
# PATTERNS: Abstract Factory (base classes), Facade (KioskInterface)
# STATUS: Skeleton (Subtask 2)
# ============================================================

from abc import ABC, abstractmethod


# ------------------------------------------------------------
# ABSTRACT BASE CLASS
# ------------------------------------------------------------

class Kiosk(ABC):
    """
    Abstract base for all kiosk types.
    Subclasses: PharmacyKiosk, FoodKiosk, EmergencyReliefKiosk

    Each kiosk holds references to its subsystems:
    - dispenser        → hardware layer
    - inventory_manager → inventory proxy
    - payment_gateway  → payment adapter

    These are injected by KioskFactory (not set here directly).

    TODO (Final Submission):
    - Add operational mode (ACTIVE / POWER_SAVING / MAINTENANCE / EMERGENCY)
    - Auto-restrict operations based on mode
    - Add hardware health check
    """

    def __init__(self, kiosk_id: str, location: str):
        self.kiosk_id = kiosk_id
        self.location = location
        self.dispenser = None
        self.inventory_manager = None
        self.payment_gateway = None

    def initialize(self, dispenser, inventory_manager, payment_gateway):
        """Called by KioskFactory to wire up all subsystems."""
        self.dispenser = dispenser
        self.inventory_manager = inventory_manager
        self.payment_gateway = payment_gateway

    @abstractmethod
    def get_status(self) -> str:
        """Return a human-readable status string for this kiosk."""
        pass


# ------------------------------------------------------------
# CONCRETE KIOSK TYPES
# ------------------------------------------------------------

class PharmacyKiosk(Kiosk):
    """
    Deployed in hospitals.
    Uses RoboticArmDispenser for precise medication dispensing.
    TODO (Final): add prescription verification before purchase
    """
    def __init__(self, kiosk_id: str, location: str):
        super().__init__(kiosk_id, location)
        self.requires_prescription = True  # TODO (Final): enforce this

    def get_status(self) -> str:
        return f"PharmacyKiosk [{self.kiosk_id}] @ {self.location}"


class FoodKiosk(Kiosk):
    """
    Deployed in metro stations and universities.
    Uses SpiralDispenser for standard vending.
    """
    def get_status(self) -> str:
        return f"FoodKiosk [{self.kiosk_id}] @ {self.location}"


class EmergencyReliefKiosk(Kiosk):
    """
    Deployed in disaster zones.
    Enforces a per-user purchase limit during emergency mode.
    TODO (Final): integrate with CentralRegistry emergency status
    """
    def __init__(self, kiosk_id: str, location: str):
        super().__init__(kiosk_id, location)
        self.emergency_limit = 2  # max items per user

    def get_status(self) -> str:
        return f"EmergencyReliefKiosk [{self.kiosk_id}] @ {self.location}"


# ------------------------------------------------------------
# FACADE PATTERN
# ------------------------------------------------------------

class KioskInterface:
    """
    Facade — exposes a simplified interface to external systems.
    Users, city monitoring, and admin systems talk ONLY to this class.
    Internal complexity (inventory proxy, payment adapter, dispenser) is hidden.

    Methods:
        purchase_item()       → buy a product
        refund_transaction()  → reverse a purchase
        run_diagnostics()     → get kiosk health report
        restock_inventory()   → add stock to a product

    TODO (Final Submission):
    - Route all operations through Command pattern (PurchaseItemCommand etc.)
    - Add transaction logging to persistence layer
    - Enforce emergency purchase limits
    - Handle atomic transaction failure + rollback
    """

    def __init__(self, kiosk: Kiosk):
        self._kiosk = kiosk

    def purchase_item(self, product_id: str, quantity: int, user_id: str) -> bool:
        """
        Full purchase flow (Facade simplifies this for the user):
        1. Access Inventory Proxy
        2. Check Stock (Derived Attribute)
        3. Authorize Payment (Adapter)
        4. Dispense via Hardware (Bridge)
        5. Reduce Inventory Stock
        """
        proxy = self._kiosk.inventory_manager
        item = proxy.get_product(product_id)
        
        if not item:
            print(f"  [ERROR] Product '{product_id}' not found in registry.")
            return False

        available = proxy.get_available_stock(product_id)
        if available < quantity:
            print(f"  [DENIED] Insufficient stock for '{item.get_name()}'.")
            print(f"           Requested: {quantity}, Available: {available}")
            return False

        price_per_unit = item.get_price()
        total_price = price_per_unit * quantity
        print(f"  [Kiosk] Requesting ₹{total_price:.2f} for {quantity}x {item.get_name()}")
        
        # Payment via Adapter
        if self._kiosk.payment_gateway.process_payment(user_id, total_price):
            # Hardware dispense via Bridge
            if self._kiosk.dispenser.dispense(product_id):
                proxy.reduce_stock(product_id, quantity)
                print(f"  [SUCCESS] Transaction complete. Enjoy your {item.get_name()}!")
                return True
            else:
                print(f"  [CRITICAL] Hardware failure during dispense. Initiating refund...")
                self._kiosk.payment_gateway.refund_payment("FAIL_AUTO")
                return False
        
        print(f"  [ERROR] Payment failed for user {user_id}.")
        return False

    def refund_transaction(self, transaction_id: str):
        """
        TODO (Final Submission):
        - Look up transaction from persistence layer
        - Call payment_gateway.refund_payment()
        - Restock inventory
        - Log refund
        """
        print(f"[KioskInterface] Refund for '{transaction_id}' — TODO in Final Submission")

    def run_diagnostics(self) -> str:
        """
        TODO (Final Submission):
        - Check dispenser health
        - Check inventory manager connectivity
        - Check payment gateway connectivity
        - Check all attached hardware modules
        """
        status = self._kiosk.get_status()
        print(f"[KioskInterface] Diagnostics OK → {status}")
        return status

    def restock_inventory(self, product_id: str, quantity: int):
        """
        TODO (Final Submission): wrap in RestockCommand, require admin role
        """
        self._kiosk.inventory_manager.add_stock(product_id, quantity)
        print(f"[KioskInterface] Restocked '{product_id}' +{quantity} units")
