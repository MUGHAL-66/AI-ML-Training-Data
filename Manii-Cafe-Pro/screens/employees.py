import customtkinter as ctk
from services.employee_service import get_all_employees,save_employee,deactivate_employee
from utils.theme import COLORS,FONTS

class EmployeesScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate):
        super().__init__(parent,fg_color=COLORS["background"]); self.navigate=navigate; self.build(); self.load()
    def build(self):
        h=ctk.CTkFrame(self,fg_color="transparent"); h.pack(fill="x",padx=25,pady=25)
        ctk.CTkLabel(h,text="Employees",font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(h,text="+ Add Employee",command=self.form).pack(side="right",padx=5)
        ctk.CTkButton(h,text="← Dashboard",command=lambda:self.navigate("dashboard")).pack(side="right")
        self.scroll=ctk.CTkScrollableFrame(self,fg_color="transparent"); self.scroll.pack(fill="both",expand=True,padx=25,pady=10)
    def load(self):
        for w in self.scroll.winfo_children(): w.destroy()
        for e in get_all_employees():
            c=ctk.CTkFrame(self.scroll,fg_color=COLORS["card"],corner_radius=14); c.pack(fill="x",pady=5)
            ctk.CTkLabel(c,text=e["name"],font=FONTS["subheading"]).pack(side="left",padx=18,pady=15)
            ctk.CTkLabel(c,text=f"{e['role']} • Rs {e['salary']:,.0f} • {'Active' if e['active'] else 'Inactive'}",text_color=COLORS["text_secondary"]).pack(side="left")
            ctk.CTkButton(c,text="Edit",width=70,command=lambda x=e:self.form(x)).pack(side="right",padx=5)
            if e["active"]: ctk.CTkButton(c,text="Deactivate",width=100,fg_color=COLORS["danger"],command=lambda i=e["id"]:self.remove(i)).pack(side="right",padx=5)
    def form(self,e=None):
        d=ctk.CTkToplevel(self); d.title("Employee"); d.geometry("520x620"); d.grab_set()
        ent={}
        for lab,key in [("Name","name"),("Phone","phone"),("Email","email"),("Salary","salary"),("Hire Date","hire_date")]:
            ctk.CTkLabel(d,text=lab).pack(anchor="w",padx=35,pady=(10,3)); x=ctk.CTkEntry(d,height=38); x.pack(fill="x",padx=35); ent[key]=x
            if e: x.insert(0,str(e[key] or ""))
        role=ctk.CTkOptionMenu(d,values=["Admin","Cashier","Barista"]); role.pack(fill="x",padx=35,pady=15)
        if e: role.set(e["role"])
        def save():
            try: salary=float(ent["salary"].get() or 0)
            except: salary=0
            save_employee(ent["name"].get(),ent["phone"].get(),ent["email"].get(),role.get(),salary,ent["hire_date"].get(),e["id"] if e else None,e["active"] if e else 1)
            d.destroy(); self.load()
        ctk.CTkButton(d,text="Save Employee",height=45,fg_color=COLORS["gold"],text_color=COLORS["black"],command=save).pack(fill="x",padx=35,pady=20)
    def remove(self,i): deactivate_employee(i); self.load()
