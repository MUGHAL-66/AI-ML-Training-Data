from database.database import get_connection

def get_all_products(include_inactive=False):
    con=get_connection()
    try:
        sql="SELECT * FROM products"
        if not include_inactive: sql += " WHERE active=1"
        sql += " ORDER BY name"
        return con.execute(sql).fetchall()
    finally: con.close()

def get_categories():
    con=get_connection()
    try:
        return [r[0] for r in con.execute(
            "SELECT DISTINCT category FROM products WHERE active=1 ORDER BY category"
        ).fetchall()]
    finally: con.close()

def get_product_sizes(product_id):
    con=get_connection()
    try:
        return con.execute(
            "SELECT * FROM product_sizes WHERE product_id=? AND active=1 ORDER BY id",
            (product_id,)
        ).fetchall()
    finally: con.close()

def get_product(product_id):
    con=get_connection()
    try: return con.execute("SELECT * FROM products WHERE id=?",(product_id,)).fetchone()
    finally: con.close()

def save_product(name,category,description,price,product_id=None):
    con=get_connection()
    try:
        if product_id:
            con.execute("""
                UPDATE products SET name=?,category=?,description=?,price=?,updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """,(name,category,description,float(price),product_id))
        else:
            con.execute(
                "INSERT INTO products(name,category,description,price) VALUES(?,?,?,?)",
                (name,category,description,float(price))
            )
        con.commit()
    finally: con.close()

def delete_product(product_id):
    con=get_connection()
    try:
        con.execute("UPDATE products SET active=0 WHERE id=?",(product_id,))
        con.commit()
    finally: con.close()

def add_size(product_id,size_name,extra_price):
    con=get_connection()
    try:
        con.execute(
            "INSERT INTO product_sizes(product_id,size_name,extra_price) VALUES(?,?,?)",
            (product_id,size_name,float(extra_price or 0))
        )
        con.commit()
    finally: con.close()

def delete_size(size_id):
    con=get_connection()
    try:
        con.execute("DELETE FROM product_sizes WHERE id=?",(size_id,))
        con.commit()
    finally: con.close()
