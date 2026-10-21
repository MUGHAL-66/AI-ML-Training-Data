"""Automated tests using isolated temporary SQLite databases."""

import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from billing import checkout, get_receipt, sales_history
from cart import add_to_cart, calculate_cart, update_cart_quantity
from database import initialize_database
from products import (
    add_product,
    delete_product,
    get_product,
    list_products,
    update_product,
)
from sales_analysis import get_sales_analysis


class SupermarketTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_supermarket.db"
        initialize_database(self.db_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def product(self, product_id="P001"):
        return get_product(product_id, self.db_path)

    def test_starter_catalog_and_idempotent_initialization(self):
        first_ids = {item["product_id"] for item in list_products(self.db_path)}
        add_product("CUSTOM", "Custom item", "1.25", 4, "Test", self.db_path)
        initialize_database(self.db_path)
        self.assertGreaterEqual(len(first_ids), 10)
        self.assertIsNotNone(get_product("CUSTOM", self.db_path))
        for product in list_products(self.db_path):
            delete_product(product["product_id"], self.db_path)
        initialize_database(self.db_path)
        self.assertEqual(list_products(self.db_path), [])

    def test_add_product_and_reject_duplicate_or_invalid_values(self):
        created = add_product("NEW-1", "New item", "10.50", 3, "Test", self.db_path)
        self.assertEqual(created["price"], Decimal("10.5"))
        with self.assertRaisesRegex(ValueError, "already exists"):
            add_product("NEW-1", "Duplicate", 5, 1, "Test", self.db_path)
        with self.assertRaises(ValueError):
            add_product("BAD", "Bad price", -1, 1, "Test", self.db_path)
        with self.assertRaises(ValueError):
            add_product("BAD", "Bad stock", 1, -1, "Test", self.db_path)

    def test_update_product_and_reject_missing_id(self):
        updated = update_product("P001", "Fresh milk", "199.99", "Chilled", 8, self.db_path)
        self.assertEqual(updated["name"], "Fresh milk")
        self.assertEqual(updated["price"], Decimal("199.99"))
        self.assertEqual(updated["category"], "Chilled")
        self.assertEqual(updated["stock"], 8)
        with self.assertRaisesRegex(ValueError, "not found"):
            update_product("MISSING", "x", 1, "x", 0, self.db_path)

    def test_delete_product_preserves_existing_receipt_snapshot(self):
        cart = {}
        add_to_cart(cart, self.product(), 1)
        receipt = checkout(cart, self.db_path)
        delete_product("P001", self.db_path)
        saved_receipt = get_receipt(receipt["invoice_number"], self.db_path)
        self.assertIsNone(get_product("P001", self.db_path))
        self.assertEqual(saved_receipt["lines"][0]["name"], "Milk")
        self.assertEqual(saved_receipt["lines"][0]["category"], "Dairy")
        self.assertEqual(saved_receipt["lines"][0]["unit_price_cents"], 18000)

    def test_cart_calculations_for_multiple_items(self):
        cart = {}
        add_to_cart(cart, self.product("P001"), 2)
        add_to_cart(cart, self.product("P002"), 3)
        result = calculate_cart(cart)
        self.assertEqual(len(result["lines"]), 2)
        self.assertEqual(result["subtotal_cents"], 72000)
        self.assertEqual(result["discount_cents"], 0)
        self.assertEqual(result["total_cents"], 72000)

    def test_discount_threshold_is_exact(self):
        cart_below = {
            "one": {
                "product_id": "one", "name": "Item", "category": "Test",
                "price": Decimal("999.99"), "quantity": 1, "stock": 10,
            }
        }
        self.assertEqual(calculate_cart(cart_below)["discount_cents"], 0)
        cart_at_threshold = {
            "one": {
                "product_id": "one", "name": "Item", "category": "Test",
                "price": Decimal("1000.00"), "quantity": 1, "stock": 10,
            }
        }
        at_threshold = calculate_cart(cart_at_threshold)
        self.assertEqual(at_threshold["discount_percent"], 10)
        self.assertEqual(at_threshold["discount_cents"], 10000)
        self.assertEqual(at_threshold["total_cents"], 90000)
        half_cent_discount = {
            "one": {
                "product_id": "one", "name": "Item", "category": "Test",
                "price": Decimal("1000.05"), "quantity": 1, "stock": 10,
            }
        }
        self.assertEqual(calculate_cart(half_cent_discount)["discount_cents"], 10001)

    def test_invalid_zero_and_insufficient_cart_quantities(self):
        with self.assertRaises(ValueError):
            add_to_cart({}, self.product(), "not-a-number")
        with self.assertRaises(ValueError):
            add_to_cart({}, self.product(), 0)
        with self.assertRaises(ValueError):
            add_to_cart({}, self.product(), self.product()["stock"] + 1)
        cart = {}
        add_to_cart(cart, self.product(), 1)
        with self.assertRaises(ValueError):
            update_cart_quantity(cart, "P001", -1)
        update_cart_quantity(cart, "P001", 0)
        self.assertEqual(cart, {})

    def test_empty_checkout_and_empty_history(self):
        self.assertEqual(sales_history(self.db_path), [])
        report = get_sales_analysis(self.db_path)
        self.assertEqual(report["completed_transactions"], 0)
        self.assertEqual(report["total_revenue_cents"], 0)
        self.assertTrue(report["sample_sales"])
        with self.assertRaisesRegex(ValueError, "empty"):
            checkout({}, self.db_path)

    def test_successful_checkout_deducts_stock_and_saves_receipt(self):
        starting_stock = self.product()["stock"]
        cart = {}
        add_to_cart(cart, self.product(), 2)
        receipt = checkout(cart, self.db_path)
        self.assertEqual(self.product()["stock"], starting_stock - 2)
        self.assertEqual(receipt["status"], "completed")
        self.assertEqual(receipt["lines"][0]["quantity"], 2)
        self.assertTrue(receipt["invoice_number"].startswith("INV-"))
        self.assertEqual(len(sales_history(self.db_path)), 1)

    def test_stock_conflict_rolls_back_whole_checkout(self):
        product = self.product()
        cart = {}
        add_to_cart(cart, product, 2)
        update_product(
            product["product_id"], product["name"], product["price"],
            product["category"], 1, self.db_path,
        )
        with self.assertRaisesRegex(ValueError, "Insufficient stock"):
            checkout(cart, self.db_path)
        self.assertEqual(self.product()["stock"], 1)
        self.assertEqual(sales_history(self.db_path), [])

    def test_sales_analysis_revenue_units_best_seller_and_demo_separation(self):
        cart = {}
        add_to_cart(cart, self.product("P001"), 2)
        add_to_cart(cart, self.product("P002"), 1)
        checkout(cart, self.db_path)
        report = get_sales_analysis(self.db_path)
        self.assertEqual(report["completed_transactions"], 1)
        self.assertEqual(report["total_units_sold"], 3)
        self.assertEqual(report["total_revenue_cents"], 48000)
        self.assertEqual(report["best_selling_product"], "Milk")
        self.assertEqual(len(report["daily_sales"]), 1)
        self.assertEqual(report["sample_data_is_separate"], True)
        self.assertTrue(report["sample_sales"])


if __name__ == "__main__":
    unittest.main()
