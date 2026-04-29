# Software Design Document
## Aura Retail OS

**Project Context:** IT620 — Object Oriented Programming  
**Group:** 28  
**Team Members:** 
- Kalagi [202512037]
- Digvijay [202512008]
- Sakina [202512046]
- Aayushi [202512101]

---

## 1. Executive Summary
**Aura Retail OS** is a modular, high-performance platform designed to power autonomous retail kiosks in the smart city of Zephyrus. The system decoupling high-level business logic from low-level hardware interactions and payment integrations ensures adaptability across diverse environments such as hospitals, metro stations, and disaster zones. This document outlines the architectural choices and object-oriented design patterns utilized to achieve a scalable, maintainable, and cohesive software system.

## 2. System Architecture
The application is structured around five primary, loosely coupled subsystems. This layered approach adheres to the principles of high cohesion and low coupling.

### Architectural Layout
- **`core/`**: Orchestrates high-level business operations. It acts as the brain of the kiosk, providing base classes, factory provisioning, and a unified interface for the rest of the application.
- **`inventory/`**: Manages product lifecycles, nested product bundles, stock derivation, and secure proxy access to critical data.
- **`payment/`**: Unifies external, heterogeneous payment APIs into a single, standardized processing pipeline.
- **`hardware/`**: Abstracts physical dispensing logic and allows dynamic attachment of specialized hardware features (like refrigeration or solar monitoring).
- **`persistence/`**: Manages data serialization, allowing system state to be saved and restored across sessions.

## 3. Object-Oriented Design Patterns

Aura Retail OS extensively implements "Gang of Four" (GoF) design patterns to solve common architectural challenges.

### 3.1 Structural Patterns

#### **Composite Pattern**
- **Subsystem:** `inventory` (`product.py`)
- **Implementation:** The `Product` (leaf) and `ProductBundle` (composite) classes share a common interface. This allows nested products (e.g., an Emergency Relief Kit containing Aspirin and Bandages) to automatically aggregate pricing (`get_price()`) and compute maximum available stock dynamically without the client distinguishing between individual items and bundles.

#### **Adapter Pattern**
- **Subsystem:** `payment` (`adapters.py`)
- **Implementation:** Various external payment interfaces (`UPIAPI`, `CreditCardAPI`, `WalletAPI`) have incompatible structures. The adapter pattern wraps these disparate APIs under a unified `PaymentGateway` interface, meaning the core `purchase_item` logic never needs to change when a new payment provider is added.

#### **Facade Pattern**
- **Subsystem:** `core` (`kiosk.py`)
- **Implementation:** The `KioskInterface` provides a simplified, high-level interface to the complex subsystems (Inventory, Hardware, Payment, Persistence). Instead of clients managing subsystem interactions manually, they invoke single methods like `run_diagnostics()` or `purchase()`.

#### **Bridge Pattern**
- **Subsystem:** `hardware` (`dispenser.py`)
- **Implementation:** Decouples the abstract dispenser logic from physical motor implementations. This ensures that the system can support different types of vending machines (e.g., spiral dispensers vs. robotic arms) without altering the high-level kiosk logic.

#### **Decorator Pattern**
- **Subsystem:** `hardware` (`modules.py`)
- **Implementation:** Hardware capabilities can be dynamically augmented at runtime. For example, a base kiosk can be wrapped in a `RefrigerationModule` or `SolarMonitoringModule`. This enables modular hardware upgrades without subclassing every possible combination of kiosk features.

#### **Proxy Pattern**
- **Subsystem:** `inventory` (`inventory_manager.py`)
- **Implementation:** An `InventoryAccessProxy` stands between the client and the underlying inventory system. It is responsible for logging, securing access, and validating state before performing operations on the sensitive inventory records.

### 3.2 Creational Patterns

#### **Abstract Factory Pattern**
- **Subsystem:** `core` (`kiosk_factory.py`)
- **Implementation:** The `KioskFactory` provides an interface for creating families of related objects without specifying their concrete classes. It handles the consistent provisioning of different kiosk types (`PharmacyKiosk`, `FoodKiosk`, `EmergencyReliefKiosk`) ensuring that they are initialized with compatible hardware and inventory modules.

#### **Singleton Pattern**
- **Subsystem:** `core` (`central_registry.py`)
- **Implementation:** The `CentralRegistry` acts as a single, globally accessible instance that tracks system-wide configuration, transaction logs, and overall kiosk network status.

### 3.3 Behavioral Patterns

#### **Command Pattern**
- **Subsystem:** `core` (`commands.py`)
- **Implementation:** User operations (such as making a purchase, processing a refund, or running diagnostics) are encapsulated as objects. This parameterizes the invoker with different requests, supports queuing, and paves the way for easily implementing undo/rollback operations on failed transactions.

## 4. Team Responsibilities

The implementation was divided to ensure specialized focus on distinct architectural layers:

| Member | Subsystem | Key Contributions |
| :--- | :--- | :--- |
| **Kalagi** | `core/` | Implemented abstract/concrete Kiosk classes, Facade (`KioskInterface`), Factory (`KioskFactory`), Singleton (`CentralRegistry`), and Command pattern structures. |
| **Digvijay** | `inventory/` | Built the Composite structure for products/bundles, the `InventoryManager`, and the security layer using the Proxy Pattern. Handled dynamic stock derivation. |
| **Sakina** | `payment/` | Designed the `PaymentGateway` and implemented Adapter pattern for 3rd-party integration. Managed transaction atomicity and error states. |
| **Aayushi** | `hardware/` | Abstracted hardware via the Bridge pattern. Implemented the runtime Decorator pattern for modules (Refrigeration, Solar). Handled hardware constraints. |

## 5. System Execution Flow

When a user executes the application (`simulation.py`):
1. **Initialization:** The user interacts with the CLI to select a kiosk type. The `KioskFactory` provisions the correct instance.
2. **Dynamic Augmentation:** The user can opt to attach hardware modules (e.g., refrigeration). The system uses the Decorator to wrap the existing instance.
3. **Transaction Request:** The user selects an item (resolving through the Composite pattern). 
4. **Validation:** The `InventoryAccessProxy` checks constraints (e.g., stock limits).
5. **Payment Processing:** The request is passed to the unified `PaymentGateway`, which delegates to the specific `Adapter`.
6. **Dispensing:** If successful, the hardware subsystem triggers the `Dispenser` (via Bridge).
7. **State Persistence:** Finally, data is committed by the persistence manager, updating records in `inventory.json`.

---
*Generated based on the Aura Retail OS implementation for IT620.*
