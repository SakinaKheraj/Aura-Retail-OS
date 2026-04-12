# ============================================================
# FILE: core/central_registry.py
# MEMBER: Kalagi [202512037]
# PATTERN: Singleton (skeleton)
# ============================================================

class CentralRegistry:
    """
    Singleton — only one instance exists across the whole system.
    Stores global config (city name, version, kiosk settings)
    and system-wide status.

    TODO (Final Submission):
    - Load config from persistence/config.json on startup
    - Save config on every set() call
    - Trigger events when status changes (EmergencyModeActivated etc.)
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = {}
            cls._instance._system_status = "ACTIVE"
        return cls._instance

    def set(self, key: str, value):
        """Store a config value."""
        self._config[key] = value

    def get(self, key: str):
        """Get a config value by key. Returns None if not found."""
        return self._config.get(key)

    def get_system_status(self) -> str:
        return self._system_status

    def set_system_status(self, status: str):
        """
        Valid statuses: ACTIVE | MAINTENANCE | EMERGENCY | SHUTDOWN
        TODO (Final): validate, log, and broadcast status change event
        """
        self._system_status = status
        print(f"[CentralRegistry] Status → {status}")
