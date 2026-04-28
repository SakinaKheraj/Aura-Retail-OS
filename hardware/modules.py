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
    Required for: insulin, vaccines, chilled food.

    TODO (Final Submission):
    - Read temperature from sensor every N seconds
    - If temperature exceeds threshold → raise HardwareFailureEvent
    - Block purchase of cold-storage products if module is offline
    """

    def __init__(self, temperature_celsius: float = 4.0):
        self.temperature = temperature_celsius
        self._active = False

    def attach(self, kiosk_id: str):
        self._active = True
        # TODO: start cooling hardware, connect temperature sensor
        print(f"  [RefrigerationModule] Attached to '{kiosk_id}' — target: {self.temperature}°C")

    def detach(self, kiosk_id: str):
        self._active = False
        # TODO: safely power down cooling unit
        print(f"  [RefrigerationModule] Detached from '{kiosk_id}'")

    def get_module_name(self) -> str:
        return f"Refrigeration({self.temperature}°C)"


class SolarMonitoringModule(HardwareModule):
    """
    Solar panel monitoring unit.
    Tracks power generation and battery charge state.

    TODO (Final Submission):
    - Read watt output from solar sensor
    - If output drops below threshold → trigger POWER_SAVING mode in kiosk
    - Report power data to City Monitoring System
    """

    def __init__(self):
        self.power_output_watts = 0.0

    def attach(self, kiosk_id: str):
        self.power_output_watts = 120.0
        # TODO: connect to solar panel sensor via HAL
        print(f"  [SolarMonitoringModule] Attached to '{kiosk_id}' — output: {self.power_output_watts}W")

    def detach(self, kiosk_id: str):
        self.power_output_watts = 0.0
        print(f"  [SolarMonitoringModule] Detached from '{kiosk_id}'")

    def get_module_name(self) -> str:
        return f"Solar({self.power_output_watts}W)"


class NetworkModule(HardwareModule):
    """
    Network connectivity module.
    Manages internet/intranet connection for the kiosk.

    TODO (Final Submission):
    - Ping city server every N seconds to check connectivity
    - If offline → raise NetworkFailureEvent
    - Restrict online payment methods if network is down
    - Report bandwidth usage to City Monitoring System
    """

    def __init__(self, bandwidth_mbps: float = 100.0):
        self.bandwidth = bandwidth_mbps
        self._connected = False

    def attach(self, kiosk_id: str):
        self._connected = True
        # TODO: initialize network interface via HAL
        print(f"  [NetworkModule] Attached to '{kiosk_id}' — {self.bandwidth} Mbps")

    def detach(self, kiosk_id: str):
        self._connected = False
        print(f"  [NetworkModule] Detached from '{kiosk_id}'")

    def get_module_name(self) -> str:
        return f"Network({self.bandwidth}Mbps)"