<div align="center">

### Autonomous Smart-City Retail Infrastructure

**IT620 — Object Oriented Programming · Path B: Modular Hardware Platform**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![OOP Patterns](https://img.shields.io/badge/Design%20Patterns-9%20Implemented-success?style=flat-square)](./docs/)
[![colorama](https://img.shields.io/badge/Dependency-colorama-informational?style=flat-square)](https://pypi.org/project/colorama/)

*Governing the kiosks of Zephyrus — one design pattern at a time.*

</div>

---

## 📺 Project Demonstration

https://github.com/user-attachments/assets/20d9cad9-31eb-46bb-9df0-8e51211b7e01

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
| **Strategy** | Dynamic Pricing | Allows the system to switch between Standard and Emergency pricing strategies at runtime based on the city's operational status. |
| **Facade** | Public API | Presents a clean `KioskInterface` to the simulation layer, hiding the complexity of all subsystems behind a minimal surface area. |
| **Singleton** | City Registry | Maintains a single, globally consistent city state object used to broadcast emergency mode across all active kiosk instances simultaneously. |


---

## Simulation Walkthrough

Run `python simulation.py` and follow these scenarios to observe all major system capabilities.

### Scenario 1 — System Boot via Abstract Factory
```
Menu → [1] Reset System → [1] Pharmacy Kiosk
```
The Abstract Factory initializes the Pharmacy Kiosk and automatically pairs it with a **Robotic Arm Dispenser**.

### Scenario 2 — Hardware Dependency (Path B Core)
```
Menu → [4] Purchase → MED-03 (Insulin)
```
❌ **DENIED** — Insulin requires refrigeration, but NO COOLING MODULE is attached.

### Scenario 3 — Atomic Rollback
```
Menu → [4] Purchase → MED-01 (Aspirin)
Menu → [5] Undo Last Transaction
```
✅ **SUCCESS** — Stock and payment are atomically restored via the Command pattern.

### Scenario 4 — Emergency Mode
```
Menu → [6] Toggle Emergency Mode
Menu → [4] Purchase → MED-01 (Quantity: 5)
```
⚠️ **CAPPED** — Quantity is restricted to 2 units for essential items during emergencies.

---

## Project Structure

```
Aura-Retail-OS/
├── simulation.py          # Entry point — main simulation loop & CLI menu
├── core/
│   ├── central_registry.py# Singleton — global city state
│   ├── kiosk.py           # Facade & Kiosk base classes
│   ├── kiosk_factory.py   # Abstract Factory implementation
│   ├── commands.py        # Command pattern — purchase/undo logic
│   └── pricing.py         # Strategy pattern — pricing models
├── hardware/
│   ├── dispenser.py       # Bridge — hardware motors
│   └── modules.py         # Decorator — optional modules
├── inventory/
│   ├── product.py         # Composite & Proxy implementation
│   └── inventory_manager.py# Core inventory store
├── payment/
│   ├── adapters.py        # Payment Adapters (UPI, CC, Wallet)
│   └── payment_processor.py# Incompatible legacy SDK targets
├── persistence/
│   ├── inventory.json     # Saved stock state
│   ├── config.json        # Saved system configuration
│   └── transactions.csv   # Audit trail of all commands
└── TESTING_GUIDE.md       # Step-by-step validation guide
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
