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
    All kiosk code talks to this interface only.
    Never talks to SpiralDispenser or RoboticArmDispenser directly.
    """

    @abstractmethod
    def dispense(self, product_id: str) -> bool:
        """
        Physically dispense the product with given ID.
        Returns True on success, False on hardware failure.
        TODO (Final): raise HardwareFailureEvent on False
        """
        pass

    @abstractmethod
    def retract(self, product_id: str) -> bool:
        """
        Cancel a dispense in progress (e.g. after payment failure).
        Returns True on success.
        TODO (Final): called by transaction rollback mechanism
        """
        pass

    @abstractmethod
    def get_type(self) -> str:
        """Return the name/type of this dispenser hardware."""
        pass


class SpiralDispenser(Dispenser):
    """
    Standard spiral/coil vending dispenser.
    Motor rotates a spiral coil to push items forward into the tray.
    Used in: FoodKiosk, EmergencyReliefKiosk

    TODO (Final Submission):
    - Implement real motor control via HAL
    - Detect jam condition and raise HardwareFailureEvent
    - Add calibrate() to set coil rotation amount per product
    """

    def dispense(self, product_id: str) -> bool:
        # TODO: send rotate command to spiral motor controller
        print(f"  [SpiralDispenser] Rotating coil → dispensing '{product_id}'")
        return True

    def retract(self, product_id: str) -> bool:
        # TODO: reverse motor rotation to pull item back
        print(f"  [SpiralDispenser] Reversing coil for '{product_id}'")
        return True

    def get_type(self) -> str:
        return "SpiralDispenser"


class RoboticArmDispenser(Dispenser):
    """
    Robotic arm with gripper for precise item retrieval.
    Used in: PharmacyKiosk (medication needs exact placement)

    TODO (Final Submission):
    - Implement arm movement via HAL motor commands
    - Implement gripper open/close
    - Add item drop detection sensor
    - Return item to shelf on retract
    """

    def dispense(self, product_id: str) -> bool:
        # TODO: move arm to product slot, grip item, move to output tray
        print(f"  [RoboticArmDispenser] Arm picking '{product_id}' → placing in tray")
        return True

    def retract(self, product_id: str) -> bool:
        # TODO: open gripper, return arm to home position
        print(f"  [RoboticArmDispenser] Arm returning to home position")
        return True

    def get_type(self) -> str:
        return "RoboticArmDispenser"


class ConveyorDispenser(Dispenser):
    """
    Conveyor belt system for large or heavy items.
    Used in: bulk emergency supply distribution

    TODO (Final Submission):
    - Implement belt start/stop/reverse via HAL
    - Detect item position with optical sensor
    - Stop belt when item reaches exit point
    """

    def dispense(self, product_id: str) -> bool:
        # TODO: start belt moving towards exit slot
        print(f"  [ConveyorDispenser] Belt moving '{product_id}' to exit slot")
        return True

    def retract(self, product_id: str) -> bool:
        # TODO: reverse belt to pull item back
        print(f"  [ConveyorDispenser] Belt reversing")
        return True

    def get_type(self) -> str:
        return "ConveyorDispenser"
