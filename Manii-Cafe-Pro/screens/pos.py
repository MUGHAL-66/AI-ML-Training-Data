import customtkinter as ctk
from database.database import get_connection
from services.product_service import get_all_products,get_categories,get_product_sizes
from services.customer_service import get_all_customers
from services.order_service import calculate_order_totals,create_order
from components.receipt import create_pdf_receipt
from utils.theme import COLORS,FONTS
from utils.constants import PAYMENT_CASH,PAYMENT_CARD,PAYMENT_DIGITAL,ORDER_DINE_IN,ORDER_TAKEAWAY,ORDER_DELIVERY
from utils.helpers import money

class POSScreen(ctk.CTkFrame):
    def __init__(self,parent,user,navigate):
        super().__init__(parent,fg_color=COLORS["background"]); self.user=user; self.navigate=navigate
        self.cart=[]; self.payment_method=PAYMENT_CASH
        self.tax=5; self.build()
    def build(self):
        top=ctk.CTkFrame(self,fg_color=COLORS["card"],height=65); top.pack(fill="x")
        ctk.CTkLabel(top,text="POINT OF SALE",font=FONTS["heading"]).pack(side="left",padx=20,pady=15)
        ctk.CTkButton(top,text="← Dashboard",command=lambda:self.navigate("dashboard")).pack(side="right",padx=15)
        left=ctk.CTkFrame(self,fg_color="transparent"); left.pack(side="left",fill="both",expand=True,padx=(20,10),pady=15)
        self.search=ctk.CTkEntry(left,placeholder_text="Search products...",height=42); self.search.pack(fill="x",pady=(0,10)); self.search.bind("<KeyRelease>",lambda e:self.load_products())
        cats=ctk.CTkFrame(left,fg_color="transparent"); cats.pack(fill="x")
        ctk.CTkButton(cats,text="All",width=70,command=lambda:self.set_cat(None)).pack(side="left",padx=3)
        for cat in get_categories():
            ctk.CTkButton(cats,text=cat,width=100,command=lambda x=cat:self.set_cat(x)).pack(side="left",padx=3)
        self.category=None
        self.grid=ctk.CTkScrollableFrame(left,fg_color="transparent"); self.grid.pack(fill="both",expand=True,pady=10)
        right=ctk.CTkFrame(self,fg_color=COLORS["card"],width=420,corner_radius=0); right.pack(side="right",fill="y",padx=(10,20),pady=15); right.pack_propagate(False)
        ctk.CTkLabel(right,text="Current Order",font=FONTS["heading"]).pack(anchor="w",padx=18,pady=15)
        self.cart_frame=ctk.CTkScrollableFrame(right,height=230); self.cart_frame.pack(fill="x",padx=12)
        self.customer=ctk.CTkOptionMenu(right,values=["Walk-in Customer"]+[f"{c['id']} - {c['name']}" for c in get_all_customers()]); self.customer.pack(fill="x",padx=15,pady=8)
        self.order_type=ctk.CTkOptionMenu(right,values=[ORDER_TAKEAWAY,ORDER_DINE_IN,ORDER_DELIVERY]); self.order_type.pack(fill="x",padx=15,pady=5)
        self.discount=ctk.CTkEntry(right,placeholder_text="Discount (Rs)"); self.discount.pack(fill="x",padx=15,pady=5); self.discount.bind("<KeyRelease>",lambda e:self.refresh_summary())
        self.summary=ctk.CTkLabel(right,text="",justify="left",font=FONTS["body"]); self.summary.pack(anchor="w",padx=18,pady=10)
        ctk.CTkLabel(right,text="Payment Method",font=FONTS["subheading"]).pack(anchor="w",padx=18)
        self.payment=ctk.CTkOptionMenu(right,values=[PAYMENT_CASH,PAYMENT_CARD,PAYMENT_DIGITAL],command=self.payment_changed); self.payment.pack(fill="x",padx=15,pady=6)
        self.cash_area=ctk.CTkFrame(right,fg_color="transparent"); self.cash_area.pack(fill="x",padx=15)
        self.cash=ctk.CTkEntry(self.cash_area,placeholder_text="Cash Received"); self.cash.pack(fill="x",pady=5); self.cash.bind("<KeyRelease>",lambda e:self.refresh_summary())
        self.change=ctk.CTkLabel(self.cash_area,text="Change: Rs 0.00",text_color=COLORS["success"]); self.change.pack(anchor="w")
        ctk.CTkButton(right,text="✓ PROCESS ORDER",height=50,fg_color=COLORS["gold"],text_color=COLORS["black"],
                      hover_color=COLORS["gold_hover"],command=self.confirm_order).pack(fill="x",padx=15,pady=15)
        self.load_products(); self.refresh_cart()
    def set_cat(self,cat): self.category=cat; self.load_products()
    def load_products(self):
        for w in self.grid.winfo_children(): w.destroy()
        q=self.search.get().lower().strip()
        rows=get_all_products()
        if self.category: rows=[p for p in rows if p["category"]==self.category]
        if q: rows=[p for p in rows if q in p["name"].lower()]
        for i,p in enumerate(rows):
            c=ctk.CTkFrame(self.grid,fg_color=COLORS["card"],corner_radius=14); c.grid(row=i//3,column=i%3,sticky="nsew",padx=6,pady=6)
            ctk.CTkLabel(c,text=p["name"],font=FONTS["subheading"]).pack(pady=(18,4))
            ctk.CTkLabel(c,text=p["category"],text_color=COLORS["muted"]).pack()
            ctk.CTkLabel(c,text=money(p["price"]),font=FONTS["body"],text_color=COLORS["gold"]).pack(pady=5)
            ctk.CTkButton(c,text="Add",command=lambda x=p:self.choose_size(x)).pack(padx=15,pady=(5,18))
    def choose_size(self,p):
        sizes=get_product_sizes(p["id"])
        d=ctk.CTkToplevel(self); d.title("Select Size"); d.geometry("360x330"); d.transient(self.winfo_toplevel()); d.grab_set()
        ctk.CTkLabel(d,text=p["name"],font=FONTS["heading"]).pack(pady=20)
        for s in sizes:
            ctk.CTkButton(d,text=f"{s['size_name']}  •  {money(p['price']+s['extra_price'])}",
                          command=lambda x=s:self.add_item(p,x,d)).pack(fill="x",padx=35,pady=6)
    def add_item(self,p,s,d):
        price=float(p["price"])+float(s["extra_price"])
        for item in self.cart:
            if item["product_id"]==p["id"] and item["size"]==s["size_name"]:
                item["quantity"]+=1; d.destroy(); self.refresh_cart(); return
        self.cart.append({"product_id":p["id"],"name":p["name"],"size":s["size_name"],"price":price,"quantity":1})
        d.destroy(); self.refresh_cart()
    def refresh_cart(self):
        for w in self.cart_frame.winfo_children(): w.destroy()
        for idx,item in enumerate(self.cart):
            row=ctk.CTkFrame(self.cart_frame,fg_color=COLORS["card_light"]); row.pack(fill="x",pady=3)
            ctk.CTkLabel(row,text=f"{item['name']} • {item['size']}\n{money(item['price'])} x {item['quantity']}",justify="left").pack(side="left",padx=8,pady=7)
            ctk.CTkButton(row,text="−",width=30,command=lambda i=idx:self.change_qty(i,-1)).pack(side="right",padx=2)
            ctk.CTkButton(row,text="+",width=30,command=lambda i=idx:self.change_qty(i,1)).pack(side="right",padx=2)
        self.refresh_summary()
    def change_qty(self,i,delta):
        self.cart[i]["quantity"]+=delta
        if self.cart[i]["quantity"]<=0: self.cart.pop(i)
        self.refresh_cart()
    def refresh_summary(self):
        try: disc=float(self.discount.get() or 0)
        except: disc=0
        t=calculate_order_totals(self.cart,disc,self.tax)
        self.summary.configure(text=f"Subtotal       {money(t['subtotal'])}\nDiscount       {money(t['discount'])}\nTax ({self.tax:.0f}%)       {money(t['tax'])}\n\nTOTAL          {money(t['total'])}")
        try: received=float(self.cash.get() or 0); ch=max(received-t["total"],0)
        except: ch=0
        self.change.configure(text=f"Change: {money(ch)}")
    def payment_changed(self,value):
        self.payment_method=value
        if value==PAYMENT_CASH: self.cash_area.pack(fill="x",padx=15)
        else: self.cash_area.pack_forget()
        self.refresh_summary()
    def confirm_order(self):
        if not self.cart: return self.message("Cart is empty.")
        try: disc=float(self.discount.get() or 0)
        except: disc=0
        t=calculate_order_totals(self.cart,disc,self.tax)
        d=ctk.CTkToplevel(self); d.title("Confirm Order"); d.geometry("430x470"); d.transient(self.winfo_toplevel()); d.grab_set()
        text=f"Items: {sum(i['quantity'] for i in self.cart)}\n\nSubtotal: {money(t['subtotal'])}\nDiscount: {money(t['discount'])}\nTax: {money(t['tax'])}\n\nTOTAL: {money(t['total'])}\n\nPayment: {self.payment_method}\nOrder Type: {self.order_type.get()}"
        ctk.CTkLabel(d,text="Confirm Order",font=FONTS["heading"]).pack(pady=25)
        ctk.CTkLabel(d,text=text,justify="left",font=FONTS["body"]).pack(anchor="w",padx=40)
        ctk.CTkButton(d,text="✓ Confirm & Process",height=45,fg_color=COLORS["gold"],text_color=COLORS["black"],
                      command=lambda:self.process(d,disc)).pack(fill="x",padx=35,pady=18)
        ctk.CTkButton(d,text="Cancel",command=d.destroy).pack()
    def process(self,confirm_dialog,disc):
        cid=None
        val=self.customer.get()
        if val!="Walk-in Customer": cid=int(val.split(" - ")[0])
        received=self.cash.get() if self.payment_method==PAYMENT_CASH else None
        result=create_order(self.cart,self.payment_method,self.user["id"],disc,self.tax,cid,self.order_type.get(),received)
        if not result["success"]: return self.message(result["message"])
        confirm_dialog.destroy()
        self.success(result)
    def success(self,r):
        d=ctk.CTkToplevel(self); d.title("Order Successful"); d.geometry("470x500"); d.transient(self.winfo_toplevel()); d.grab_set()
        ctk.CTkLabel(d,text="✓",font=("Segoe UI",44,"bold"),text_color=COLORS["success"]).pack(pady=(25,0))
        ctk.CTkLabel(d,text="ORDER SUCCESSFUL",font=FONTS["heading"],text_color=COLORS["success"]).pack(pady=5)
        ctk.CTkLabel(d,text=r["order_number"],font=FONTS["subheading"],text_color=COLORS["gold"]).pack(pady=5)
        txt=f"Total: {money(r['total'])}\nPayment: {r['payment_method']}\n"
        if r["payment_method"]=="Cash": txt+=f"Received: {money(r['amount_received'])}\nChange: {money(r['change_amount'])}\n"
        txt+="\nStatus: Pending\nSent to Kitchen"
        ctk.CTkLabel(d,text=txt,justify="center",font=FONTS["body"]).pack(pady=15)
        ctk.CTkButton(d,text="🧾 View Receipt",command=lambda:self.receipt(r["order_id"])).pack(fill="x",padx=45,pady=5)
        ctk.CTkButton(d,text="+ New Order",command=lambda:(d.destroy(),self.new_order())).pack(fill="x",padx=45,pady=5)
        ctk.CTkButton(d,text="← Dashboard",command=lambda:(d.destroy(),self.navigate("dashboard"))).pack(fill="x",padx=45,pady=5)
    def receipt(self,oid):
        path=create_pdf_receipt(oid)
        self.message(f"Receipt created:\n{path}")
    def new_order(self):
        self.cart=[]; self.discount.delete(0,"end"); self.cash.delete(0,"end"); self.refresh_cart()
    def message(self,text):
        d=ctk.CTkToplevel(self); d.title("Message"); d.geometry("420x190")
        ctk.CTkLabel(d,text=text,wraplength=350,justify="center").pack(pady=35)
        ctk.CTkButton(d,text="OK",command=d.destroy).pack()
