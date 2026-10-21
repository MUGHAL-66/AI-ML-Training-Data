"""Independent console interface for the Mini Supermarket Management System."""

from billing import checkout, sales_history
from cart import add_to_cart, calculate_cart, format_pkr, update_cart_quantity
from database import initialize_database
from products import add_product, delete_product, get_product, list_products, update_product
from sales_analysis import get_sales_analysis


def show_products():
    products = list_products()
    print("\nPRODUCT CATALOG")
    print("-" * 77)
    print(f"{'ID':<9}{'Product':<22}{'Category':<18}{'Price':>14}{'Stock':>10}")
    for product in products:
        print(
            f"{product['product_id']:<9}{product['name']:<22}"
            f"{product['category']:<18}{format_pkr(int(product['price'] * 100)):>14}"
            f"{product['stock']:>10}"
        )
    if not products:
        print("No products found.")


def show_cart(cart):
    if not cart:
        print("\nYour cart is empty.")
        return
    calculation = calculate_cart(cart)
    print("\nSHOPPING CART")
    for line in calculation["lines"]:
        print(
            f"{line['name']} x {line['quantity']} @ "
            f"{format_pkr(line['unit_price_cents'])} = "
            f"{format_pkr(line['line_total_cents'])}"
        )
    print(f"Subtotal: {format_pkr(calculation['subtotal_cents'])}")
    print(
        f"Discount ({calculation['discount_percent']}%): "
        f"-{format_pkr(calculation['discount_cents'])}"
    )
    print(f"Payable: {format_pkr(calculation['total_cents'])}")


def add_cart_item(cart):
    show_products()
    product = get_product(input("Enter product ID: ").strip().upper())
    if product is None:
        print("That product ID was not found.")
        return
    try:
        add_to_cart(cart, product, input("Quantity: "))
        print(f"Added {product['name']} to the cart.")
    except ValueError as error:
        print(f"Could not add item: {error}")


def manage_cart(cart):
    show_cart(cart)
    if not cart:
        return
    product_id = input("Enter cart product ID to update (or 0 to cancel): ").strip().upper()
    if product_id == "0":
        return
    try:
        update_cart_quantity(cart, product_id, input("New quantity (0 removes item): "))
        print("Cart updated.")
    except ValueError as error:
        print(f"Could not update cart: {error}")


def print_receipt(receipt):
    print(f"\n{'=' * 48}")
    print(f"{receipt['supermarket_name']:^48}")
    print(f"Invoice: {receipt['invoice_number']}")
    print(f"Date: {receipt['created_at']}")
    print("-" * 48)
    for line in receipt["lines"]:
        print(
            f"{line['name']}  {line['quantity']} x "
            f"{format_pkr(line['unit_price_cents'])} = "
            f"{format_pkr(line['line_total_cents'])}"
        )
    print("-" * 48)
    print(f"Subtotal: {format_pkr(receipt['subtotal_cents'])}")
    print(
        f"Discount ({receipt['discount_percent']}%): "
        f"-{format_pkr(receipt['discount_cents'])}"
    )
    print(f"Final payable: {format_pkr(receipt['total_cents'])}")
    print("Thank you for shopping with us!")
    print("=" * 48)


def manage_products():
    print("\nPRODUCT MANAGEMENT: 1 Add | 2 Update | 3 Delete | 4 Search")
    choice = input("Choose: ").strip()
    try:
        if choice == "1":
            add_product(
                input("Product ID: "),
                input("Name: "),
                input("Price (PKR): "),
                input("Stock: "),
                input("Category: "),
            )
            print("Product added.")
        elif choice == "2":
            product_id = input("Product ID: ").strip().upper()
            product = get_product(product_id)
            if product is None:
                print("Product not found.")
                return
            update_product(
                product_id,
                input(f"Name [{product['name']}]: ") or product["name"],
                input(f"Price [{product['price']}]: ") or product["price"],
                input(f"Category [{product['category']}]: ") or product["category"],
                input(f"Stock [{product['stock']}]: ") or product["stock"],
            )
            print("Product updated.")
        elif choice == "3":
            product_id = input("Product ID to delete: ").strip().upper()
            if input(f"Delete {product_id}? (y/N): ").strip().lower() == "y":
                delete_product(product_id)
                print("Product deleted; historical receipts are preserved.")
        elif choice == "4":
            for product in list_products(search=input("Search: ")):
                print(product)
        else:
            print("Choose 1, 2, 3, or 4.")
    except ValueError as error:
        print(f"Could not manage product: {error}")


def show_analysis():
    report = get_sales_analysis()
    print("\nSALES ANALYSIS (actual completed transactions only)")
    print(f"Completed transactions: {report['completed_transactions']}")
    print(f"Units sold: {report['total_units_sold']}")
    print(f"Revenue: {format_pkr(report['total_revenue_cents'])}")
    print(f"Best seller: {report['best_selling_product'] or 'No sales yet'}")
    if report["revenue_by_product"]:
        print("Sales by product:")
        for item in report["revenue_by_product"]:
            print(f"  {item['name']}: {item['units_sold']} units, {format_pkr(item['revenue_cents'])}")
    else:
        print("No completed sales yet. Demo figures are available in the dashboard.")


def show_sales_history():
    history = sales_history(limit=50)
    if not history:
        print("There are no completed receipts yet.")
        return
    for sale in history:
        print(
            f"{sale['invoice_number']} | {sale['created_at']} | "
            f"{format_pkr(sale['total_cents'])}"
        )
        for line in sale["lines"]:
            print(f"  {line['name']} x {line['quantity']}")


def run_console():
    initialize_database()
    cart = {}
    while True:
        print(
            "\nMINI SUPERMARKET\n"
            "1. Display Products\n"
            "2. Add Product to Cart\n"
            "3. View Shopping Cart\n"
            "4. Remove/Update Cart Item\n"
            "5. Generate Bill / Checkout\n"
            "6. Sales Analysis\n"
            "7. Manage Products (CRUD)\n"
            "8. View Sales History\n"
            "9. Exit"
        )
        choice = input("Select an option: ").strip()
        if choice == "1":
            show_products()
        elif choice == "2":
            add_cart_item(cart)
        elif choice == "3":
            show_cart(cart)
        elif choice == "4":
            manage_cart(cart)
        elif choice == "5":
            try:
                receipt = checkout(cart)
                print_receipt(receipt)
                cart.clear()
            except ValueError as error:
                print(f"Checkout could not be completed: {error}")
        elif choice == "6":
            show_analysis()
        elif choice == "7":
            manage_products()
        elif choice == "8":
            show_sales_history()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 1 to 9.")


if __name__ == "__main__":
    run_console()
