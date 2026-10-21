from database.database import get_connection

def get_all_inventory():
    con=get_connection()
    try: return con.execute("SELECT * FROM inventory ORDER BY item_name").fetchall()
    finally: con.close()

def add_inventory(name,quantity,unit,minimum_stock,cost):
    con=get_connection()
    try:
        cur=con.execute("""
            INSERT INTO inventory(item_name,quantity,unit,minimum_stock,cost_per_unit)
            VALUES(?,?,?,?,?)
        """,(name.strip(),float(quantity),unit,float(minimum_stock),float(cost)))
        iid=cur.lastrowid
        con.execute("""
            INSERT INTO inventory_transactions(inventory_id,transaction_type,quantity,reason)
            VALUES(?,?,?,?)
        """,(iid,"STOCK_IN",float(quantity),"Initial stock"))
        con.commit(); return True,"Stock item added."
    except Exception as e:
        con.rollback(); return False,str(e)
    finally: con.close()

def update_inventory(iid,quantity,minimum_stock,cost):
    con=get_connection()
    try:
        old=con.execute("SELECT quantity FROM inventory WHERE id=?",(iid,)).fetchone()
        con.execute("""
            UPDATE inventory SET quantity=?,minimum_stock=?,cost_per_unit=?,updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        """,(float(quantity),float(minimum_stock),float(cost),iid))
        if old:
            diff=float(quantity)-float(old["quantity"])
            if diff:
                con.execute("""
                    INSERT INTO inventory_transactions(inventory_id,transaction_type,quantity,reason)
                    VALUES(?,?,?,?)
                """,(iid,"ADJUSTMENT",diff,"Manual stock adjustment"))
        con.commit()
    finally: con.close()

def delete_inventory(iid):
    con=get_connection()
    try:
        con.execute("DELETE FROM inventory WHERE id=?",(iid,)); con.commit(); return True,"Deleted."
    except Exception as e:
        con.rollback(); return False,str(e)
    finally: con.close()

def get_low_stock_items():
    con=get_connection()
    try: return con.execute("SELECT * FROM inventory WHERE quantity<=minimum_stock ORDER BY quantity").fetchall()
    finally: con.close()
