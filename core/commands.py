# ============================================================
# FILE: core/commands.py
# MEMBER: Sakina [202512046]
# PATTERN: Command
# ============================================================

import time
from abc import ABC, abstractmethod
from datetime import datetime
from persistence.persistence_manager import PersistenceManager


# ============================================================
# COMMAND PATTERN — Skeleton
# ============================================================
#
# Goal: Encapsulate each operation (purchase, refund, restock)
#       as an object. This allows:
#       - Logging every operation
#       - Undoing operations (rollback)
#       - Queuing operations
#
# Structure:
#   Command          ← abstract interface
#   PurchaseItemCommand, RefundCommand, RestockCommand ← concrete
#   CommandInvoker   ← stores and executes commands
#
# TODO :
# - implement execute() for all concrete commands with real logic
# - implement undo() for rollback support
# - CommandInvoker maintains full undo stack
# - KioskInterface routes all operations through CommandInvoker
# ============================================================


class Command(ABC):
    """Abstract command interface. Every operation is a Command."""

    @abstractmethod
    def execute(self):
        """Run the operation."""
        pass

    @abstractmethod
    def undo(self):
        """Reverse the operation (rollback)."""
        pass

    @abstractmethod
    def log(self) -> str:
        """Return a string description for logging."""
        pass


class PurchaseItemCommand(Command):
    """
    Encapsulates a purchase operation.
    """

    def __init__(self, kiosk, product_id: str, quantity: int, user_id: str):
        self.kiosk = kiosk
        self.product_id = product_id
        self.quantity = quantity
        self.user_id = user_id
        self.transaction_id = f"TXN_{int(time.time())}"
        self.persistence = PersistenceManager()
        self._total_amount = 0.0
        self._success = False

    def execute(self):
        proxy = self.kiosk.inventory_manager
        item = proxy.get_product(self.product_id)
        
        if not item:
            print(f"  [Command] Error: Product '{self.product_id}' not found.")
            return False

        # ── Constraint: Network Connectivity for Digital Payments ──
        if not self.kiosk.is_online():
            from payment.adapters import UPIAdapter, WalletAdapter
            if isinstance(self.kiosk.payment_gateway, (UPIAdapter, WalletAdapter)):
                print(f"  [SECURITY] OFFLINE: Digital payment requires network connectivity. Please use physical card.")
                return False

        available = proxy.get_available_stock(self.product_id)
        if available < self.quantity:
            print(f"  [Command] Error: Insufficient stock ({available} available).")
            return False

        # ── Constraint: Hardware Dependency (Refrigeration) ──
        if getattr(item, 'requires_refrigeration', False):
            if "Refrigeration" not in self.kiosk.get_status():
                print(f"  [SAFETY] DENIED — '{item.get_name()}' requires refrigeration, but NO COOLING MODULE is attached.")
                return False
            else:
                print(f"  [SAFETY] Temperature Check: OK")

        # ── Constraint: Emergency Mode Limits ──
        from core.central_registry import CentralRegistry
        if CentralRegistry().get_system_status() == "EMERGENCY":
            if getattr(item, 'is_essential', False) and self.quantity > 2:
                print(f"  [EMERGENCY LIMIT] Maximum 2 units per transaction for essential items during emergency mode.")
                print(f"                    Adjusting quantity to 2.")
                self.quantity = 2

        # ── Path B: Dynamic Pricing Policy (Strategy Pattern) ──
        from core.pricing import StandardPricing, EmergencyPricing
        policy = StandardPricing()
        if CentralRegistry().get_system_status() == "EMERGENCY":
            policy = EmergencyPricing()

        self._total_amount = policy.compute_price(item.get_price(), self.quantity)
        
        # Payment
        if self.kiosk.payment_gateway.process_payment(self.user_id, self._total_amount):
            # Hardware dispense
            if self.kiosk.dispenser.dispense(self.product_id):
                # Update inventory
                proxy.reduce_stock(self.product_id, self.quantity)
                self._success = True
                
                # Log to persistence
                self.persistence.save_transaction({
                    "transaction_id": self.transaction_id,
                    "product_id": self.product_id,
                    "quantity": self.quantity,
                    "amount": self._total_amount,
                    "status": "SUCCESS",
                    "timestamp": datetime.now().isoformat()
                })
                print(f"  [Command] Purchase successful. ID: {self.transaction_id}")
                return True
            else:
                print(f"  [Command] Hardware failure! Initiating automatic refund...")
                self.kiosk.payment_gateway.refund_payment(self.transaction_id)
                return False
        
        return False

    def undo(self):
        if self._success:
            print(f"  [Command] Rolling back transaction {self.transaction_id}...")
            self.kiosk.payment_gateway.refund_payment(self.transaction_id)
            self.kiosk.inventory_manager.add_stock(self.product_id, self.quantity, role="admin")
            self._success = False

    def log(self) -> str:
        return (f"PurchaseItemCommand("
                f"id={self.transaction_id}, "
                f"product={self.product_id}, "
                f"qty={self.quantity}, "
                f"user={self.user_id})")


