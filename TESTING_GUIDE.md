# Testing & Validation Guide — Aura Retail OS

**IT620 Object Oriented Programming · Path B · Project v2.0**

Run `python simulation.py` and follow each scenario in order. Each scenario targets a specific pattern and has a clear pass/fail condition.

---

## Scenario A — Hardware Consistency (Abstract Factory)

**Goal:** Confirm that each kiosk type is automatically paired with the correct dispenser at boot.

**Steps:**
1. Select `[1] Reset` → `[1] Pharmacy Kiosk`

**Expected output:**
```
[KioskFactory] Created pharmacy kiosk 'K-1001' with RoboticArmDispenser
```

**Pass condition:** The log shows `RoboticArmDispenser` — not a Spiral or Conveyor. The factory selected a high-precision dispenser automatically based on kiosk type.

**Pattern verified:** Abstract Factory

---

## Scenario B — Hardware Dependency Enforcement (Bridge + Decorator)

**Goal:** Confirm that a product requiring specific hardware is blocked until that hardware is attached.

**Steps:**
1. Select `[4] Purchase` → `MED-03 (Insulin)`
2. Observe the denial.
3. Select `[2] Upgrade` → `[1] Refrigeration`
4. Select `[4] Purchase` → `MED-03 (Insulin)` again

**Expected output (step 2):**
```
[SAFETY] DENIED — Insulin Vial requires refrigeration, but NO COOLING MODULE is attached.
```

**Expected output (step 4):**
```
[SAFETY] Temperature Check: OK
```

**Pass condition:** Purchase is blocked before the upgrade and succeeds after. The base kiosk class is unchanged — only its decorator wrapper changes.

**Pattern verified:** Decorator (runtime capability extension), Bridge (kiosk logic isolated from dispenser type)

---

## Scenario C — Atomic Rollback (Command Pattern)

**Goal:** Confirm that undoing a transaction fully restores both payment and inventory with no partial state.

**Steps:**
1. Select `[4] Purchase` → `MED-01 (Aspirin)` — note the stock count (e.g. 100 → 99)
2. Select `[5] Undo Last Transaction`
3. Select `[3] View Inventory` — check the stock count

**Expected output (step 2):**
```
[CommandInvoker] Rolling back...
[CreditCardAdapter] Refunding ₹50.00...
[Inventory] Stock restored: MED-01 → 100
```

**Pass condition:** Stock returns to its original value. Payment is refunded. No orphaned state remains.

**Pattern verified:** Command

---

## Scenario D — Network Failure & Payment Fallback (Adapter)

**Goal:** Confirm that individual payment adapters respond correctly to network status, and that a fallback adapter works independently.

**Steps:**
1. Select `[2] Upgrade` → `[3] Network Unit` — note it initializes as OFFLINE
2. Select `[4] Purchase` → payment method `[1] UPI`
3. Observe the block.
4. Retry with payment method `[2] Credit Card`

**Expected output (step 2):**
```
[SECURITY] OFFLINE — UPI payment unavailable. Please use physical card or cash.
```

**Expected output (step 4):** Purchase completes successfully.

**Pass condition:** UPI is blocked; Credit Card succeeds. Each adapter independently checks system state — the gateway interface is identical for both.

**Pattern verified:** Adapter

---

## Scenario E — Emergency Mode Restrictions (Singleton + Proxy)

**Goal:** Confirm that toggling emergency mode applies city-wide purchase limits consistently.

**Steps:**
1. Select `[6] Toggle Emergency Mode`
2. Select `[4] Purchase` → `MED-01 (Aspirin)` → enter quantity `5`

**Expected output:**
```
[EMERGENCY LIMIT] Maximum 2 units per transaction during emergency mode.
```

**Pass condition:** Quantity is capped at 2 regardless of input. The limit is enforced by the Proxy before the request reaches inventory. The Singleton ensures this state is consistent across all kiosk instances.

**Pattern verified:** Singleton (city-wide state broadcast), Proxy (restriction enforcement)

---

## Scenario F — System Diagnostics (Facade)

**Goal:** Confirm that a single API call triggers a full multi-subsystem health check.

**Steps:**
1. Select `[7] Diagnostics`

**Expected output:**
```
[Diagnostics] Dispenser:  OK
[Diagnostics] Inventory:  OK
[Diagnostics] Payment:    OK
```

**Pass condition:** All three subsystems are reported in one call. No internal subsystem logic is exposed to the caller.

**Pattern verified:** Facade

---

## Quick Reference

| Scenario | Pattern(s) Tested | Pass Condition |
|:---|:---|:---|
| A | Abstract Factory | Correct dispenser auto-selected at boot |
| B | Bridge, Decorator | Purchase blocked without module; passes after attachment |
| C | Command | Full rollback restores both payment and stock |
| D | Adapter | UPI blocked offline; Credit Card succeeds independently |
| E | Singleton, Proxy | Quantity capped at 2 under emergency mode |
| F | Facade | Single call returns health status of all subsystems |