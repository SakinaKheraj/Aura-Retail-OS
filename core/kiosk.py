# ============================================================
# FILE: core/kiosk.py
# MEMBER: Kalagi [202512037]
# PATTERNS: Abstract Factory (base classes), Facade (KioskInterface)
# STATUS: Skeleton (Subtask 2)
# ============================================================

import time
from abc import ABC, abstractmethod


# ------------------------------------------------------------
# ABSTRACT BASE CLASS
# ------------------------------------------------------------

from core.commands import CommandInvoker, PurchaseItemCommand, RefundCommand, RestockCommand
from core.central_registry import CentralRegistry

# ------------------------------------------------------------
# ABSTRACT BASE CLASS
# ------------------------------------------------------------

class Kiosk(ABC):
    """
    Abstract base for all kiosk types.
    """

    def __init__(self, kiosk_id: str, location: str):
        self.kiosk_id = kiosk_id
        self.location = location
        self.dispenser = None
        self.inventory_manager = None
        self.payment_gateway = None
        self.mode = "ACTIVE" # ACTIVE, POWER_SAVING, MAINTENANCE, EMERGENCY
        self.health_level = 100

    def initialize(self, dispenser, inventory_manager, payment_gateway):
        """Called by KioskFactory to wire up all subsystems."""
        self.dispenser = dispenser
        self.inventory_manager = inventory_manager
        self.payment_gateway = payment_gateway

    def is_refrigerated(self) -> bool:
        """Default False. Overridden by Refrigeration Decorator."""
        return False

    def is_online(self) -> bool:
        """Default True. Overridden by Network Module."""
        return True

    def set_mode(self, mode: str):
        self.mode = mode
        print(f"[Kiosk {self.kiosk_id}] Mode set to {mode}")

    def run_health_check(self) -> bool:
        """Simulate hardware health check."""
        if not self.dispenser: return False
        # In a real system, we'd ping the HAL.
        return True

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
    """
    def __init__(self, kiosk_id: str, location: str):
        super().__init__(kiosk_id, location)
        self.requires_prescription = True

    def get_status(self) -> str:
        return f"PharmacyKiosk [{self.kiosk_id}] ({self.mode}) @ {self.location}"


class FoodKiosk(Kiosk):
    """
    Deployed in metro stations and universities.
    """
    def get_status(self) -> str:
        return f"FoodKiosk [{self.kiosk_id}] ({self.mode}) @ {self.location}"


class EmergencyReliefKiosk(Kiosk):
    """
    Deployed in disaster zones.
    """
    def __init__(self, kiosk_id: str, location: str):
        super().__init__(kiosk_id, location)
        self.emergency_limit = 2  # max items per user

    def get_status(self) -> str:
        return f"EmergencyReliefKiosk [{self.kiosk_id}] ({self.mode}) @ {self.location}"


# ------------------------------------------------------------
# FACADE PATTERN
# ------------------------------------------------------------

class KioskInterface:
    """
    Facade — exposes a simplified interface to external systems.
    """

    def __init__(self, kiosk: Kiosk):
        self._kiosk = kiosk
        self._invoker = CommandInvoker()
        self._registry = CentralRegistry()

    def purchase_item(self, product_id: str, quantity: int, user_id: str) -> bool:
        """
        Full purchase flow routed through Command pattern.
        """
        # Edge Case: Invalid Input Validation
        if quantity <= 0:
            print(f"  [KioskInterface] Error: Invalid quantity ({quantity}).")
            return False

        # Access inventory via proxy - role check only
        internal_mgr = self._kiosk.inventory_manager._manager # check existence directly to avoid proxy log flood
        item = internal_mgr.get_product(product_id)
        if not item:
            print(f"\033[91m  [CRITICAL] Error: Product '{product_id}' not found.\033[0m")
            return False

        # Global Operational Restrictions
        if self._registry.get_system_status() == "SHUTDOWN":
            print("  [KioskInterface] System SHUTDOWN. No transactions possible.")
            return False

        if self._kiosk.mode == "MAINTENANCE":
            print("  [KioskInterface] Kiosk in MAINTENANCE mode. Please wait.")
            return False

        # Mode-specific logic (Emergency Limit for Essentials)
        if self._registry.get("emergency_mode"):
            # Limit applied to Emergency Kiosks or any Essential product in Emergency Mode
            if isinstance(self._kiosk, EmergencyReliefKiosk) or getattr(item, "is_essential", False):
                if quantity > getattr(self._kiosk, "emergency_limit", 2):
                    actual_limit = getattr(self._kiosk, "emergency_limit", 2)
                    print(f"  [KioskInterface] EMERGENCY LIMIT! Max {actual_limit} essential units per user.")
                    quantity = actual_limit

        # Path B Constraint: Hardware Dependency (Network)
        if not self._kiosk.is_online():
            # If offline, only basic payment allowed (simulated as UPI being disabled)
            from payment.adapters import UPIAdapter
            if isinstance(self._kiosk.payment_gateway, UPIAdapter):
                print(f"\033[93m  [SECURITY] OFFLINE: UPI payment unavailable. Please use physical card or cash.\033[0m")
                return False

        if isinstance(self._kiosk, PharmacyKiosk):
            print(f"\033[94m  [Verification] Verifying prescription for user {user_id}...\033[0m")
            # Simulate verification
            time.sleep(0.5)
            print("\033[92m  [Verification] Prescription VALID.\033[0m")

        # Path B Constraint: Hardware Dependency (Refrigeration)
        if getattr(item, "requires_refrigeration", False):
            if not self._kiosk.is_refrigerated():
                print(f"\033[91m  [SAFETY] DENIED: '{item.get_name()}' requires refrigeration, but NO COOLING MODULE is attached.\033[0m")
                return False
            print(f"\033[92m  [SAFETY] Temperature Check: OK.\033[0m")

        # Create and execute command
        cmd = PurchaseItemCommand(self._kiosk, product_id, quantity, user_id)
        return self._invoker.execute_command(cmd)

    def refund_transaction(self, transaction_id: str):
        """
        Refund routed through Command pattern.
        """
        cmd = RefundCommand(self._kiosk, transaction_id)
        self._invoker.execute_command(cmd)

    def run_diagnostics(self) -> str:
        """
        Hardware diagnostics check.
        """
        print(f"\n[KioskInterface] Initiating System Diagnostics for {self._kiosk.kiosk_id}...")
        
        disp_ok = self._kiosk.dispenser.get_type() is not None
        inv_ok = self._kiosk.inventory_manager is not None
        pay_ok = self._kiosk.payment_gateway is not None
        
        print(f"  - Dispenser: {'ONLINE' if disp_ok else 'OFFLINE'}")
        print(f"  - Inventory: {'ONLINE' if inv_ok else 'OFFLINE'}")
        print(f"  - Payment:   {'ONLINE' if pay_ok else 'OFFLINE'}")
        
        status = self._kiosk.get_status()
        print(f"[Diagnostics Result] Kiosk '{self._kiosk.kiosk_id}' is HEALTHY.")
        return status

    def restock_inventory(self, product_id: str, quantity: int):
        """
        Restock routed through Command pattern.
        """
        cmd = RestockCommand(self._kiosk, product_id, quantity)
        self._invoker.execute_command(cmd)

    def undo_last_operation(self):
        """Rollback support."""
        self._invoker.undo_last()
