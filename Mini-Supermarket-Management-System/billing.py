"""Atomic checkout, printable receipts, and sales-history queries."""

from datetime import datetime
from uuid import uuid4

from cart import calculate_cart
from database import database_connection, initialize_database
from products import validate_quantity


SUPERMARKET_NAME = "Mini Supermarket"


def checkout(cart, db_path=None):
    """Save a complete sale and deduct stock in one SQLite transaction."""
    if not cart:
        raise ValueError("The shopping cart is empty.")
    calculation = calculate_cart(cart)
    if not calculation["lines"]:
        raise ValueError("The shopping cart is empty.")
    initialize_database(db_path)
    created_at = datetime.now().astimezone().isoformat(timespec="seconds")
    invoice_number = f"INV-{datetime.now():%Y%m%d}-{uuid4().hex[:8].upper()}"

    with database_connection(db_path) as connection:
        try:
            connection.execute("BEGIN IMMEDIATE")
            for line in calculation["lines"]:
                product = connection.execute(
                    "SELECT name, price_cents, stock FROM products WHERE product_id = ?",
                    (line["product_id"],),
                ).fetchone()
                if product is None:
                    raise ValueError(
                        f"Product '{line['product_id']}' is no longer available."
                    )
                quantity = validate_quantity(line["quantity"])
                if product["stock"] < quantity:
                    raise ValueError(
                        f"Insufficient stock for {product['name']}: "
                        f"{product['stock']} available, {quantity} requested."
                    )
                if product["price_cents"] != line["unit_price_cents"]:
                    raise ValueError(
                        f"The price of {product['name']} changed. Please refresh your cart."
                    )
            cursor = connection.execute(
                """
                INSERT INTO sales
                    (invoice_number, created_at, subtotal_cents, discount_cents,
                     discount_percent, total_cents, status)
                VALUES (?, ?, ?, ?, ?, ?, 'completed')
                """,
                (
                    invoice_number,
                    created_at,
                    calculation["subtotal_cents"],
                    calculation["discount_cents"],
                    calculation["discount_percent"],
                    calculation["total_cents"],
                ),
            )
            sale_id = cursor.lastrowid
            for line in calculation["lines"]:
                connection.execute(
                    "UPDATE products SET stock = stock - ? WHERE product_id = ?",
                    (line["quantity"], line["product_id"]),
                )
                connection.execute(
                    """
                    INSERT INTO sale_items
                        (sale_id, product_id, product_name, product_category,
                         unit_price_cents, quantity, line_total_cents)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        sale_id,
                        line["product_id"],
                        line["name"],
                        line["category"],
                        line["unit_price_cents"],
                        line["quantity"],
                        line["line_total_cents"],
                    ),
                )
            connection.commit()
        except Exception:
            connection.rollback()
            raise

    return get_receipt(invoice_number, db_path)


def get_receipt(invoice_number, db_path=None):
    """Return one completed receipt, including its saved item snapshots."""
    initialize_database(db_path)
    with database_connection(db_path) as connection:
        sale = connection.execute(
            "SELECT * FROM sales WHERE invoice_number = ?", (invoice_number,)
        ).fetchone()
        if sale is None:
            return None
        lines = connection.execute(
            """
            SELECT product_name AS name, product_category AS category,
                   product_id, unit_price_cents,
                   quantity, line_total_cents
            FROM sale_items WHERE sale_id = ? ORDER BY item_id
            """,
            (sale["sale_id"],),
        ).fetchall()
    receipt = dict(sale)
    receipt["lines"] = [dict(line) for line in lines]
    receipt["supermarket_name"] = SUPERMARKET_NAME
    return receipt


def sales_history(db_path=None, limit=100):
    """List the latest completed receipts with their saved line items."""
    initialize_database(db_path)
    with database_connection(db_path) as connection:
        sales = connection.execute(
            """
            SELECT * FROM sales
            WHERE status = 'completed'
            ORDER BY created_at DESC, sale_id DESC LIMIT ?
            """,
            (int(limit),),
        ).fetchall()
        history = []
        for sale in sales:
            record = dict(sale)
            record["lines"] = [
                dict(line)
                for line in connection.execute(
                    """
                    SELECT product_name AS name, product_category AS category,
                           product_id, unit_price_cents,
                           quantity, line_total_cents
                    FROM sale_items WHERE sale_id = ? ORDER BY item_id
                    """,
                    (sale["sale_id"],),
                ).fetchall()
            ]
            history.append(record)
    return history
