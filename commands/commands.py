# ============================================================
# FILE: commands/commands.py
# MEMBER: Kalagi [202512037]
# PATTERN: Command (skeleton)
# STATUS: Skeleton (Subtask 2) — Full implementation in Final Submission
# ============================================================

from abc import ABC, abstractmethod


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
# TODO (Final Submission):
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

    TODO (Final Submission):
    execute():
        1. Check stock via proxy
        2. Process payment via gateway
        3. Dispense product via dispenser
        4. Reduce stock
        5. Save transaction to CSV
    undo():
        1. Refund payment
        2. Restore stock
    """

    def __init__(self, product_id: str, quantity: int, user_id: str):
        self.product_id = product_id
        self.quantity = quantity
        self.user_id = user_id

    def execute(self):
        # TODO (Final Submission): implement full purchase flow
        print(f"[PurchaseItemCommand] STUB — not yet implemented")

    def undo(self):
        # TODO (Final Submission): refund + restock
        print(f"[PurchaseItemCommand] STUB — undo() not yet implemented")

    def log(self) -> str:
        return (f"PurchaseItemCommand("
                f"product={self.product_id}, "
                f"qty={self.quantity}, "
                f"user={self.user_id})")


class RefundCommand(Command):
    """
    Encapsulates a refund operation.

    TODO (Final Submission):
    execute():
        1. Look up original transaction
        2. Call gateway.refund_payment()
        3. Restock inventory
        4. Log refund to CSV
    undo():
        1. Re-charge the customer (cancel the refund)
    """

    def __init__(self, transaction_id: str):
        self.transaction_id = transaction_id

    def execute(self):
        # TODO (Final Submission): implement refund flow
        print(f"[RefundCommand] STUB — not yet implemented")

    def undo(self):
        # TODO (Final Submission): cancel the refund
        print(f"[RefundCommand] STUB — undo() not yet implemented")

    def log(self) -> str:
        return f"RefundCommand(transaction={self.transaction_id})"


class RestockCommand(Command):
    """
    Encapsulates a restock operation.

    TODO (Final Submission):
    execute():
        1. Verify admin role via proxy
        2. Call proxy.add_stock()
        3. Log restock event
    undo():
        1. Reduce stock back to previous level
    """

    def __init__(self, product_id: str, quantity: int):
        self.product_id = product_id
        self.quantity = quantity

    def execute(self):
        # TODO (Final Submission): implement restock flow
        print(f"[RestockCommand] STUB — not yet implemented")

    def undo(self):
        # TODO (Final Submission): reverse the restock
        print(f"[RestockCommand] STUB — undo() not yet implemented")

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
