import customtkinter as ctk
from utils.theme import COLORS

class Sidebar(ctk.CTkFrame):
    def __init__(self,parent,user,navigate,logout):
        super().__init__(parent,width=230,fg_color=COLORS["sidebar"],corner_radius=0)
        self.pack_propagate(False)
        ctk.CTkLabel(self,text="MANII CAFE",font=("Segoe UI",20,"bold"),text_color=COLORS["gold"]).pack(pady=(28,4))
        ctk.CTkLabel(self,text=user["role"],font=("Segoe UI",11),text_color=COLORS["muted"]).pack(pady=(0,20))
        items=[("Dashboard","dashboard"),("POS","pos"),("Orders","orders"),("Products","products"),
               ("Inventory","inventory"),("Customers","customers"),("Employees","employees"),
               ("Expenses","expenses"),("Reports","reports"),("Kitchen","kitchen"),("Settings","settings")]
        allowed={
            "Admin":set(x[1] for x in items),
            "Cashier":{"dashboard","pos","orders","customers"},
            "Barista":{"dashboard","kitchen"}
        }
        for text,key in items:
            if key in allowed.get(user["role"],set()):
                ctk.CTkButton(self,text=text,anchor="w",height=40,fg_color="transparent",
                              hover_color=COLORS["card_light"],command=lambda k=key:navigate(k)).pack(fill="x",padx=12,pady=2)
        ctk.CTkButton(self,text="Logout",anchor="w",height=40,fg_color=COLORS["danger"],
                      hover_color="#DC2626",command=logout).pack(side="bottom",fill="x",padx=12,pady=18)
