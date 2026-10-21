import customtkinter as ctk
from services.order_service import get_all_orders,update_order_status
from utils.theme import COLORS,FONTS
from utils.constants import ORDER_PENDING,ORDER_PREPARING,ORDER_READY

class KitchenScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate):
        super().__init__(parent,fg_color=COLORS["background"]); self.navigate=navigate; self.build(); self.load()
    def build(self):
        h=ctk.CTkFrame(self,fg_color="transparent"); h.pack(fill="x",padx=25,pady=25)
        ctk.CTkLabel(h,text="Kitchen Display",font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(h,text="↻ Refresh",command=self.load).pack(side="right",padx=5)
        ctk.CTkButton(h,text="← Dashboard",command=lambda:self.navigate("dashboard")).pack(side="right")
        self.grid=ctk.CTkScrollableFrame(self,fg_color="transparent"); self.grid.pack(fill="both",expand=True,padx=25,pady=10)
    def load(self):
        for w in self.grid.winfo_children(): w.destroy()
        active=[o for o in get_all_orders() if o["status"] in [ORDER_PENDING,ORDER_PREPARING,ORDER_READY]]
        if not active:
            ctk.CTkLabel(self.grid,text="No active kitchen orders.",font=FONTS["heading"],text_color=COLORS["muted"]).pack(pady=100); return
        for i,o in enumerate(active):
            c=ctk.CTkFrame(self.grid,fg_color=COLORS["card"],corner_radius=16); c.grid(row=i//3,column=i%3,sticky="nsew",padx=7,pady=7)
            ctk.CTkLabel(c,text=o["order_number"],font=FONTS["subheading"],text_color=COLORS["gold"]).pack(pady=(18,5))
            ctk.CTkLabel(c,text=o["status"],font=FONTS["heading"]).pack(pady=5)
            from services.order_service import get_order_items
            for item in get_order_items(o["id"]):
                ctk.CTkLabel(c,text=f"{item['product_name']} • {item['size_name']} × {item['quantity']}").pack(anchor="w",padx=20,pady=3)
            next_status={ORDER_PENDING:ORDER_PREPARING,ORDER_PREPARING:ORDER_READY,ORDER_READY:"Completed"}[o["status"]]
            label={ORDER_PENDING:"START PREPARING",ORDER_PREPARING:"MARK READY",ORDER_READY:"COMPLETE ORDER"}[o["status"]]
            ctk.CTkButton(c,text=label,height=42,command=lambda oid=o["id"],s=next_status:self.advance(oid,s)).pack(fill="x",padx=18,pady=18)
    def advance(self,oid,status): update_order_status(oid,status); self.load()
