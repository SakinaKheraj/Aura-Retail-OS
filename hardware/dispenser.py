# ============================================================
# FILE: hardware/dispenser.py
# MEMBER: Aayushi [202512101]
# PATTERN: Bridge (skeleton)
# STATUS: Skeleton (Subtask 2)
# ============================================================

from abc import ABC, abstractmethod


# ============================================================
# BRIDGE PATTERN — Skeleton
# ============================================================
#
# Goal: Separate the high-level dispensing abstraction from
#       the low-level hardware implementation.
#
# The kiosk calls dispenser.dispense(product_id).
# It does not care if the hardware underneath is a spiral,
# a robotic arm, or a conveyor belt.
#
# Swapping hardware = change which Dispenser subclass is used.
# The kiosk code does not change at all.
#
# TODO (Final Submission):
# - Add is_healthy() method for hardware diagnostics
# - Add calibrate() method called before each use
# - Raise HardwareFailureEvent if dispense() fails
# - Connect to HAL (Hardware Abstraction Layer)
# ============================================================


class Dispenser(ABC):
    """
    Abstraction interface for all dispensing hardware.
    """

    @abstractmethod
    def dispense(self, product_id: str) -> bool:
        """Physically dispense the product."""
        pass

    @abstractmethod
    def retract(self, product_id: str) -> bool:
        """Cancel a dispense in progress."""
        pass

    @abstractmethod
    def get_type(self) -> str:
        """Return the name/type of this dispenser hardware."""
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        """Return True if hardware is operational."""
        pass

    @abstractmethod
    def calibrate(self):
        """Calibrate motors."""
        pass


class SpiralDispenser(Dispenser):
    """Standard spiral/coil vending dispenser."""

    def dispense(self, product_id: str) -> bool:
        print(f"  [SpiralDispenser] Rotating coil → dispensing '{product_id}'")
        # Simulate high success rate
        return True

    def retract(self, product_id: str) -> bool:
        print(f"  [SpiralDispenser] Reversing coil for '{product_id}'")
        return True

    def get_type(self) -> str:
        return "SpiralDispenser"

    def is_healthy(self) -> bool:
        return True

    def calibrate(self):
        print(f"  [SpiralDispenser] Calibrating coil rotation...")


class RoboticArmDispenser(Dispenser):
    """Robotic arm with gripper for precise item retrieval."""

    def dispense(self, product_id: str) -> bool:
        print(f"  [RoboticArmDispenser] Arm picking '{product_id}' → placing in tray")
        return True

    def retract(self, product_id: str) -> bool:
        print(f"  [RoboticArmDispenser] Arm returning to home position")
        return True

    def get_type(self) -> str:
        return "RoboticArmDispenser"

    def is_healthy(self) -> bool:
        return True

    def calibrate(self):
        print(f"  [RoboticArmDispenser] Calibrating arm XYZ coordinates...")


class ConveyorDispenser(Dispenser):
    """Conveyor belt system for large or heavy items."""

    def dispense(self, product_id: str) -> bool:
        print(f"  [ConveyorDispenser] Belt moving '{product_id}' to exit slot")
        return True

    def retract(self, product_id: str) -> bool:
        print(f"  [ConveyorDispenser] Belt reversing")
        return True

    def get_type(self) -> str:
        return "ConveyorDispenser"

    def is_healthy(self) -> bool:
        return True

    def calibrate(self):
        print(f"  [ConveyorDispenser] Calibrating belt speed and tension...")
