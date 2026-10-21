import customtkinter as ctk
from services.product_service import get_all_products,save_product,delete_product,get_product_sizes,add_size,delete_size
from utils.theme import COLORS,FONTS
from utils.helpers import money

class ProductsScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate):
        super().__init__(parent,fg_color=COLORS["background"]); self.navigate=navigate; self.build(); self.load()
    def build(self):
        h=ctk.CTkFrame(self,fg_color="transparent"); h.pack(fill="x",padx=25,pady=25)
        ctk.CTkLabel(h,text="Products",font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(h,text="+ Add Product",command=lambda:self.form()).pack(side="right",padx=5)
        ctk.CTkButton(h,text="← Dashboard",command=lambda:self.navigate("dashboard")).pack(side="right")
        self.search=ctk.CTkEntry(self,placeholder_text="Search...",height=40); self.search.pack(fill="x",padx=25); self.search.bind("<KeyRelease>",lambda e:self.load())
        self.scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); self.scroll.pack(fill="both",expand=True,padx=25,pady=15)
    def load(self):
        for w in self.scroll.winfo_children(): w.destroy()
        q=self.search.get().lower().strip()
        for p in get_all_products():
            if q and q not in p["name"].lower(): continue
            c=ctk.CTkFrame(self.scroll,fg_color=COLORS["card"],corner_radius=14); c.pack(fill="x",pady=5)
            ctk.CTkLabel(c,text=p["name"],font=FONTS["subheading"]).pack(side="left",padx=18,pady=15)
            ctk.CTkLabel(c,text=f"{p['category']} • {money(p['price'])}",text_color=COLORS["gold"]).pack(side="left")
            ctk.CTkButton(c,text="Sizes",width=75,command=lambda x=p:self.sizes(x)).pack(side="right",padx=4)
            ctk.CTkButton(c,text="Edit",width=70,command=lambda x=p:self.form(x)).pack(side="right",padx=4)
            ctk.CTkButton(c,text="Delete",width=75,fg_color=COLORS["danger"],command=lambda i=p["id"]:self.remove(i)).pack(side="right",padx=4)
    def form(self,p=None):
        d=ctk.CTkToplevel(self); d.title("Product"); d.geometry("500x520"); d.grab_set()
        fields={}; data=[("Name","name"),("Category","category"),("Description","description"),("Base Price","price")]
        for label,key in data:
            ctk.CTkLabel(d,text=label).pack(anchor="w",padx=35,pady=(12,3)); e=ctk.CTkEntry(d,height=38); e.pack(fill="x",padx=35); fields[key]=e
            if p: e.insert(0,str(p[key] or ""))
        def save():
            if not fields["name"].get().strip(): return
            try: price=float(fields["price"].get())
            except: return
            save_product(fields["name"].get(),fields["category"].get(),fields["description"].get(),price,p["id"] if p else None)
            d.destroy(); self.load()
        ctk.CTkButton(d,text="Save Product",height=45,fg_color=COLORS["gold"],text_color=COLORS["black"],command=save).pack(fill="x",padx=35,pady=25)
    def remove(self,i): delete_product(i); self.load()
    def sizes(self,p):
        d=ctk.CTkToplevel(self); d.title(f"Sizes - {p['name']}"); d.geometry("450x450"); d.grab_set()
        box=ctk.CTkScrollableFrame(d); box.pack(fill="both",expand=True,padx=15,pady=15)
        for s in get_product_sizes(p["id"]):
            row=ctk.CTkFrame(box); row.pack(fill="x",pady=4)
            ctk.CTkLabel(row,text=f"{s['size_name']}  + {money(s['extra_price'])}").pack(side="left",padx=10,pady=8)
            ctk.CTkButton(row,text="Delete",width=70,fg_color=COLORS["danger"],command=lambda i=s["id"]:self.del_size(i,d,p)).pack(side="right",padx=5)
        ctk.CTkButton(d,text="+ Add Size",command=lambda:self.add_size_dialog(d,p)).pack(pady=10)
    def add_size_dialog(self,parent,p):
        d=ctk.CTkToplevel(parent); d.title("Add Size"); d.geometry("380x280"); d.grab_set()
        n=ctk.CTkEntry(d,placeholder_text="Size (Small/Medium/Large)"); n.pack(fill="x",padx=30,pady=25)
        x=ctk.CTkEntry(d,placeholder_text="Extra Price"); x.pack(fill="x",padx=30,pady=10)
        def save():
            try: add_size(p["id"],n.get(),float(x.get() or 0))
            except: return
            d.destroy(); parent.destroy(); self.sizes(p)
        ctk.CTkButton(d,text="Save",command=save).pack(pady=20)
    def del_size(self,i,parent,p):
        delete_size(i); parent.destroy(); self.sizes(p)
