# ============================================================
# FILE: core/pricing.py
# MEMBER: Sakina [202512046]
# PATTERN: Strategy (Pricing Policies)
# ============================================================

from abc import ABC, abstractmethod

class PricingPolicy(ABC):
    """
    Strategy pattern for dynamic price computation.
    """
    @abstractmethod
    def compute_price(self, base_price: float, quantity: int) -> float:
        pass

class StandardPricing(PricingPolicy):
    def compute_price(self, base_price: float, quantity: int) -> float:
        return base_price * quantity

class EmergencyPricing(PricingPolicy):
    """Adds a 50% surcharge during emergencies."""
    def compute_price(self, base_price: float, quantity: int) -> float:
        return (base_price * 1.5) * quantity

class DiscountPricing(PricingPolicy):
    """10% discount for bulk purchases (>= 5 units)."""
    def compute_price(self, base_price: float, quantity: int) -> float:
        total = base_price * quantity
        if quantity >= 5:
            return total * 0.9
        return total
