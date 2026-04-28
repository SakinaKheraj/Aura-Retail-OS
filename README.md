<div align="center">

```
 █████╗ ██╗   ██╗██████╗  █████╗     ██████╗ ███████╗
██╔══██╗██║   ██║██╔══██╗██╔══██╗   ██╔═══██╗██╔════╝
███████║██║   ██║██████╔╝███████║   ██║   ██║███████╗
██╔══██║██║   ██║██╔══██╗██╔══██║   ██║   ██║╚════██║
██║  ██║╚██████╔╝██║  ██║██║  ██║   ╚██████╔╝███████║
╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝
```

### Autonomous Smart-City Retail Infrastructure

**IT620 — Object Oriented Programming · Path B: Modular Hardware Platform**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![OOP Patterns](https://img.shields.io/badge/Design%20Patterns-9%20Implemented-success?style=flat-square)](./docs/)
[![colorama](https://img.shields.io/badge/Dependency-colorama-informational?style=flat-square)](https://pypi.org/project/colorama/)
[![License](https://img.shields.io/badge/License-Academic-orange?style=flat-square)]()

*Governing the kiosks of Zephyrus — one design pattern at a time.*

</div>

---

## Overview

**Aura Retail OS** is a modular, high-reliability software platform that governs autonomous retail kiosks deployed across the smart city of **Zephyrus**. Built entirely on OOP design principles, it demonstrates how complex real-world hardware-software challenges — from payment failures to emergency city-wide lockdowns — can be elegantly solved through thoughtful architectural design.

The system treats every hardware component as a **decoupled, swappable entity**, enabling kiosks to be upgraded, reconfigured, or extended at runtime without system restarts or code changes. This is the "Path B: Modular Hardware Platform" approach in action.

---

## Architecture & Design Patterns

Nine industry-standard design patterns work in concert to form the Aura OS backbone. Each pattern was selected because it solves a specific, concrete problem in the system.

| Pattern | Applied To | Problem It Solves |
|:---|:---|:---|
| **Abstract Factory** | System Provisioning | Guarantees that each kiosk type (Pharmacy, Grocery, etc.) is initialized with a fully compatible hardware suite — no mismatched components at boot. |
| **Bridge** | Hardware HAL | Decouples kiosk logic from dispenser implementations, allowing Robotic Arm and Spiral dispensers to be swapped without touching business logic. |
| **Decorator** | Modular Upgrades | Dynamically wraps a base kiosk with additional hardware capabilities (Solar Panel, Refrigeration, Network Unit) at runtime. |
| **Composite** | Inventory Management | Lets the system treat individual products and bundled product groups through a unified interface, simplifying all inventory traversal. |
| **Proxy** | Operational Security | Intercepts all inventory access to enforce role-based permissions and emergency-mode restrictions before they reach the real inventory. |
| **Adapter** | Payment Integration | Provides a single, unified payment interface over three incompatible vendor APIs — UPI, Credit Card, and Wallet — with zero coupling. |
| **Command** | Transaction Management | Wraps every purchase as a reversible command object, enabling full atomic rollback of payment and inventory in a single undo operation. |
| **Facade** | Public API | Presents a clean `KioskInterface` to the simulation layer, hiding the complexity of all subsystems behind a minimal surface area. |
| **Singleton** | City Registry | Maintains a single, globally consistent city state object used to broadcast emergency mode across all active kiosk instances simultaneously. |

---

## Simulation Walkthrough

Run `python simulation.py` and follow these scenarios to observe all major system capabilities.

### Scenario 1 — System Boot via Abstract Factory

```
Menu → [1] Reset System → [1] Pharmacy Kiosk
```

The Abstract Factory initializes the Pharmacy Kiosk and automatically pairs it with a **Robotic Arm Dispenser** — the only dispenser type compatible with precise pharmaceutical dispensing. Incompatible hardware combinations are rejected at the factory level.

---

### Scenario 2 — Hardware Dependency Enforcement (Path B Core Logic)

```
Menu → [4] Purchase → MED-03 (Insulin)
```
> ❌ **DENIED** — No Cooling Module detected. Insulin requires refrigeration.

```
Menu → [2] Upgrade Hardware → [1] Refrigeration Module
Menu → [4] Purchase → MED-03 (Insulin)
```
> ✅ **SUCCESS** — The Decorator wraps the kiosk with a `RefrigeratedKiosk`, and the temperature pre-check now passes.

This scenario demonstrates the Decorator and Bridge patterns working together: the hardware wrapper adds new *capability*, while the underlying dispenser logic remains unchanged.

---

### Scenario 3 — Atomic Rollback via Command Pattern

```
Menu → [4] Purchase → MED-01 (Aspirin)   ← Note current stock level
Menu → [5] Undo Last Transaction
```

The Command pattern stores the complete state of the transaction — payment authorization, inventory delta, and timestamp — as a reversible command object. A single `undo()` call atomically restores both the payment and the stock count to their pre-purchase state, with no partial rollbacks.

---

### Scenario 4 — Emergency Mode & Graceful Degradation

```
Menu → [6] Toggle Emergency Mode
Menu → [2] Upgrade → [3] Network Unit     ← Observe: OFFLINE status
Menu → [4] Purchase → MED-01 with UPI
```

Two simultaneous restrictions activate:

| Restriction | Enforced By | Behaviour |
|:---|:---|:---|
| UPI / digital payments blocked | Proxy (Security Layer) | Transaction rejected at the access layer |
| Purchase quantity capped at 2 units | Proxy (Safety Layer) | Enforced before reaching inventory |

The Singleton ensures this emergency state propagates consistently to all kiosk instances across the city. The Network Unit going offline is surfaced by the Decorator wrapping state, not the core kiosk logic.

---

## Project Structure

```
aura-retail-os/
│
├── simulation.py          # Entry point — main simulation loop & CLI menu
│
├── patterns/
│   ├── factory.py         # Abstract Factory — kiosk + hardware provisioning
│   ├── bridge.py          # Hardware HAL — dispenser abstraction layer
│   ├── decorator.py       # Runtime hardware module attachments
│   ├── composite.py       # Inventory product tree (items + bundles)
│   ├── proxy.py           # Role-based access & emergency enforcement
│   ├── adapter.py         # Unified payment gateway (UPI, CC, Wallet)
│   ├── command.py         # Transaction commands + undo stack
│   ├── facade.py          # KioskInterface — simplified public API
│   └── singleton.py       # CityRegistry — global emergency state
│
└── docs/
    └── project_report.pdf # Full UML diagrams & technical specification
```

---

## Installation & Running

**Requirements:** Python 3.8+

```bash
# 1. Install the single dependency
pip install colorama

# 2. Launch the simulation
python simulation.py
```

No environment setup, virtual environments, or configuration files required.

---

## Development Team

| Member | ID | Responsibilities |
|:---|:---|:---|
| **Kalagi** | 202512037 | System architecture, Abstract Factory, Facade (`KioskInterface`) |
| **Digvijay** | 202512008 | Inventory Composite tree, Proxy security and emergency layers |
| **Aayushi** | 202512101 | Hardware HAL (Bridge pattern), Decorator module system |
| **Sakina** | 202512046 | Payment Adapters (UPI/CC/Wallet), Command-based transaction rollback |




<div align="center">

*IT620 Object Oriented Programming · Team Nova*

</div>