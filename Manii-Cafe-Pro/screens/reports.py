import customtkinter as ctk
from services.report_service import dashboard_stats,top_products,payment_summary
from utils.theme import COLORS,FONTS
from utils.helpers import money

class ReportsScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate):
        super().__init__(parent,fg_color=COLORS["background"]); self.navigate=navigate; self.build()
    def build(self):
        h=ctk.CTkFrame(self,fg_color="transparent"); h.pack(fill="x",padx=25,pady=25)
        ctk.CTkLabel(h,text="Reports",font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(h,text="↻ Refresh",command=self.build).pack(side="right",padx=5)
        ctk.CTkButton(h,text="← Dashboard",command=lambda:self.navigate("dashboard")).pack(side="right")
        body=ctk.CTkScrollableFrame(self,fg_color="transparent"); body.pack(fill="both",expand=True,padx=25)
        s=dashboard_stats()
        for title,value in [("Today Sales",money(s["sales"])),("Today Expenses",money(s["expenses"])),("Net Profit",money(s["profit"])),("Orders",s["orders"])]:
            c=ctk.CTkFrame(body,fg_color=COLORS["card"],corner_radius=14); c.pack(fill="x",pady=5)
            ctk.CTkLabel(c,text=title,font=FONTS["subheading"]).pack(side="left",padx=20,pady=15)
            ctk.CTkLabel(c,text=str(value),font=FONTS["heading"],text_color=COLORS["gold"]).pack(side="right",padx=20)
        c=ctk.CTkFrame(body,fg_color=COLORS["card"],corner_radius=14); c.pack(fill="x",pady=15)
        ctk.CTkLabel(c,text="Top Products",font=FONTS["heading"]).pack(anchor="w",padx=20,pady=15)
        for r in top_products(10):
            ctk.CTkLabel(c,text=f"{r['product_name']} — {r['qty']} sold — {money(r['revenue'])}").pack(anchor="w",padx=25,pady=4)
        c=ctk.CTkFrame(body,fg_color=COLORS["card"],corner_radius=14); c.pack(fill="x",pady=15)
        ctk.CTkLabel(c,text="Payment Summary",font=FONTS["heading"]).pack(anchor="w",padx=20,pady=15)
        for r in payment_summary():
            ctk.CTkLabel(c,text=f"{r['payment_method']} — {r['orders']} orders — {money(r['total'])}").pack(anchor="w",padx=25,pady=4)
