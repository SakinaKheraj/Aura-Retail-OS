"""
================================================================
  Aura Retail OS — Interactive CLI
  Group 28 | Path B: Modular Hardware Platform
================================================================
"""

import os
import time
import sys
from core.central_registry import CentralRegistry
from core.kiosk_factory import KioskFactory
from core.kiosk import KioskInterface
from inventory.product import Product, ProductBundle
from payment.adapters import UPIAdapter, CreditCardAdapter, WalletAdapter
from hardware.modules import RefrigerationModule, KioskWithModule

# Ensure UTF-8 for better symbols on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

# --- ANSI Colors ---
class Style:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    BLUE = '\033[94m'
    GRAY = '\033[90m'

# --- UI Helpers ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    print(f"\n{Style.BOLD}{Style.CYAN}{'='*70}{Style.RESET}")
    print(f" {Style.BOLD}{text.upper()}{Style.RESET}")
    print(f"{Style.BOLD}{Style.CYAN}{'='*70}{Style.RESET}")

def print_info(text):
    print(f" {Style.BLUE}[i] {text}{Style.RESET}")

def print_success(text):
    print(f" {Style.GREEN}[✓] {text}{Style.RESET}")

def print_error(text):
    print(f" {Style.RED}[!] {text}{Style.RESET}")

def aura_banner():
    banner = f"""{Style.BOLD}{Style.CYAN}
    ┌────────────────────────────────────────────────────────────┐
    │                {Style.YELLOW}A U R A   R E T A I L   O S{Style.CYAN}                 │
    │          {Style.RESET}{Style.GRAY}Smart-City Autonomous Infrastructure{Style.BOLD}{Style.CYAN}              │
    │                 {Style.RESET}ZEPHYRUS CITY COUNCIL{Style.BOLD}{Style.CYAN}                      │
    └────────────────────────────────────────────────────────────┘{Style.RESET}
    """
    print(banner)

# ================================================================
# CLI APPLICATION CLASS
# ================================================================

