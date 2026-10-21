import customtkinter as ctk
from database.schema import create_tables
from database.seed import seed_database
from screens.login import LoginScreen
from screens.dashboard import DashboardScreen
from screens.pos import POSScreen
from screens.orders import OrdersScreen
from screens.products import ProductsScreen
from screens.inventory import InventoryScreen
from screens.customers import CustomersScreen
from screens.employees import EmployeesScreen
from screens.expenses import ExpensesScreen
from screens.reports import ReportsScreen
from screens.kitchen import KitchenScreen
from screens.settings import SettingsScreen
from utils.theme import setup_theme, COLORS
from utils.constants import APP_NAME

class CafeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1360x850")
        self.minsize(1150, 720)
        self.configure(fg_color=COLORS["background"])
        self.current_user = None
        self.show_login()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()
        LoginScreen(self, self.login_success).pack(fill="both", expand=True)

    def login_success(self, user):
        self.current_user = user
        self.show_dashboard()

    def show_page(self, screen_class):
        self.clear()
        screen_class(self, self.current_user, self.navigate).pack(fill="both", expand=True)

    def navigate(self, page):
        pages = {
            "dashboard": self.show_dashboard,
            "pos": lambda: self.show_page(POSScreen),
            "orders": lambda: self.show_page(OrdersScreen),
            "products": lambda: self.show_page(ProductsScreen),
            "inventory": lambda: self.show_page(InventoryScreen),
            "customers": lambda: self.show_page(CustomersScreen),
            "employees": lambda: self.show_page(EmployeesScreen),
            "expenses": lambda: self.show_page(ExpensesScreen),
            "reports": lambda: self.show_page(ReportsScreen),
            "kitchen": lambda: self.show_page(KitchenScreen),
            "settings": lambda: self.show_page(SettingsScreen),
        }
        if page in pages:
            pages[page]()

    def show_dashboard(self):
        self.clear()
        DashboardScreen(
            self, self.current_user, self.navigate, self.logout
        ).pack(fill="both", expand=True)

    def logout(self):
        self.current_user = None
        self.show_login()

def initialize():
    create_tables()
    seed_database()

if __name__ == "__main__":
    setup_theme()
    initialize()
    CafeApp().mainloop()
