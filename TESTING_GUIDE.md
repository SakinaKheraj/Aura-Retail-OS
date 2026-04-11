# Testing Guide — Aura Retail OS

Follow these steps to test all design patterns in the interactive CLI.

### 1. Initialize the System
- **Command**: Choose `1` (Initialize/Reset Kiosk).
- **Sub-command**: Choose `1` (Pharmacy Kiosk).
- **Pattern**: **Factory Pattern** creates the specific kiosk and injecting sub-systems.

### 2. Upgrade Hardware
- **Command**: Choose `2` (Upgrade Hardware Modules).
- **Sub-command**: Choose `1` (Refrigeration Module).
- **Pattern**: **Decorator Pattern** wraps the existing kiosk object at runtime to add cooling capabilities.

### 3. Verify Composite Inventory
- **Command**: Choose `3` (View Inventory Tree).
- **Observation**: Look for `BND-01` (Emergency Relief Kit). Note how its total price (₹2670.00) is automatically calculated from its children (Aspirin, Bandage, Insulin).
- **Pattern**: **Composite Pattern** allows treating bundles and products through the same `get_price()` interface.

### 4. Test Adapter Pattern (Unified Payment)
- **Command**: Choose `4` (Purchase Item).
- **ID**: `MED-01`.
- **Quantity**: `2`.
- **Payment**: Choose `2` (Credit Card).
- **Observation**: The system successfully uses a different API call (CreditCardAPI) without changing the `purchase_item` logic.
- **Pattern**: **Adapter Pattern** translates the unified interface to heterogeneous payment providers.

### 5. Check System Constraints
- **Command**: Choose `4` (Purchase Item).
- **ID**: `MED-03` (Insulin).
- **Quantity**: `99` (Exceeds stock of 10).
- **Observation**: The system denies the request, demonstrating **Derived Attribute** calculation (Available Stock).

### 6. Diagnostics & Shutdown
- **Command**: Choose `5` to run diagnostics (**Facade Pattern** simplifies complexity).
- **Command**: Choose `0` to shutdown (**Persistence Manager** saves state to `inventory.json`).
