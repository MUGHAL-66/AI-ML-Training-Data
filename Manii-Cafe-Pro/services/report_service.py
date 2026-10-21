from database.database import get_connection
from services.expense_service import get_expense_total

def dashboard_stats():
    con=get_connection()
    try:
        sales=con.execute("""
            SELECT COALESCE(SUM(total),0) FROM orders
            WHERE DATE(created_at)=DATE('now','localtime') AND status!='Cancelled'
        """).fetchone()[0]
        orders=con.execute("""
            SELECT COUNT(*) FROM orders
            WHERE DATE(created_at)=DATE('now','localtime') AND status!='Cancelled'
        """).fetchone()[0]
        customers=con.execute("SELECT COUNT(*) FROM customers").fetchone()[0]
        low=con.execute("SELECT COUNT(*) FROM inventory WHERE quantity<=minimum_stock").fetchone()[0]
        expenses=get_expense_total("today")
        return {"sales":float(sales or 0),"orders":int(orders),"customers":int(customers),
                "low_stock":int(low),"expenses":expenses,"profit":float(sales or 0)-expenses}
    finally: con.close()

def top_products(limit=5):
    con=get_connection()
    try:
        return con.execute("""
            SELECT product_name,SUM(quantity) qty,SUM(total_price) revenue
            FROM order_items oi JOIN orders o ON o.id=oi.order_id
            WHERE o.status!='Cancelled'
            GROUP BY product_id,product_name ORDER BY qty DESC LIMIT ?
        """,(limit,)).fetchall()
    finally: con.close()

def payment_summary():
    con=get_connection()
    try:
        return con.execute("""
            SELECT payment_method,SUM(total) total,COUNT(*) orders
            FROM orders WHERE status!='Cancelled'
            GROUP BY payment_method
        """).fetchall()
    finally: con.close()
