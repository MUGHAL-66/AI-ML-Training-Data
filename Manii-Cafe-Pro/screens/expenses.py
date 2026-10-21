import customtkinter as ctk
from services.expense_service import get_all_expenses,add_expense,delete_expense,get_expense_total
from utils.theme import COLORS,FONTS
from utils.helpers import money

class ExpensesScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate):
        super().__init__(parent,fg_color=COLORS["background"]); self.user=user; self.navigate=navigate; self.build(); self.load()
    def build(self):
        h=ctk.CTkFrame(self,fg_color="transparent"); h.pack(fill="x",padx=25,pady=25)
        ctk.CTkLabel(h,text="Expenses",font=FONTS["title"]).pack(side="left")
        self.total=ctk.CTkLabel(h,text="",font=FONTS["heading"],text_color=COLORS["gold"]); self.total.pack(side="left",padx=25)
        ctk.CTkButton(h,text="+ Add Expense",command=self.form).pack(side="right",padx=5)
        ctk.CTkButton(h,text="← Dashboard",command=lambda:self.navigate("dashboard")).pack(side="right")
        self.scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); self.scroll.pack(fill="both",expand=True,padx=25,pady=10)
    def load(self):
        for w in self.scroll.winfo_children(): w.destroy()
        self.total.configure(text=f"Today: {money(get_expense_total('today'))}")
        for e in get_all_expenses():
            c=ctk.CTkFrame(self.scroll,fg_color=COLORS["card"],corner_radius=14); c.pack(fill="x",pady=5)
            ctk.CTkLabel(c,text=e["title"],font=FONTS["subheading"]).pack(side="left",padx=18,pady=15)
            ctk.CTkLabel(c,text=f"{e['category']} • {money(e['amount'])} • {e['created_at']}",text_color=COLORS["text_secondary"]).pack(side="left")
            ctk.CTkButton(c,text="Delete",width=75,fg_color=COLORS["danger"],command=lambda i=e["id"]:self.remove(i)).pack(side="right",padx=15)
    def form(self):
        d=ctk.CTkToplevel(self); d.title("Add Expense"); d.geometry("500x500"); d.grab_set()
        ent={}
        for lab,key in [("Title","title"),("Amount","amount"),("Description","description")]:
            ctk.CTkLabel(d,text=lab).pack(anchor="w",padx=35,pady=(12,3)); x=ctk.CTkEntry(d,height=40); x.pack(fill="x",padx=35); ent[key]=x
        cat=ctk.CTkOptionMenu(d,values=["Rent","Electricity","Salary","Supplies","Maintenance","Marketing","Other"]); cat.pack(fill="x",padx=35,pady=15)
        def save():
            ok,msg=add_expense(ent["title"].get(),cat.get(),ent["amount"].get(),ent["description"].get(),self.user["id"])
            if ok: d.destroy(); self.load()
        ctk.CTkButton(d,text="Save Expense",height=45,fg_color=COLORS["gold"],text_color=COLORS["black"],command=save).pack(fill="x",padx=35,pady=20)
    def remove(self,i): delete_expense(i); self.load()
