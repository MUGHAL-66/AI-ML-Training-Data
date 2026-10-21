from database.database import get_connection
from utils.helpers import generate_order_number

def calculate_order_totals(cart,discount=0,tax_percentage=5):
    subtotal=sum(float(i["price"])*int(i["quantity"]) for i in cart)
    discount=max(float(discount or 0),0)
    taxable=max(subtotal-discount,0)
    tax=taxable*float(tax_percentage)/100
    return {"subtotal":round(subtotal,2),"discount":round(discount,2),
            "tax":round(tax,2),"total":round(taxable+tax,2)}

def _check_stock(con,cart):
    needed={}
    for item in cart:
        size=con.execute("""
            SELECT id FROM product_sizes WHERE product_id=? AND size_name=? AND active=1
        """,(item["product_id"],item["size"])).fetchone()
        if not size:
            return False,f"Size not found: {item['size']}"
        recipes=con.execute("""
            SELECT pr.inventory_id,pr.quantity_required,i.item_name,i.quantity,i.unit
            FROM product_recipes pr JOIN inventory i ON i.id=pr.inventory_id
            WHERE pr.product_size_id=?
        """,(size["id"],)).fetchall()
        for r in recipes:
            iid=r["inventory_id"]
            needed[iid]=needed.get(iid,0)+float(r["quantity_required"])*int(item["quantity"])
            if iid not in needed or needed[iid] <= r["quantity"]:
                pass
            if needed[iid] > float(r["quantity"]):
                return False,f"Not enough {r['item_name']}. Required {needed[iid]:.2f} {r['unit']}, available {r['quantity']:.2f} {r['unit']}."
    return True,"Inventory available."

def create_order(cart,payment_method,cashier_id,discount=0,tax_percentage=5,
                 customer_id=None,order_type="Takeaway",amount_received=None):
    if not cart: return {"success":False,"message":"Cart is empty."}
    totals=calculate_order_totals(cart,discount,tax_percentage)
    if payment_method=="Cash":
        try: received=float(amount_received)
        except: return {"success":False,"message":"Enter valid cash received."}
        if received<totals["total"]:
            return {"success":False,"message":f"Insufficient cash. Total Rs {totals['total']:,.2f}, received Rs {received:,.2f}."}
        change=received-totals["total"]
    else:
        received=totals["total"]; change=0

    con=get_connection()
    try:
        ok,msg=_check_stock(con,cart)
        if not ok: return {"success":False,"message":msg}

        order_no=generate_order_number()
        cur=con.cursor()
        cur.execute("""
            INSERT INTO orders(order_number,customer_id,subtotal,discount,tax,total,payment_method,
            amount_received,change_amount,order_type,status,cashier_id)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
        """,(order_no,customer_id,totals["subtotal"],totals["discount"],totals["tax"],totals["total"],
             payment_method,received,change,order_type,"Pending",cashier_id))
        oid=cur.lastrowid

        for item in cart:
            cur.execute("""
                INSERT INTO order_items(order_id,product_id,product_name,size_name,quantity,unit_price,total_price)
                VALUES(?,?,?,?,?,?,?)
            """,(oid,item["product_id"],item["name"],item["size"],item["quantity"],
                 item["price"],item["price"]*item["quantity"]))

        cur.execute("""
            INSERT INTO payments(order_id,method,amount,status,transaction_reference)
            VALUES(?,?,?,?,?)
        """,(oid,payment_method,totals["total"],"Paid",order_no))

        for item in cart:
            ps=cur.execute("""
                SELECT id FROM product_sizes WHERE product_id=? AND size_name=? AND active=1
            """,(item["product_id"],item["size"])).fetchone()
            recipes=cur.execute("""
                SELECT pr.inventory_id,pr.quantity_required,i.item_name,i.quantity
                FROM product_recipes pr JOIN inventory i ON i.id=pr.inventory_id
                WHERE pr.product_size_id=?
            """,(ps["id"],)).fetchall()
            for r in recipes:
                used=float(r["quantity_required"])*int(item["quantity"])
                cur.execute("UPDATE inventory SET quantity=quantity-?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
                            (used,r["inventory_id"]))
                cur.execute("""
                    INSERT INTO inventory_transactions(inventory_id,transaction_type,quantity,reason,reference)
                    VALUES(?,?,?,?,?)
                """,(r["inventory_id"],"SALE",-used,f"Used for {item['name']}",order_no))

        if customer_id:
            points=int(totals["total"]//100)
            cur.execute("""
                UPDATE customers SET total_orders=total_orders+1,total_spent=total_spent+?,
                loyalty_points=loyalty_points+?,updated_at=CURRENT_TIMESTAMP WHERE id=?
            """,(totals["total"],points,customer_id))

        con.commit()
        return {"success":True,"order_id":oid,"order_number":order_no,**totals,
                "payment_method":payment_method,"amount_received":received,"change_amount":change}
    except Exception as e:
        con.rollback()
        return {"success":False,"message":str(e)}
    finally: con.close()

def get_all_orders():
    con=get_connection()
    try:
        return con.execute("""
            SELECT o.*,u.full_name AS cashier_name,c.name AS customer_name
            FROM orders o
            LEFT JOIN users u ON u.id=o.cashier_id
            LEFT JOIN customers c ON c.id=o.customer_id
            ORDER BY o.id DESC
        """).fetchall()
    finally: con.close()

def get_order_by_id(oid):
    con=get_connection()
    try: return con.execute("SELECT * FROM orders WHERE id=?",(oid,)).fetchone()
    finally: con.close()

def get_order_items(oid):
    con=get_connection()
    try: return con.execute("SELECT * FROM order_items WHERE order_id=? ORDER BY id",(oid,)).fetchall()
    finally: con.close()

def update_order_status(oid,status):
    con=get_connection()
    try:
        con.execute("UPDATE orders SET status=? WHERE id=?",(status,oid)); con.commit()
        return True
    finally: con.close()

def cancel_order(oid):
    con=get_connection()
    try:
        order=con.execute("SELECT * FROM orders WHERE id=?",(oid,)).fetchone()
        if not order or order["status"]=="Cancelled":
            return False,"Order not found/already cancelled."
        if order["status"]=="Completed":
            return False,"Completed orders cannot be cancelled from this screen."
        items=con.execute("SELECT * FROM order_items WHERE order_id=?",(oid,)).fetchall()
        for item in items:
            ps=con.execute("SELECT id FROM product_sizes WHERE product_id=? AND size_name=?",(item["product_id"],item["size_name"])).fetchone()
            if ps:
                recipes=con.execute("SELECT inventory_id,quantity_required FROM product_recipes WHERE product_size_id=?",(ps["id"],)).fetchall()
                for r in recipes:
                    con.execute("UPDATE inventory SET quantity=quantity+? WHERE id=?",
                                (float(r["quantity_required"])*item["quantity"],r["inventory_id"]))
        con.execute("UPDATE orders SET status=? WHERE id=? ",("Cancelled",oid))
        con.commit(); return True,"Order cancelled and stock restored."
    except Exception as e:
        con.rollback(); return False,str(e)
    finally: con.close()
