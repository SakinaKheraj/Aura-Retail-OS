# ============================================================
# FILE: core/central_registry.py
# MEMBER: Kalagi [202512037]
# PATTERN: Singleton (skeleton)
# ============================================================

from persistence.persistence_manager import PersistenceManager

class CentralRegistry:
    """
    Singleton — only one instance exists across the whole system.
    Stores global config (city name, version, kiosk settings)
    and system-wide status.
    """

    _instance = None

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
        """Get a config value by key. Returns None if not found."""
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
        valid_statuses = ["ACTIVE", "MAINTENANCE", "EMERGENCY", "SHUTDOWN"]
        if status in valid_statuses:
            self._system_status = status
            if status == "EMERGENCY":
                self._config["emergency_mode"] = True
            else:
                self._config["emergency_mode"] = False
            self.save()
            print(f"[CentralRegistry] Status → {status}")
        else:
            print(f"[CentralRegistry] Invalid status attempted: {status}")
