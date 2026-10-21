from database.database import get_connection

def get_all_employees():
    con=get_connection()
    try: return con.execute("SELECT * FROM employees ORDER BY id DESC").fetchall()
    finally: con.close()

def save_employee(name,phone,email,role,salary,hire_date,employee_id=None,active=1):
    con=get_connection()
    try:
        data=(name.strip(),phone.strip(),email.strip(),role,float(salary or 0),hire_date,active)
        if employee_id:
            con.execute("""
                UPDATE employees SET name=?,phone=?,email=?,role=?,salary=?,hire_date=?,active=? WHERE id=?
            """,data+(employee_id,))
        else:
            con.execute("""
                INSERT INTO employees(name,phone,email,role,salary,hire_date,active) VALUES(?,?,?,?,?,?,?)
            """,data)
        con.commit(); return True,"Employee saved."
    except Exception as e:
        con.rollback(); return False,str(e)
    finally: con.close()

def deactivate_employee(eid):
    con=get_connection()
    try:
        con.execute("UPDATE employees SET active=0 WHERE id=?",(eid,)); con.commit()
    finally: con.close()
