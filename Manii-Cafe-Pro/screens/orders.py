import customtkinter as ctk
from services.order_service import get_all_orders,get_order_items,update_order_status,cancel_order
from components.receipt import create_pdf_receipt
from utils.theme import COLORS,FONTS
from utils.constants import ORDER_PENDING,ORDER_PREPARING,ORDER_READY,ORDER_COMPLETED,ORDER_CANCELLED
from utils.helpers import money

class OrdersScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate):
        super().__init__(parent,fg_color=COLORS["background"]); self.navigate=navigate; self.build(); self.load()
    def build(self):
        h=ctk.CTkFrame(self,fg_color="transparent"); h.pack(fill="x",padx=25,pady=25)
        ctk.CTkLabel(h,text="Orders",font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(h,text="← Dashboard",command=lambda:self.navigate("dashboard")).pack(side="right")
        self.search=ctk.CTkEntry(self,placeholder_text="Search order number...",height=40); self.search.pack(fill="x",padx=25); self.search.bind("<KeyRelease>",lambda e:self.load())
        self.scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); self.scroll.pack(fill="both",expand=True,padx=25,pady=10)
    def load(self):
        for w in self.scroll.winfo_children(): w.destroy()
        q=self.search.get().lower().strip()
        for o in get_all_orders():
            if q and q not in o["order_number"].lower(): continue
            c=ctk.CTkFrame(self.scroll,fg_color=COLORS["card"],corner_radius=14); c.pack(fill="x",pady=5)
            info=ctk.CTkFrame(c,fg_color="transparent"); info.pack(side="left",padx=18,pady=12)
            ctk.CTkLabel(info,text=o["order_number"],font=FONTS["subheading"],text_color=COLORS["gold"]).pack(anchor="w")
            ctk.CTkLabel(info,text=f"{o['customer_name'] or 'Walk-in'} • {o['order_type']} • {o['payment_method']}",text_color=COLORS["text_secondary"]).pack(anchor="w")
            ctk.CTkLabel(info,text=str(o["created_at"]),text_color=COLORS["muted"]).pack(anchor="w")
            ctk.CTkButton(c,text=money(o["total"]),width=115,command=lambda x=o:self.details(x)).pack(side="right",padx=5)
            status=ctk.CTkOptionMenu(c,values=[ORDER_PENDING,ORDER_PREPARING,ORDER_READY,ORDER_COMPLETED,ORDER_CANCELLED],
                                     command=lambda v,i=o["id"]:self.status(i,v)); status.set(o["status"]); status.pack(side="right",padx=5)
    def status(self,i,v): update_order_status(i,v); self.load()
    def details(self,o):
        d=ctk.CTkToplevel(self); d.title(o["order_number"]); d.geometry("520x600"); d.grab_set()
        ctk.CTkLabel(d,text=o["order_number"],font=FONTS["heading"],text_color=COLORS["gold"]).pack(pady=20)
        for x in get_order_items(o["id"]):
            ctk.CTkLabel(d,text=f"{x['product_name']} • {x['size_name']} × {x['quantity']} = {money(x['total_price'])}").pack(anchor="w",padx=35,pady=5)
        ctk.CTkLabel(d,text=f"\nSubtotal: {money(o['subtotal'])}\nDiscount: {money(o['discount'])}\nTax: {money(o['tax'])}\nTOTAL: {money(o['total'])}",justify="left",font=FONTS["body"]).pack(anchor="w",padx=35,pady=20)
        ctk.CTkButton(d,text="🧾 PDF Receipt",command=lambda:self.receipt(o["id"])).pack(fill="x",padx=35,pady=5)
    def receipt(self,i):
        p=create_pdf_receipt(i)
        d=ctk.CTkToplevel(self); d.title("Receipt"); d.geometry("450x180")
        ctk.CTkLabel(d,text=f"PDF receipt created:\n{p}",wraplength=380).pack(pady=30)
        ctk.CTkButton(d,text="OK",command=d.destroy).pack()
