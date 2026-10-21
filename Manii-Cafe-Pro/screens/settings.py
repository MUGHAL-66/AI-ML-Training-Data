import customtkinter as ctk
from database.database import get_connection
from services.backup_service import create_backup,list_backups
from utils.theme import COLORS,FONTS
from utils.constants import APP_VERSION

class SettingsScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate):
        super().__init__(parent,fg_color=COLORS["background"]); self.navigate=navigate; self.build(); self.load()
    def build(self):
        h=ctk.CTkFrame(self,fg_color="transparent"); h.pack(fill="x",padx=25,pady=25)
        ctk.CTkLabel(h,text="Settings",font=FONTS["title"]).pack(side="left")
        ctk.CTkButton(h,text="← Dashboard",command=lambda:self.navigate("dashboard")).pack(side="right")
        self.box=ctk.CTkScrollableFrame(self,fg_color="transparent"); self.box.pack(fill="both",expand=True,padx=25)
    def load(self):
        for w in self.box.winfo_children(): w.destroy()
        con=get_connection(); r=con.execute("SELECT * FROM cafe_settings WHERE id=1").fetchone(); con.close()
        ent={}
        for lab,key in [("Cafe Name","cafe_name"),("Phone","phone"),("Address","address"),("Tax %","tax_percentage"),("Currency","currency"),("Receipt Footer","receipt_footer")]:
            ctk.CTkLabel(self.box,text=lab).pack(anchor="w",pady=(10,3)); e=ctk.CTkEntry(self.box,height=40); e.pack(fill="x"); e.insert(0,str(r[key] or "")); ent[key]=e
        def save():
            con=get_connection()
            con.execute("""
                UPDATE cafe_settings SET cafe_name=?,phone=?,address=?,tax_percentage=?,currency=?,receipt_footer=?,updated_at=CURRENT_TIMESTAMP WHERE id=1
            """,(ent["cafe_name"].get(),ent["phone"].get(),ent["address"].get(),float(ent["tax_percentage"].get() or 5),ent["currency"].get(),ent["receipt_footer"].get()))
            con.commit(); con.close(); self.notice("Settings saved.")
        ctk.CTkButton(self.box,text="Save Settings",height=45,fg_color=COLORS["gold"],text_color=COLORS["black"],command=save).pack(fill="x",pady=20)
        ctk.CTkLabel(self.box,text="Database Backup",font=FONTS["heading"]).pack(anchor="w",pady=(20,10))
        ctk.CTkButton(self.box,text="Create Backup",command=lambda:self.notice(f"Backup created:\n{create_backup()}")).pack(anchor="w")
        ctk.CTkLabel(self.box,text=f"Version {APP_VERSION}",text_color=COLORS["muted"]).pack(anchor="w",pady=25)
    def notice(self,text):
        d=ctk.CTkToplevel(self); d.title("Settings"); d.geometry("450x190")
        ctk.CTkLabel(d,text=text,wraplength=380,justify="center").pack(pady=35); ctk.CTkButton(d,text="OK",command=d.destroy).pack()
