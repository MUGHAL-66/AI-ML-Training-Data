import customtkinter as ctk
from utils.theme import COLORS

class Navbar(ctk.CTkFrame):
    def __init__(self,parent,title,user):
        super().__init__(parent,fg_color="transparent",height=65)
        ctk.CTkLabel(self,text=title,font=("Segoe UI",24,"bold")).pack(side="left",padx=20,pady=15)
        ctk.CTkLabel(self,text=f"{user['full_name']}  •  {user['role']}",
                     text_color=COLORS["text_secondary"]).pack(side="right",padx=20)
