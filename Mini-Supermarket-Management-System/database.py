"""SQLite setup and connection helpers for the supermarket application."""

import os
import sqlite3
from contextlib import contextmanager
from decimal import Decimal
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_DATABASE_PATH = PROJECT_DIR / "data" / "supermarket.db"

STARTER_PRODUCTS = [
    ("P001", "Milk", "Dairy", "180.00", 40),
    ("P002", "Bread", "Bakery", "120.00", 35),
    ("P003", "Rice", "Grains", "320.00", 50),
    ("P004", "Sugar", "Grocery", "160.00", 45),
    ("P005", "Cooking Oil", "Grocery", "650.00", 25),
    ("P006", "Eggs", "Dairy", "300.00", 30),
    ("P007", "Tea", "Beverages", "450.00", 20),
    ("P008", "Biscuits", "Snacks", "90.00", 60),
    ("P009", "Soap", "Personal Care", "110.00", 40),
    ("P010", "Shampoo", "Personal Care", "520.00", 18),
]


def get_database_path(db_path=None):
    """Return an explicit path, or the path configured for this application."""
    if db_path is not None:
        return Path(db_path)
    return Path(os.environ.get("SUPERMARKET_DB_PATH", DEFAULT_DATABASE_PATH))


def get_connection(db_path=None):
    """Open a SQLite connection with foreign-key checks enabled."""
    path = get_database_path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path), timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def database_connection(db_path=None):
    """Yield a connection and reliably close it after the operation."""
    connection = get_connection(db_path)
    try:
        yield connection
    finally:
        connection.close()


def initialize_database(db_path=None):
    """Create tables and add starter/demo data once, without resetting data."""
    with database_connection(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
                stock INTEGER NOT NULL CHECK (stock >= 0),
                category TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT NOT NULL UNIQUE,
                created_at TEXT NOT NULL,
                subtotal_cents INTEGER NOT NULL,
                discount_cents INTEGER NOT NULL,
                discount_percent INTEGER NOT NULL,
                total_cents INTEGER NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('completed', 'cancelled'))
            );
            CREATE TABLE IF NOT EXISTS sale_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_id INTEGER NOT NULL REFERENCES sales(sale_id),
                product_id TEXT REFERENCES products(product_id) ON DELETE SET NULL,
                product_name TEXT NOT NULL,
                product_category TEXT NOT NULL,
                unit_price_cents INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                line_total_cents INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sample_sales (
                sample_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                note TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS app_metadata (
                metadata_key TEXT PRIMARY KEY,
                metadata_value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS sample_sale_items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sample_id TEXT NOT NULL REFERENCES sample_sales(sample_id),
                product_name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                revenue_cents INTEGER NOT NULL
            );
            """
        )
        products_seeded = connection.execute(
            "SELECT 1 FROM app_metadata WHERE metadata_key = 'starter_products_seeded'"
        ).fetchone()
        product_count = connection.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if products_seeded is None and product_count == 0:
            connection.executemany(
                """
                INSERT INTO products (product_id, name, category, price_cents, stock)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (product_id, name, category, int(Decimal(price) * 100), stock)
                    for product_id, name, category, price, stock in STARTER_PRODUCTS
                ],
            )
        if products_seeded is None:
            connection.execute(
                "INSERT INTO app_metadata (metadata_key, metadata_value) VALUES (?, ?)",
                ("starter_products_seeded", "yes"),
            )

        samples_seeded = connection.execute(
            "SELECT 1 FROM app_metadata WHERE metadata_key = 'sample_sales_seeded'"
        ).fetchone()
        sample_count = connection.execute("SELECT COUNT(*) FROM sample_sales").fetchone()[0]
        if samples_seeded is None and sample_count == 0:
            connection.executemany(
                "INSERT INTO sample_sales (sample_id, created_at, note) VALUES (?, ?, ?)",
                [
                    ("DEMO-001", "2025-01-10T10:00:00", "Clearly labelled demonstration data"),
                    ("DEMO-002", "2025-01-11T12:30:00", "Clearly labelled demonstration data"),
                ],
            )
            connection.executemany(
                """
                INSERT INTO sample_sale_items
                    (sample_id, product_name, category, quantity, revenue_cents)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    ("DEMO-001", "Milk", "Dairy", 3, 54000),
                    ("DEMO-001", "Bread", "Bakery", 2, 24000),
                    ("DEMO-002", "Rice", "Grains", 2, 64000),
                    ("DEMO-002", "Milk", "Dairy", 1, 18000),
                ],
            )
        if samples_seeded is None:
            connection.execute(
                "INSERT INTO app_metadata (metadata_key, metadata_value) VALUES (?, ?)",
                ("sample_sales_seeded", "yes"),
            )
        connection.commit()
