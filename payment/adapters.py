from payment.payment_processor import (
    PaymentGateway,
    CreditCardAPI,
    UPISystem,
    WalletService
)


# ============================================================
# HOW THE ADAPTER PATTERN WORKS HERE
# ============================================================
#
# Problem:
#   The kiosk needs to call process_payment(user_id, amount).
#   But CreditCardAPI uses make_payment(card_number, amount).
#   And UPISystem uses initiate_upi_transfer(upi_id, rupees).
#   And WalletService uses deduct_balance(wallet_id, amount).
#   All three have completely different method names and arguments.
#
# Solution:
#   Create one Adapter class per provider.
#   Each adapter:
#     - Inherits PaymentGateway (the target interface the kiosk expects)
#     - Holds an instance of the real provider (the adaptee)
#     - Translates each PaymentGateway call into the provider's call
#
# Result:
#   The kiosk always calls process_payment(user_id, amount).
#   The adapter translates this to whatever the real provider needs.
#   Switching providers = swap the adapter. Zero kiosk code changes.
# ============================================================


class CreditCardAdapter(PaymentGateway):
    """
    Adapts CreditCardAPI → PaymentGateway interface.

    Translation:
        process_payment(user_id, amount)  →  make_payment(card_number, amount)
        refund_payment(txn_id)            →  cancel_payment(txn_id)
        get_transaction_status(txn_id)    →  check_status(txn_id)
    """

    def __init__(self, card_number: str):
        self._api = CreditCardAPI()         # the real provider (adaptee)
        self._card_number = card_number
        self._last_txn_id = None

    def process_payment(self, user_id: str, amount: float) -> bool:
        # Translate: process_payment → make_payment
        result = self._api.make_payment(self._card_number, amount)
        if result.get("status") == "SUCCESS":
            self._last_txn_id = result.get("txn_id")
            print(f"  [CreditCardAdapter] Transaction ID: {self._last_txn_id}")
            return True
        return False

    def refund_payment(self, transaction_id: str) -> bool:
        # Translate: refund_payment → cancel_payment
        return self._api.cancel_payment(transaction_id)

    def get_transaction_status(self, transaction_id: str) -> str:
        # Translate: get_transaction_status → check_status
        return self._api.check_status(transaction_id)


class UPIAdapter(PaymentGateway):
    """
    Adapts UPISystem → PaymentGateway interface.

    Translation:
        process_payment(user_id, amount)  →  initiate_upi_transfer(upi_id, rupees)
        refund_payment(txn_id)            →  reverse_upi_transfer(upi_txn_id)
        get_transaction_status(txn_id)    →  query_transfer(upi_txn_id)
    """

    def __init__(self, upi_id: str):
        self._upi = UPISystem()             # the real provider (adaptee)
        self._upi_id = upi_id
        self._last_txn_id = None

    def process_payment(self, user_id: str, amount: float) -> bool:
        # Translate: process_payment → initiate_upi_transfer
        txn_id = self._upi.initiate_upi_transfer(self._upi_id, amount)
        if txn_id:
            self._last_txn_id = txn_id
            print(f"  [UPIAdapter] Transaction ID: {self._last_txn_id}")
            return True
        return False

    def refund_payment(self, transaction_id: str) -> bool:
        # Translate: refund_payment → reverse_upi_transfer
        return self._upi.reverse_upi_transfer(transaction_id)

    def get_transaction_status(self, transaction_id: str) -> str:
        # Translate: get_transaction_status → query_transfer
        return self._upi.query_transfer(transaction_id)


class WalletAdapter(PaymentGateway):
    """
    Adapts WalletService → PaymentGateway interface.

    Translation:
        process_payment(user_id, amount)  →  deduct_balance(wallet_id, amount)
        refund_payment(txn_id)            →  add_balance(wallet_id, amount)
        get_transaction_status(txn_id)    →  checks internal ref
    """

    def __init__(self, wallet_id: str):
        self._wallet = WalletService()      # the real provider (adaptee)
        self._wallet_id = wallet_id
        self._last_ref = None
        self._last_amount = 0.0             # saved for refund

    def process_payment(self, user_id: str, amount: float) -> bool:
        # Translate: process_payment → deduct_balance
        result = self._wallet.deduct_balance(self._wallet_id, amount)
        if result.get("success"):
            self._last_ref = result.get("ref")
            self._last_amount = amount
            print(f"  [WalletAdapter] Reference: {self._last_ref}")
            return True
        return False

    def refund_payment(self, transaction_id: str) -> bool:
        # Translate: refund_payment → add_balance
        self._wallet.add_balance(self._wallet_id, self._last_amount)
        return True

    def get_transaction_status(self, transaction_id: str) -> str:
        return "COMPLETED" if self._last_ref else "NOT_FOUND"