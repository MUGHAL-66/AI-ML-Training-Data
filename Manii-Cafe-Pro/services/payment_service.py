from database.database import get_connection

def get_order_payments(order_id):
    con=get_connection()
    try: return con.execute("SELECT * FROM payments WHERE order_id=? ORDER BY id DESC",(order_id,)).fetchall()
    finally: con.close()
