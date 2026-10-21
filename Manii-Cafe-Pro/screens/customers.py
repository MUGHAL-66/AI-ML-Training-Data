import customtkinter as ctk
from services.customer_service import get_all_customers,add_customer,update_customer,delete_customer
from utils.theme import COLORS,FONTS
from utils.helpers import money

class CustomersScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate):
        super().__init__(parent,fg_color=COLORS["background"]); self.navigate=navigate; self.build(); self.load()
    def build(self):
        h=ctk.CTkFrame(self,fg_color="transparent"); h.pack(fill="x",padx=25,pady=25)
        ctk.CTkLabel(h,text="Customers",font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(h,text="+ Add Customer",command=lambda:self.form()).pack(side="right",padx=5)
        ctk.CTkButton(h,text="← Dashboard",command=lambda:self.navigate("dashboard")).pack(side="right")
        self.scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); self.scroll.pack(fill="both",expand=True,padx=25,pady=10)
    def load(self):
        for w in self.scroll.winfo_children(): w.destroy()
        for cst in get_all_customers():
            c=ctk.CTkFrame(self.scroll,fg_color=COLORS["card"],corner_radius=14); c.pack(fill="x",pady=5)
            info=ctk.CTkFrame(c,fg_color="transparent"); info.pack(side="left",padx=18,pady=12)
            ctk.CTkLabel(info,text=cst["name"],font=FONTS["subheading"]).pack(anchor="w")
            ctk.CTkLabel(info,text=f"{cst['phone'] or '-'} • {cst['email'] or '-'}",text_color=COLORS["text_secondary"]).pack(anchor="w")
            ctk.CTkLabel(info,text=f"Orders: {cst['total_orders']} • Spent: {money(cst['total_spent'])} • Points: {cst['loyalty_points']}",text_color=COLORS["gold"]).pack(anchor="w")
            ctk.CTkButton(c,text="Edit",width=70,command=lambda x=cst:self.form(x)).pack(side="right",padx=4)
            ctk.CTkButton(c,text="Delete",width=75,fg_color=COLORS["danger"],command=lambda i=cst["id"]:self.remove(i)).pack(side="right",padx=4)
    def form(self,c=None):
        d=ctk.CTkToplevel(self); d.title("Customer"); d.geometry("480x430"); d.grab_set(); ent={}
        for lab,key in [("Name","name"),("Phone","phone"),("Email","email")]:
            ctk.CTkLabel(d,text=lab).pack(anchor="w",padx=35,pady=(15,3)); e=ctk.CTkEntry(d,height=40); e.pack(fill="x",padx=35); ent[key]=e
            if c: e.insert(0,str(c[key] or ""))
        def save():
            ok,msg=(update_customer(c["id"],ent["name"].get(),ent["phone"].get(),ent["email"].get()) if c else add_customer(ent["name"].get(),ent["phone"].get(),ent["email"].get()))
            if ok: d.destroy(); self.load()
        ctk.CTkButton(d,text="Save Customer",height=45,command=save).pack(fill="x",padx=35,pady=25)
    def remove(self,i): delete_customer(i); self.load()
