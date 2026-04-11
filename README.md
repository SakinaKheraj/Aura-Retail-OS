# Aura Retail OS
**Group 28 | Path B: Modular Hardware Platform**
Course: IT620 — Object Oriented Programming

---

## How to Run

```bash
# From the project root (aura_retail_os/)
python simulation.py
```

No external libraries needed. Python 3.10+ recommended.

---

## Folder Structure

```
aura_retail_os/
├── core/
│   ├── central_registry.py    # Singleton pattern (skeleton)
│   ├── kiosk.py               # Abstract Kiosk + subclasses + KioskInterface Facade (skeleton)
│   └── kiosk_factory.py       # Abstract Factory pattern (skeleton)
├── inventory/
│   ├── product.py             # Composite pattern + Proxy pattern (COMPLETE)
│   └── inventory_manager.py   # Inventory store (COMPLETE)
├── payment/
│   ├── payment_processor.py   # PaymentGateway interface + Adaptees (COMPLETE)
│   └── adapters.py            # Adapter pattern — 3 adapters (COMPLETE)
├── hardware/
│   ├── dispenser.py           # Bridge pattern (skeleton)
│   └── modules.py             # Decorator pattern (skeleton)
├── commands/
│   └── commands.py            # Command pattern (skeleton)
├── persistence/
│   └── persistence_manager.py # JSON + CSV persistence (skeleton)
├── simulation.py              # Main simulation demo
└── README.md
```

---

## Design Patterns

### Subtask 2 — Fully Implemented

| Pattern | File | Member | Purpose |
|---|---|---|---|
| **Composite** | `inventory/product.py` | Digvijay | Nested product bundles with recursive price |
| **Adapter** | `payment/adapters.py` | Sakina | 3 payment providers via one interface |

### Subtask 2 — Skeletons (Final Submission)

| Pattern | File | Member |
|---|---|---|
| Singleton | `core/central_registry.py` | Kalagi |
| Abstract Factory | `core/kiosk_factory.py` | Kalagi |
| Facade | `core/kiosk.py` | Kalagi |
| Command | `commands/commands.py` | Kalagi |
| Proxy | `inventory/product.py` | Digvijay |
| Bridge | `hardware/dispenser.py` | Aayushi |
| Decorator | `hardware/modules.py` | Aayushi |

---

## Work Distribution

| Member | ID | Files |
|---|---|---|
| Kalagi | 202512037 | `core/`, `commands/`, `persistence/`, `simulation.py` |
| Digvijay | 202512008 | `inventory/` |
| Sakina | 202512046 | `payment/` |
| Aayushi | 202512101 | `hardware/` |