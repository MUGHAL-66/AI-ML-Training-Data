import customtkinter as ctk
from services.auth_service import login_user
from utils.theme import COLORS

class LoginScreen(ctk.CTkFrame):
    def __init__(self,parent,on_success):
        super().__init__(parent,fg_color=COLORS["background"]); self.on_success=on_success
        box=ctk.CTkFrame(self,fg_color=COLORS["card"],corner_radius=20,width=430,height=500)
        box.place(relx=.5,rely=.5,anchor="center"); box.pack_propagate(False)
        ctk.CTkLabel(box,text="MANII CAFE",font=("Segoe UI",30,"bold"),text_color=COLORS["gold"]).pack(pady=(55,5))
        ctk.CTkLabel(box,text="PRO MANAGEMENT SYSTEM",font=("Segoe UI",12),text_color=COLORS["muted"]).pack(pady=(0,35))
        self.username=ctk.CTkEntry(box,placeholder_text="Username",height=45); self.username.pack(fill="x",padx=45,pady=8)
        self.password=ctk.CTkEntry(box,placeholder_text="Password",show="•",height=45); self.password.pack(fill="x",padx=45,pady=8)
        self.error=ctk.CTkLabel(box,text="",text_color=COLORS["danger"]); self.error.pack(pady=5)
        ctk.CTkButton(box,text="LOGIN",height=48,fg_color=COLORS["gold"],text_color=COLORS["black"],
                      hover_color=COLORS["gold_hover"],command=self.login).pack(fill="x",padx=45,pady=15)
        ctk.CTkLabel(box,text="admin / admin123",text_color=COLORS["muted"]).pack()
    def login(self):
        user=login_user(self.username.get(),self.password.get())
        if user: self.on_success(user)
        else: self.error.configure(text="Invalid username or password.")