class AuraApp:
    def __init__(self):
        self.registry = CentralRegistry()
        self.kiosk = None
        self.facade = None
        self.is_running = True
        
        # Setup initial state
        self.registry.set("city", "Zephyrus")
        self.registry.set("version", "2.0-interactive")

    def bootstrap_inventory(self):
        """Prepare some initial products for the demo."""
        if not self.kiosk: return
        
        mgr = self.kiosk.inventory_manager._manager
        
        # Products
        med1 = Product("MED-01", "Aspirin 100mg", price=50.0, quantity=100)
        med2 = Product("MED-02", "Gauze Bandage", price=120.0, quantity=50)
        med3 = Product("MED-03", "Insulin Vial", price=2500.0, quantity=10)
        
        # Bundle (Composite)
        bundle = ProductBundle("BND-01", "Emergency Relief Kit")
        bundle.add(med1)
        bundle.add(med2)
        bundle.add(med3)
        
        mgr.add_product(med1)
        mgr.add_product(med2)
        mgr.add_product(med3)
        mgr.add_product(bundle)

    def select_kiosk(self):
        print_header("Kiosk Provisioning")
        print(f" 1. {Style.YELLOW}Pharmacy Kiosk{Style.RESET}  (Hospitals)")
        print(f" 2. {Style.YELLOW}Food Kiosk{Style.RESET}      (Metro/Uni)")
        print(f" 3. {Style.YELLOW}Emergency Kiosk{Style.RESET} (Disaster Zones)")
        
        choice = input(f"\n {Style.BOLD}Select Type [1-3]: {Style.RESET}")
        
        k_types = {"1": "pharmacy", "2": "food", "3": "emergency"}
        k_type = k_types.get(choice, "food")
        
        # Payment setup (default)
        adapter = UPIAdapter(upi_id="aura@icici")
        
        self.kiosk = KioskFactory.create_kiosk(
            kiosk_type=k_type,
            kiosk_id="K-1001",
            location="Downtown Zephyrus",
            payment_gateway=adapter
        )
        self.facade = KioskInterface(self.kiosk)
        self.bootstrap_inventory()
        print_success(f"{k_type.capitalize()} Kiosk initialized.")

    def add_module(self):
        if not self.kiosk:
            print_error("No kiosk detected. Please initialize first.")
            return
        
        print_header("Modular Hardware Upgrades")
        print(f" 1. {Style.YELLOW}Refrigeration Module{Style.RESET} (2.0°C)")
        print(f" 2. {Style.YELLOW}Solar Monitoring{Style.RESET}")
        print(f" 3. {Style.YELLOW}Network Unit{Style.RESET}")
        
        choice = input(f"\n {Style.BOLD}Select Module [1-3]: {Style.RESET}")
        
        if choice == "1":
            self.kiosk = KioskWithModule(self.kiosk, RefrigerationModule(temperature_celsius=2.0))
            self.facade = KioskInterface(self.kiosk) # Re-wrap if needed
            print_success("Refrigeration module attached via Decorator Pattern.")
        else:
            print_info("Module skeleton attached.")

    def show_inventory(self):
        if not self.kiosk: return
        print_header("Current Inventory (Composite Tree)")
        mgr = self.kiosk.inventory_manager._manager
        mgr.list_all()
        print(f"\n {Style.GRAY}Note: Bundles compute price & stock recursively.{Style.RESET}")

    def run_purchase(self):
        if not self.facade: return
        
        print_header("Secure Transaction")
        pid = input(f" {Style.BOLD}Enter Product ID (e.g., MED-01): {Style.RESET}").upper()
        
        try:
            qty = int(input(f" {Style.BOLD}Enter Quantity: {Style.RESET}"))
        except ValueError:
            print_error("Invalid quantity.")
            return

        print(f"\n {Style.BOLD}Select Payment Method:{Style.RESET}")
        print(" 1. UPI (Default)")
        print(" 2. Credit Card")
        print(" 3. Digital Wallet")
        p_choice = input(f" Choice [1-3]: ")
        
        if p_choice == "2":
            self.kiosk.payment_gateway = CreditCardAdapter("4111-XXXX-XXXX-1111")
            print_info("Payment Adapter swapped to Credit Card.")
        elif p_choice == "3":
            self.kiosk.payment_gateway = WalletAdapter("aura_user_88")
            print_info("Payment Adapter swapped to Digital Wallet.")
            
        print(f"{Style.GRAY}{'-'*40}{Style.RESET}")
        self.facade.purchase_item(pid, qty, "USER_Interactive")

    def main_loop(self):
        clear()
        aura_banner()
        
        while self.is_running:
            print(f"\n{Style.BOLD}--- MAIN MENU ---{Style.RESET}")
            print(f" [{Style.CYAN}1{Style.RESET}] Initialize/Reset Kiosk")
            print(f" [{Style.CYAN}2{Style.RESET}] Upgrade Hardware Modules")
            print(f" [{Style.CYAN}3{Style.RESET}] View Inventory Tree")
            print(f" [{Style.CYAN}4{Style.RESET}] Purchase Item")
            print(f" [{Style.CYAN}5{Style.RESET}] System Diagnostics")
            print(f" [{Style.CYAN}0{Style.RESET}] Shutdown System")
            
            choice = input(f"\n {Style.BOLD}Choice > {Style.RESET}")
            
            if choice == "1": self.select_kiosk()
            elif choice == "2": self.add_module()
            elif choice == "3": self.show_inventory()
            elif choice == "4": self.run_purchase()
            elif choice == "5": 
                if self.facade: self.facade.run_diagnostics()
                else: print_error("Initialize kiosk first.")
            elif choice == "0":
                print_info("Saving system state...")
                if self.kiosk: self.kiosk.inventory_manager._manager.save_to_json()
                print_success("Aura OS Shutdown complete.")
                self.is_running = False
            else:
                print_error("Invalid selection.")

# ================================================================
if __name__ == "__main__":
    app = AuraApp()
    try:
        app.main_loop()
    except KeyboardInterrupt:
        print("\n\n [!] Force shutdown detected.")
        sys.exit(0)
