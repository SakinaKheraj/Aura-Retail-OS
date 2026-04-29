# ============================================================
# FILE: core/kiosk_factory.py
# MEMBER: Kalagi [202512037]
# PATTERN: Abstract Factory (skeleton)
# ============================================================

from abc import ABC, abstractmethod
from .kiosk import Kiosk, PharmacyKiosk, FoodKiosk, EmergencyReliefKiosk
from hardware.dispenser import SpiralDispenser, RoboticArmDispenser, ConveyorDispenser
from inventory.inventory_manager import InventoryManager
from inventory.product import InventoryAccessProxy


class AbstractKioskFactory(ABC):
    """
    Abstract Factory interface.
    Each concrete factory creates compatible components for a specific kiosk type.
    """
    @abstractmethod
    def create_kiosk(self, kiosk_id: str, location: str) -> Kiosk:
        pass

    @abstractmethod
    def create_dispenser(self):
        pass


class PharmacyKioskFactory(AbstractKioskFactory):
    def create_kiosk(self, kiosk_id: str, location: str) -> PharmacyKiosk:
        return PharmacyKiosk(kiosk_id, location)

    def create_dispenser(self):
        return RoboticArmDispenser()


class FoodKioskFactory(AbstractKioskFactory):
    def create_kiosk(self, kiosk_id: str, location: str) -> FoodKiosk:
        return FoodKiosk(kiosk_id, location)

    def create_dispenser(self):
        return SpiralDispenser()


class EmergencyKioskFactory(AbstractKioskFactory):
    def create_kiosk(self, kiosk_id: str, location: str) -> EmergencyReliefKiosk:
        return EmergencyReliefKiosk(kiosk_id, location)

    def create_dispenser(self):
        return ConveyorDispenser()


class KioskFactory:
    """
    High-level factory that uses the Abstract Factory pattern to build kiosks.
    """

    @staticmethod
    def create_kiosk(kiosk_type: str, kiosk_id: str, location: str, payment_gateway):
        # build the concrete factory
        if kiosk_type == "pharmacy":
            factory = PharmacyKioskFactory()
        elif kiosk_type == "food":
            factory = FoodKioskFactory()
        elif kiosk_type == "emergency":
            factory = EmergencyKioskFactory()
        else:
            raise ValueError(f"Unknown kiosk type: {kiosk_type}")

        # create components
        kiosk = factory.create_kiosk(kiosk_id, location)
        dispenser = factory.create_dispenser()
        
        # build inventory subsystem (Proxy)
        manager = InventoryManager()
        manager.load_from_json() # Load state if exists
        proxy = InventoryAccessProxy(manager, authorized_roles=["admin", "user"])

        # wire everything
        kiosk.initialize(dispenser, proxy, payment_gateway)
        print(f"[KioskFactory] Created {kiosk_type} kiosk '{kiosk_id}' with {dispenser.get_type()}")
        
        return kiosk