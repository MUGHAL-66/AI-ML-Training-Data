from database.database import get_connection

def get_all_expenses():
    con=get_connection()
    try:
        return con.execute("""
            SELECT e.*,u.full_name AS created_by_name
            FROM expenses e LEFT JOIN users u ON u.id=e.created_by
            ORDER BY e.id DESC
        """).fetchall()
    finally: con.close()

def add_expense(title,category,amount,description,created_by):
    try: amount=float(amount)
    except: return False,"Invalid amount."
    if amount<0: return False,"Amount cannot be negative."
    con=get_connection()
    try:
        con.execute("""
            INSERT INTO expenses(title,category,amount,description,created_by)
            VALUES(?,?,?,?,?)
        """,(title.strip(),category.strip(),amount,description.strip(),created_by))
        con.commit(); return True,"Expense added."
    except Exception as e:
        con.rollback(); return False,str(e)
    finally: con.close()

def delete_expense(eid):
    con=get_connection()
    try:
        con.execute("DELETE FROM expenses WHERE id=?",(eid,)); con.commit()
    finally: con.close()

def get_expense_total(period="today"):
    con=get_connection()
    try:
        if period=="today":
            q="SELECT COALESCE(SUM(amount),0) FROM expenses WHERE DATE(created_at)=DATE('now','localtime')"
        elif period=="month":
            q="SELECT COALESCE(SUM(amount),0) FROM expenses WHERE strftime('%Y-%m',created_at)=strftime('%Y-%m','now','localtime')"
        else:
            q="SELECT COALESCE(SUM(amount),0) FROM expenses"
        return float(con.execute(q).fetchone()[0] or 0)
    finally: con.close()
