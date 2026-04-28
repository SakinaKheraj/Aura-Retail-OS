# Team Contributions — Aura Retail OS

**IT620 Object Oriented Programming · Path B · Project v2.0**

---

## Kalagi · 202512037 — System Architect
**Patterns: Abstract Factory, Singleton, Facade**

- Designed `AbstractKioskFactory` and concrete factories for Pharmacy, Food, and Emergency kiosks. Each factory guarantees compatible hardware pairing at boot — no mismatched components.
- Built `CentralRegistry` (Singleton) to hold one authoritative city-wide state, ensuring emergency mode broadcasts reach all active kiosk instances consistently.
- Implemented `KioskInterface` (Facade) as the single entry point for the simulation layer, hiding the internal complexity of commands, hardware, and inventory behind a clean API.
- Established the core system kernel and wiring between all modules.

---

## Digvijay · 202512008 — Inventory & Security Lead
**Patterns: Composite, Proxy**

- Built the `ProductComponent` hierarchy (Composite) so individual items and product bundles share one interface. Price totals and stock checks recurse through the tree without any special-casing.
- Implemented recursive price and stock calculations for nested composite objects.
- Developed `InventoryAccessProxy` to intercept all inventory operations, enforce role-based access (user vs. admin), and apply emergency purchase caps before anything reaches the real inventory.
- Integrated the JSON persistence layer so inventory state is saved and restored across sessions.

---

## Aayushi · 202512101 — Hardware HAL Lead
**Patterns: Bridge, Decorator**

- Architected the Hardware Abstraction Layer using the Bridge pattern, separating kiosk logic from motor implementations (Robotic Arm, Conveyor Belt, Spiral). Dispensers can be swapped without changing any business logic.
- Built the runtime upgrade system using Decorators. Attaching a Refrigeration, Solar, or Network module wraps the existing kiosk object — the base kiosk is never modified.
- Implemented health check and status reporting for all hardware components, including the OFFLINE state surfaced during emergency mode.

---

## Sakina · 202512046 — Payment & Transaction Lead
**Patterns: Adapter, Command**

- Implemented Adapters for UPI, Credit Card, and Digital Wallet APIs, unifying three incompatible vendor interfaces behind a single `PaymentGateway`. Adding a new payment method requires only a new adapter.
- Developed the Command pattern for transactions — each purchase is a self-contained, reversible object encapsulating payment, inventory change, and dispenser action.
- Engineered the multi-level undo and rollback mechanism: a single `undo()` call atomically reverts both payment and stock, with no partial states.
- Built the CSV-based audit trail logging every command execution and rollback.

---

## Pattern Ownership

| Member | Creational | Structural | Behavioural |
|:---|:---|:---|:---|
| Kalagi | Abstract Factory | Facade | Singleton |
| Digvijay | — | Composite, Proxy | — |
| Aayushi | — | Bridge, Decorator | — |
| Sakina | — | Adapter | Command |
