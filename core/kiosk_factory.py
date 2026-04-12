# ============================================================
# FILE: core/kiosk_factory.py
# MEMBER: Kalagi [202512037]
# PATTERN: Abstract Factory (skeleton)
# STATUS: Skeleton (Subtask 2)
# ============================================================

from .kiosk import PharmacyKiosk, FoodKiosk, EmergencyReliefKiosk
from hardware.dispenser import SpiralDispenser, RoboticArmDispenser
from inventory.inventory_manager import InventoryManager
from inventory.product import InventoryAccessProxy


class KioskFactory:
    """
    Factory that creates kiosk objects with all compatible components.

    Responsibilities:
    - Create the correct Kiosk subclass
    - Create the correct Dispenser for that kiosk type
    - Create an InventoryManager wrapped in an InventoryAccessProxy
    - Wire everything together via kiosk.initialize()

    TODO (Final Submission):
    - Split into separate factory subclasses:
        PharmacyKioskFactory, FoodKioskFactory, EmergencyKioskFactory
    - Each subclass creates its own PricingModule and VerificationModule
    - Register created kiosk in CentralRegistry
    """

    @staticmethod
    def create_kiosk(kiosk_type: str, kiosk_id: str, location: str, payment_gateway):
        """
        Create and return a fully initialized kiosk.

        Args:
            kiosk_type:      'pharmacy' | 'food' | 'emergency'
            kiosk_id:        unique string ID (e.g. 'K001')
            location:        human-readable location string
            payment_gateway: any PaymentGateway adapter instance

        Returns:
            Initialized Kiosk instance with all subsystems wired up
        """
        # Build inventory subsystem (same for all kiosk types in Subtask 2)
        manager = InventoryManager()
        proxy = InventoryAccessProxy(manager, authorized_roles=["admin", "user"])

        # Select kiosk type and matching dispenser
        if kiosk_type == "pharmacy":
            kiosk = PharmacyKiosk(kiosk_id, location)
            dispenser = RoboticArmDispenser()   # precise, for medication

        elif kiosk_type == "food":
            kiosk = FoodKiosk(kiosk_id, location)
            dispenser = SpiralDispenser()       # standard vending coil

        elif kiosk_type == "emergency":
            kiosk = EmergencyReliefKiosk(kiosk_id, location)
            dispenser = SpiralDispenser()

        else:
            raise ValueError(f"[KioskFactory] Unknown kiosk type: '{kiosk_type}'")

        # Wire all subsystems into the kiosk
        kiosk.initialize(dispenser, proxy, payment_gateway)
        print(f"[KioskFactory] Created '{kiosk_type}' kiosk '{kiosk_id}' at '{location}'")
        return kiosk