class RefundCommand(Command):
    """
    Encapsulates a refund operation.
    """

    def __init__(self, kiosk, transaction_id: str):
        self.kiosk = kiosk
        self.transaction_id = transaction_id
        self.persistence = PersistenceManager()
        self._original_product = None
        self._original_qty = 0

    def execute(self):
        # In a real system, we'd look up the CSV. For simulation, 
        # we'll assume we have the transaction data or just perform a generic refund.
        print(f"  [Command] Processing refund for {self.transaction_id}...")
        if self.kiosk.payment_gateway.refund_payment(self.transaction_id):
            # If we knew product/qty, we'd restock. 
            # For simplicity, we'll mark it as successful.
            self.persistence.save_transaction({
                "transaction_id": f"REFUND_{self.transaction_id}",
                "product_id": "N/A",
                "quantity": 0,
                "amount": 0.0,
                "status": "REFUNDED",
                "timestamp": datetime.now().isoformat()
            })
            return True
        return False

    def undo(self):
        print(f"  [Command] Undo refund not supported (cannot re-charge automatically).")

    def log(self) -> str:
        return f"RefundCommand(transaction={self.transaction_id})"


class RestockCommand(Command):
    """
    Encapsulates a restock operation.
    """

    def __init__(self, kiosk, product_id: str, quantity: int):
        self.kiosk = kiosk
        self.product_id = product_id
        self.quantity = quantity
        self._previous_stock = 0

    def execute(self):
        self._previous_stock = self.kiosk.inventory_manager.get_available_stock(self.product_id)
        self.kiosk.inventory_manager.add_stock(self.product_id, self.quantity, role="admin")
        print(f"  [Command] Restocked {self.product_id} +{self.quantity}. New total: {self._previous_stock + self.quantity}")
        return True

    def undo(self):
        self.kiosk.inventory_manager.reduce_stock(self.product_id, self.quantity)
        print(f"  [Command] Undoing restock of {self.product_id}. Restored to {self._previous_stock}.")

    def log(self) -> str:
        return f"RestockCommand(product={self.product_id}, qty={self.quantity})"


class CommandInvoker:
    """
    Stores and executes commands. Keeps full history for undo support.

    TODO (Final Submission):
    - Save command log to persistence/transactions.csv
    - Support undo_last() via undo stack
    - Support get_history() for audit trail
    """

    def __init__(self):
        self._history: list[Command] = []

    def execute_command(self, command: Command):
        """Execute a command and store it in history."""
        print(f"[CommandInvoker] Executing: {command.log()}")
        command.execute()
        self._history.append(command)

    def undo_last(self):
        """Undo the most recently executed command."""
        if self._history:
            last = self._history.pop()
            print(f"[CommandInvoker] Undoing: {last.log()}")
            last.undo()
        else:
            print("[CommandInvoker] Nothing to undo.")

    def get_history(self) -> list[str]:
        """Return list of log strings for all executed commands."""
        return [cmd.log() for cmd in self._history]
