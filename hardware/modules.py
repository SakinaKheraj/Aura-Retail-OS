# ============================================================
# FILE: hardware/modules.py
# MEMBER: Aayushi [202512101]
# PATTERN: Decorator (skeleton)
# STATUS: Skeleton (Subtask 2)
# ============================================================

from abc import ABC, abstractmethod


# ============================================================
# DECORATOR PATTERN — Skeleton
# ============================================================
#
# Goal: Add optional hardware modules (refrigeration, solar,
#       network) to any kiosk at runtime WITHOUT modifying
#       the base Kiosk class.
#
# How it works:
#   KioskWithModule wraps a Kiosk object.
#   It adds a module's behavior to get_status().
#   Multiple modules can be stacked (chained decorators).
#
# Example:
#   kiosk = KioskFactory.create_kiosk("pharmacy", ...)
#   kiosk = KioskWithModule(kiosk, RefrigerationModule(4.0))
#   kiosk = KioskWithModule(kiosk, SolarMonitoringModule())
#   kiosk = KioskWithModule(kiosk, NetworkModule())
#   → each wrap adds another module without changing any class
#
# TODO (Final Submission):
# - Each module should raise events on failure
#   (e.g. RefrigerationModule raises HardwareFailureEvent if temp too high)
# - NetworkModule offline → restrict online payment methods
# - SolarModule low output → trigger POWER_SAVING mode
# - is_healthy() method for each module (used in diagnostics)
# ============================================================


class HardwareModule(ABC):
    """
    Interface for all optional hardware modules.
    Each module can be attached to or detached from a kiosk at runtime.
    """

    @abstractmethod
    def attach(self, kiosk_id: str):
        """
        Called when this module is added to a kiosk.
        Should initialize the hardware (start sensors, etc.)
        TODO (Final): connect to actual sensor via HAL
        """
        pass

    @abstractmethod
    def detach(self, kiosk_id: str):
        """
        Called when this module is removed from a kiosk.
        Should safely shut down the hardware.
        TODO (Final): safely power down, log detachment event
        """
        pass

    @abstractmethod
    def get_module_name(self) -> str:
        """Return a short identifier string for this module."""
        pass


class KioskWithModule:
    """
    Decorator class — wraps any Kiosk and adds one HardwareModule.

    Chaining example:
        kiosk = PharmacyKiosk(...)
        kiosk = KioskWithModule(kiosk, RefrigerationModule(2.0))
        kiosk = KioskWithModule(kiosk, NetworkModule())
        # kiosk.get_status() now shows both modules appended

    __getattr__ delegates all other attribute/method calls to
    the wrapped kiosk so the rest of the system works unchanged.
    """

    def __init__(self, kiosk, module: HardwareModule):
        self._kiosk = kiosk
        self._module = module
        self._module.attach(kiosk.kiosk_id)

    def get_status(self) -> str:
        """
        Extends the wrapped kiosk's status string with module info.
        If chained: each decorator appends its module name.
        """
        return self._kiosk.get_status() + f" | +{self._module.get_module_name()}"

    def is_refrigerated(self) -> bool:
        """
        Return True if THIS module is refrigeration or if WRAPPED kiosk has it.
        """
        from .modules import RefrigerationModule
        if isinstance(self._module, RefrigerationModule):
            return True
        return self._kiosk.is_refrigerated()

    def is_online(self) -> bool:
        """
        Return False if THIS is a NetworkModule and it is offline.
        """
        from .modules import NetworkModule
        if isinstance(self._module, NetworkModule):
            return self._module.is_online()
        return self._kiosk.is_online()

    def __getattr__(self, name):
        """
        Delegate any attribute/method not defined here
        to the wrapped kiosk (transparent pass-through).
        """
        return getattr(self._kiosk, name)


# ── CONCRETE MODULES ──────────────────────────────────────────

class RefrigerationModule(HardwareModule):
    """
    Cooling unit for temperature-sensitive products.
    """

    def __init__(self, temperature_celsius: float = 4.0):
        self.temperature = temperature_celsius
        self._active = False
        self._healthy = True

    def attach(self, kiosk_id: str):
        self._active = True
        print(f"  [RefrigerationModule] Attached to '{kiosk_id}' — monitoring sensor...")

    def detach(self, kiosk_id: str):
        self._active = False
        print(f"  [RefrigerationModule] Powering down cooling unit for '{kiosk_id}'")

    def get_module_name(self) -> str:
        return f"Refrigeration({self.temperature}°C)"

    def is_healthy(self) -> bool:
        # Simulation: 95% chance it's healthy
        import random
        self._healthy = random.random() > 0.05
        return self._healthy


class SolarMonitoringModule(HardwareModule):
    """
    Solar panel monitoring unit.
    """

    def __init__(self):
        self.power_output_watts = 120.0

    def attach(self, kiosk_id: str):
        print(f"  [SolarMonitoringModule] Attached to '{kiosk_id}' — reading photo-cells...")

    def detach(self, kiosk_id: str):
        print(f"  [SolarMonitoringModule] Disconnecting solar grid from '{kiosk_id}'")

    def get_module_name(self) -> str:
        return f"Solar({self.power_output_watts}W)"

    def check_output(self, kiosk):
        """If output is low, trigger power saving."""
        if self.power_output_watts < 50.0:
            kiosk.set_mode("POWER_SAVING")


class NetworkModule(HardwareModule):
    """
    Network connectivity module.
    """

    def __init__(self, bandwidth_mbps: float = 100.0):
        self.bandwidth = bandwidth_mbps
        self._connected = False # Testing offline behavior

    def attach(self, kiosk_id: str):
        print(f"  [NetworkModule] Attached to '{kiosk_id}' — initializing 5G/LTE link...")

    def detach(self, kiosk_id: str):
        print(f"  [NetworkModule] Dropping network link for '{kiosk_id}'")

    def get_module_name(self) -> str:
        return f"Network({self.bandwidth}Mbps)"

    def is_online(self) -> bool:
        return self._connected
