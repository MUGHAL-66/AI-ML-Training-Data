from .database import get_connection
from utils.security import hash_password

def seed_database():
    con = get_connection()
    cur = con.cursor()

    if cur.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        users = [
            ("admin", hash_password("admin123"), "Cafe Administrator", "Admin"),
            ("cashier", hash_password("cashier123"), "Main Cashier", "Cashier"),
            ("barista", hash_password("barista123"), "Main Barista", "Barista"),
        ]
        cur.executemany(
            "INSERT INTO users(username,password_hash,full_name,role) VALUES(?,?,?,?)",
            users
        )

    if cur.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        products = [
            ("Espresso","Coffee","Strong classic espresso",180),
            ("Americano","Coffee","Espresso with hot water",220),
            ("Cappuccino","Coffee","Espresso, milk and foam",280),
            ("Latte","Coffee","Smooth espresso with milk",300),
            ("Green Tea","Tea","Refreshing green tea",180),
            ("Black Tea","Tea","Classic black tea",150),
            ("Iced Coffee","Cold Drinks","Cold creamy coffee",320),
            ("Chocolate Cake","Desserts","Fresh chocolate cake",350),
        ]
        cur.executemany(
            "INSERT INTO products(name,category,description,price) VALUES(?,?,?,?)",
            products
        )

    if cur.execute("SELECT COUNT(*) FROM inventory").fetchone()[0] == 0:
        items = [
            ("Coffee Beans",5000,"g",500,0.8),
            ("Milk",30000,"ml",5000,0.25),
            ("Water",50000,"ml",10000,0.03),
            ("Tea Leaves",2000,"g",300,0.5),
            ("Cake Stock",20,"pcs",3,250),
        ]
        cur.executemany(
            "INSERT INTO inventory(item_name,quantity,unit,minimum_stock,cost_per_unit) VALUES(?,?,?,?,?)",
            items
        )

    size_count = cur.execute("SELECT COUNT(*) FROM product_sizes").fetchone()[0]
    if size_count == 0:
        product_rows = cur.execute("SELECT id,name,category,price FROM products").fetchall()
        for p in product_rows:
            for size, extra in [("Small",0),("Medium",40),("Large",80)]:
                cur.execute(
                    "INSERT INTO product_sizes(product_id,size_name,extra_price) VALUES(?,?,?)",
                    (p["id"],size,extra)
                )

    if cur.execute("SELECT COUNT(*) FROM cafe_settings").fetchone()[0] == 0:
        cur.execute("""
            INSERT INTO cafe_settings(id,cafe_name,phone,address,tax_percentage,currency,receipt_footer)
            VALUES(1,'MANII CAFE','+92 300 0000000','Pakistan',5,'Rs','Thank you for visiting MANII CAFE!')
        """)

    con.commit()
    con.close()
