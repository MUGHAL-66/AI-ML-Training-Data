import customtkinter as ctk
from components.sidebar import Sidebar
from components.navbar import Navbar
from services.report_service import dashboard_stats,top_products
from utils.theme import COLORS,FONTS
from utils.helpers import money

class DashboardScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate,logout):
        super().__init__(parent,fg_color=COLORS["background"])
        Sidebar(self,user,navigate,logout).pack(side="left",fill="y")
        main=ctk.CTkFrame(self,fg_color="transparent"); main.pack(side="left",fill="both",expand=True)
        Navbar(main,"Dashboard",user).pack(fill="x")
        self.body=ctk.CTkScrollableFrame(main,fg_color="transparent"); self.body.pack(fill="both",expand=True,padx=20,pady=10)
        self.load()
    def load(self):
        for w in self.body.winfo_children(): w.destroy()
        s=dashboard_stats()
        cards=[("Today's Sales",money(s["sales"])),("Orders",s["orders"]),("Customers",s["customers"]),
               ("Low Stock",s["low_stock"]),("Expenses",money(s["expenses"])),("Profit",money(s["profit"]))]
        grid=ctk.CTkFrame(self.body,fg_color="transparent"); grid.pack(fill="x")
        for i,(a,b) in enumerate(cards):
            c=ctk.CTkFrame(grid,fg_color=COLORS["card"],corner_radius=16); c.grid(row=i//3,column=i%3,sticky="nsew",padx=6,pady=6)
            ctk.CTkLabel(c,text=a,text_color=COLORS["text_secondary"],font=FONTS["small"]).pack(anchor="w",padx=18,pady=(18,4))
            ctk.CTkLabel(c,text=str(b),font=FONTS["stat"],text_color=COLORS["gold"]).pack(anchor="w",padx=18,pady=(0,18))
        for i in range(3): grid.grid_columnconfigure(i,weight=1)
        c=ctk.CTkFrame(self.body,fg_color=COLORS["card"],corner_radius=16); c.pack(fill="x",pady=15)
        ctk.CTkLabel(c,text="Top Selling Products",font=FONTS["heading"]).pack(anchor="w",padx=20,pady=15)
        for r in top_products():
            ctk.CTkLabel(c,text=f"{r['product_name']}   •   {r['qty']} sold   •   {money(r['revenue'])}",
                         font=FONTS["body"]).pack(anchor="w",padx=25,pady=5)
