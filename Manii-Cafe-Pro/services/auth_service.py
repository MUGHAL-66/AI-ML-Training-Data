from database.database import get_connection
from utils.security import verify_password

def login_user(username,password):
    con=get_connection()
    try:
        row=con.execute("""
            SELECT id,username,password_hash,full_name,role,active
            FROM users WHERE username=?
        """,(username.strip(),)).fetchone()
        if not row or row["active"] != 1:
            return None
        if not verify_password(password,row["password_hash"]):
            return None
        return dict(row)
    finally:
        con.close()
