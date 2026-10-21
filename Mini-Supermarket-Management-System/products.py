"""Product catalogue and inventory operations."""

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import sqlite3

from database import database_connection, initialize_database


def money_to_cents(value):
    """Convert a non-negative currency value to integer paisa/cents."""
    try:
        amount = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError) as error:
        raise ValueError("Price must be a valid number.") from error
    if not amount.is_finite() or amount < 0:
        raise ValueError("Price cannot be negative.")
    return int((amount * 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def validate_quantity(quantity, allow_zero=False):
    """Convert and validate a whole-number stock or purchase quantity."""
    if isinstance(quantity, bool):
        raise ValueError("Quantity must be a whole number.")
    try:
        numeric_quantity = int(str(quantity).strip())
    except (TypeError, ValueError) as error:
        raise ValueError("Quantity must be a whole number.") from error
    if str(quantity).strip() != str(numeric_quantity):
        raise ValueError("Quantity must be a whole number.")
    minimum = 0 if allow_zero else 1
    if numeric_quantity < minimum:
        raise ValueError(
            "Stock cannot be negative." if allow_zero else "Quantity must be greater than zero."
        )
    return numeric_quantity


def _product_dict(row):
    product = dict(row)
    product["price"] = Decimal(product.pop("price_cents")) / Decimal(100)
    return product


def list_products(db_path=None, search=None):
    """Return all products, optionally matching ID, name, or category."""
    initialize_database(db_path)
    with database_connection(db_path) as connection:
        if search and search.strip():
            pattern = f"%{search.strip()}%"
            rows = connection.execute(
                """
                SELECT product_id, name, price_cents, stock, category
                FROM products
                WHERE product_id LIKE ? OR name LIKE ? OR category LIKE ?
                ORDER BY name COLLATE NOCASE
                """,
                (pattern, pattern, pattern),
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT product_id, name, price_cents, stock, category
                FROM products ORDER BY name COLLATE NOCASE
                """
            ).fetchall()
    return [_product_dict(row) for row in rows]


def get_product(product_id, db_path=None):
    """Find one product by its ID, returning None when it does not exist."""
    initialize_database(db_path)
    with database_connection(db_path) as connection:
        row = connection.execute(
            """
            SELECT product_id, name, price_cents, stock, category
            FROM products WHERE product_id = ?
            """,
            (str(product_id).strip(),),
        ).fetchone()
    return _product_dict(row) if row else None


def add_product(product_id, name, price, stock, category, db_path=None):
    """Add a product after validating its fields and unique ID."""
    product_id = str(product_id).strip().upper()
    name = str(name).strip()
    category = str(category).strip()
    if not product_id or not name or not category:
        raise ValueError("Product ID, name, and category are required.")
    price_cents = money_to_cents(price)
    stock = validate_quantity(stock, allow_zero=True)
    initialize_database(db_path)
    try:
        with database_connection(db_path) as connection:
            connection.execute(
                """
                INSERT INTO products (product_id, name, price_cents, stock, category)
                VALUES (?, ?, ?, ?, ?)
                """,
                (product_id, name, price_cents, stock, category),
            )
            connection.commit()
    except sqlite3.IntegrityError as error:
        raise ValueError(f"Product ID '{product_id}' already exists.") from error
    return get_product(product_id, db_path)


def update_product(product_id, name, price, category, stock, db_path=None):
    """Update the editable details of an existing product."""
    name = str(name).strip()
    category = str(category).strip()
    if not name or not category:
        raise ValueError("Product name and category are required.")
    price_cents = money_to_cents(price)
    stock = validate_quantity(stock, allow_zero=True)
    initialize_database(db_path)
    with database_connection(db_path) as connection:
        cursor = connection.execute(
            """
            UPDATE products
            SET name = ?, price_cents = ?, category = ?, stock = ?
            WHERE product_id = ?
            """,
            (name, price_cents, category, stock, str(product_id).strip()),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"Product '{product_id}' was not found.")
        connection.commit()
    return get_product(product_id, db_path)


def delete_product(product_id, db_path=None):
    """Delete a product while preserving past sale-item snapshots."""
    initialize_database(db_path)
    with database_connection(db_path) as connection:
        cursor = connection.execute(
            "DELETE FROM products WHERE product_id = ?", (str(product_id).strip(),)
        )
        if cursor.rowcount == 0:
            raise ValueError(f"Product '{product_id}' was not found.")
        connection.commit()


def low_stock_products(threshold=10, db_path=None):
    """Return products at or below a non-negative stock threshold."""
    threshold = validate_quantity(threshold, allow_zero=True)
    return [product for product in list_products(db_path) if product["stock"] <= threshold]
