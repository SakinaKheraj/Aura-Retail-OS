# ============================================================
# FILE: core/central_registry.py
# MEMBER: Kalagi [202512037]
# PATTERN: Singleton (improved skeleton)
# ============================================================

from persistence.persistence_manager import PersistenceManager


class CentralRegistry:
    """
    Singleton — only one instance exists across the whole system.
    Stores global config and system-wide status.
    """

    _instance = None

    #  centralized constants (safe improvement)
    VALID_STATUSES = {"ACTIVE", "MAINTENANCE", "EMERGENCY", "SHUTDOWN"}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance._persistence = PersistenceManager()
            cls._instance._config = cls._instance._persistence.load_config()

            # Default values if not found in config
            if not cls._instance._config:
                cls._instance._config = {
                    "city": "Zephyrus",
                    "version": "3.0-final",
                    "emergency_mode": False
                }
                cls._instance.save()

            cls._instance._system_status = "ACTIVE"

        return cls._instance

    def set(self, key: str, value):
        """Store a config value and persist it."""
        self._config[key] = value
        self.save()

    def get(self, key: str):
        """Get a config value by key."""
        return self._config.get(key)

    def save(self):
        """Persist current config."""
        self._persistence.save_config(self._config)

    def get_system_status(self) -> str:
        return self._system_status

    def set_system_status(self, status: str):
        """
        Valid statuses: ACTIVE | MAINTENANCE | EMERGENCY | SHUTDOWN
        """
        if status not in self.VALID_STATUSES:
            print(f"[CentralRegistry] Invalid status attempted: {status}")
            return

        self._system_status = status

        # emergency flag handling (unchanged logic, cleaner structure)
        self._config["emergency_mode"] = (status == "EMERGENCY")

        self.save()
        print(f"[CentralRegistry] Status → {status}")