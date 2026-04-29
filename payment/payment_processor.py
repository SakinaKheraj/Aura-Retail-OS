# ============================================================
# FILE: payment/payment_processor.py
# MEMBER: Sakina [202512046]
# PATTERN: Adapter (FULLY IMPLEMENTED)
# ============================================================

from abc import ABC, abstractmethod


# ============================================================
# TARGET INTERFACE
# ============================================================
#
# This is what the kiosk expects every payment provider to look like.
# The kiosk ONLY calls methods defined here.
# It never knows which real provider is underneath.
# ============================================================


class PaymentGateway(ABC):
    """
    Target interface for the Adapter pattern.

    Every payment provider — credit card, UPI, wallet —
    must be adapted to this interface.

    The kiosk calls:
        gateway.process_payment(user_id, amount)
        gateway.refund_payment(transaction_id)
        gateway.get_transaction_status(transaction_id)

    It never calls make_payment(), initiate_upi_transfer(), or
    deduct_balance() — those belong to the incompatible legacy systems.
    """

    @abstractmethod
    def process_payment(self, user_id: str, amount: float) -> bool:
        """
        Charge the user for a purchase.
        Returns True if payment succeeded, False otherwise.
        """
        pass

    @abstractmethod
    def refund_payment(self, transaction_id: str) -> bool:
        """
        Reverse a previous payment.
        Returns True if refund succeeded.
        TODO (Final Submission): look up amount from transaction log
        """
        pass

    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> str:
        """
        Return current status of a transaction.
        Possible values: 'COMPLETED', 'PENDING', 'FAILED', 'NOT_FOUND'
        """
        pass


# ============================================================
# ADAPTEES — incompatible legacy / third-party systems
# ============================================================
#
# These represent external SDKs that cannot be changed.
# Their method names, arguments, and return types all differ.
# The Adapter classes (in adapters.py) translate between
# PaymentGateway calls and these incompatible APIs.
# ============================================================


class CreditCardAPI:
    """
    Third-party credit card payment SDK.
    Incompatible interface:
        make_payment(card_number, amount) → dict
        cancel_payment(txn_id) → bool
        check_status(txn_id) → str
    """

    def make_payment(self, card_number: str, amount: float) -> dict:
        """Process a credit card charge. Returns status dict."""
        print(f"  [CreditCardAPI] Charging ₹{amount:.2f} to card ...{card_number[-4:]}")
        return {
            "status": "SUCCESS",
            "txn_id": f"CC_{abs(hash(card_number + str(amount)))}"
        }

    def cancel_payment(self, txn_id: str) -> bool:
        """Cancel/void a previous charge."""
        print(f"  [CreditCardAPI] Cancelling transaction {txn_id}")
        return True

    def check_status(self, txn_id: str) -> str:
        """Check status of a transaction."""
        return "COMPLETED"


class UPISystem:
    """
    UPI payment provider SDK.
    Incompatible interface:
        initiate_upi_transfer(upi_id, rupees) → str (txn_id)
        reverse_upi_transfer(upi_txn_id) → bool
        query_transfer(upi_txn_id) → str
    """

    def initiate_upi_transfer(self, upi_id: str, rupees: float) -> str:
        """Send money to a UPI ID. Returns a transaction ID string."""
        print(f"  [UPISystem] Sending ₹{rupees:.2f} → UPI: {upi_id}")
        return f"UPI_{abs(hash(upi_id + str(rupees)))}"

    def reverse_upi_transfer(self, upi_txn_id: str) -> bool:
        """Reverse a UPI transfer."""
        print(f"  [UPISystem] Reversing transfer {upi_txn_id}")
        return True

    def query_transfer(self, upi_txn_id: str) -> str:
        """Query status of a UPI transfer."""
        return "SUCCESS"


class WalletService:
    """
    Digital wallet provider SDK.
    Incompatible interface:
        deduct_balance(wallet_id, amount) → dict
        add_balance(wallet_id, amount) → None
        get_balance(wallet_id) → float
    """

    def deduct_balance(self, wallet_id: str, amount: float) -> dict:
        """Deduct money from a wallet. Returns result dict."""
        print(f"  [WalletService] Deducting ₹{amount:.2f} from wallet '{wallet_id}'")
        return {
            "success": True,
            "ref": f"WLT_{abs(hash(wallet_id + str(amount)))}"
        }

    def add_balance(self, wallet_id: str, amount: float):
        """Add money back to a wallet (refund)."""
        print(f"  [WalletService] Refunding ₹{amount:.2f} to wallet '{wallet_id}'")

    def get_balance(self, wallet_id: str) -> float:
        """Get current wallet balance."""
        return 5000.0   # mock value
