import customtkinter as ctk
from services.inventory_service import get_all_inventory,add_inventory,update_inventory,delete_inventory
from utils.theme import COLORS,FONTS
from utils.helpers import money

class InventoryScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate):
        super().__init__(parent,fg_color=COLORS["background"]); self.navigate=navigate; self.build(); self.load()
    def build(self):
        h=ctk.CTkFrame(self,fg_color="transparent"); h.pack(fill="x",padx=25,pady=25)
        ctk.CTkLabel(h,text="Inventory",font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(h,text="+ Add Stock Item",command=self.add).pack(side="right",padx=5)
        ctk.CTkButton(h,text="← Dashboard",command=lambda:self.navigate("dashboard")).pack(side="right")
        self.scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); self.scroll.pack(fill="both",expand=True,padx=25,pady=10)
    def load(self):
        for w in self.scroll.winfo_children(): w.destroy()
        for i in get_all_inventory():
            low=i["quantity"]<=i["minimum_stock"]
            c=ctk.CTkFrame(self.scroll,fg_color=COLORS["card"],corner_radius=14,border_width=1,border_color=COLORS["danger"] if low else COLORS["border"]); c.pack(fill="x",pady=5)
            ctk.CTkLabel(c,text=i["item_name"],font=FONTS["subheading"]).pack(side="left",padx=18,pady=15)
            ctk.CTkLabel(c,text=f"{i['quantity']:.2f} {i['unit']} • Min {i['minimum_stock']:.2f} • Cost {money(i['cost_per_unit'])}",text_color=COLORS["danger"] if low else COLORS["text_secondary"]).pack(side="left")
            ctk.CTkButton(c,text="Edit",width=70,command=lambda x=i:self.edit(x)).pack(side="right",padx=10)
    def add(self):
        d=ctk.CTkToplevel(self); d.title("Add Inventory"); d.geometry("480x500"); d.grab_set(); ent={}
        for lab,key in [("Item Name","name"),("Quantity","quantity"),("Unit","unit"),("Minimum Stock","minimum"),("Cost Per Unit","cost")]:
            ctk.CTkLabel(d,text=lab).pack(anchor="w",padx=35,pady=(10,3)); e=ctk.CTkEntry(d); e.pack(fill="x",padx=35); ent[key]=e
        def save():
            try: ok,msg=add_inventory(ent["name"].get(),ent["quantity"].get(),ent["unit"].get(),ent["minimum"].get(),ent["cost"].get())
            except: return
            if ok: d.destroy(); self.load()
        ctk.CTkButton(d,text="Save",command=save).pack(pady=25)
    def edit(self,i):
        d=ctk.CTkToplevel(self); d.title("Edit Inventory"); d.geometry("450x380"); d.grab_set()
        vals={}
        for lab,key,val in [("Quantity","q",i["quantity"]),("Minimum Stock","m",i["minimum_stock"]),("Cost Per Unit","c",i["cost_per_unit"])]:
            ctk.CTkLabel(d,text=lab).pack(anchor="w",padx=30,pady=(12,3)); e=ctk.CTkEntry(d); e.pack(fill="x",padx=30); e.insert(0,str(val)); vals[key]=e
        def save():
            update_inventory(i["id"],vals["q"].get(),vals["m"].get(),vals["c"].get()); d.destroy(); self.load()
        ctk.CTkButton(d,text="Save",command=save).pack(pady=25)
