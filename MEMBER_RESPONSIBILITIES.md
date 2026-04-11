# Member Responsibilities — Aura Retail OS

This document outlines the subsystem ownership and implementation responsibilities for each team member in Group 28.

### 1. Kalagi [202512037] — Kiosk Core & Facade
**Subsystems**: `core/`
- **Responsibilities**:
    - Implementation of `Kiosk` abstract base and concrete subclasses (`PharmacyKiosk`, `FoodKiosk`, `EmergencyReliefKiosk`).
    - Development of the **Facade Pattern** via `KioskInterface` to simplify high-level operations.
    - Implementation of the **Singleton Pattern** for `CentralRegistry`.
    - Coordination of subsystem communication via the `KioskFactory` (**Abstract Factory Pattern**).
    - Designing the system-wide command structure (**Command Pattern**) for operations like purchase and refund.

### 2. Digvijay [202512008] — Inventory System & Security
**Subsystems**: `inventory/`
- **Responsibilities**:
    - Implementation of the **Composite Pattern** for `Product` and `ProductBundle` to handle nested item structures.
    - Development of the `InventoryManager` for stock tracking and persistence.
    - Implementation of the **Proxy Pattern** (`InventoryAccessProxy`) to secure all access to the inventory layer.
    - Handling derived stock computations and ensuring inventory consistency during transactions.

### 3. Sakina [202512046] — Payment System
**Subsystems**: `payment/`
- **Responsibilities**:
    - Designing the unified `PaymentGateway` interface.
    - Implementing the **Adapter Pattern** for various third-party providers (`UPIAdapter`, `CreditCardAdapter`, `WalletAdapter`).
    - Ensuring atomic behavior in transactions (payment verification followed by dispensing confirmation).
    - Managing transaction validation states and error handling during payment processing.

### 4. Aayushi [202512101] — Hardware & Modular Platform
**Subsystems**: `hardware/`
- **Responsibilities**:
    - Designing the `Dispenser` interface and its variants using the **Bridge Pattern** to decouple logic from hardware.
    - Developing optional hardware modules (`RefrigerationModule`, `SolarMonitoringModule`, `NetworkModule`).
    - Implementing the **Decorator Pattern** to allow dynamic attachment of these modules at runtime without modifying kiosk code.
    - Handling hardware-level constraints (e.g., blocking products if refrigeration is required but unavailable).
