from database.database import get_connection

def get_all_customers():
    con=get_connection()
    try: return con.execute("SELECT * FROM customers ORDER BY id DESC").fetchall()
    finally: con.close()

def add_customer(name,phone="",email=""):
    con=get_connection()
    try:
        con.execute("INSERT INTO customers(name,phone,email) VALUES(?,?,?)",
                    (name.strip(),phone.strip(),email.strip()))
        con.commit(); return True,"Customer added successfully."
    except Exception as e:
        con.rollback(); return False,str(e)
    finally: con.close()

def update_customer(cid,name,phone="",email=""):
    con=get_connection()
    try:
        con.execute("UPDATE customers SET name=?,phone=?,email=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
                    (name.strip(),phone.strip(),email.strip(),cid))
        con.commit(); return True,"Customer updated successfully."
    except Exception as e:
        con.rollback(); return False,str(e)
    finally: con.close()

def delete_customer(cid):
    con=get_connection()
    try:
        con.execute("DELETE FROM customers WHERE id=?",(cid,)); con.commit()
    finally: con.close()
