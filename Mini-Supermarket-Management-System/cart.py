"""Shopping-cart calculations shared by the console and web interfaces."""

from decimal import Decimal

from products import money_to_cents, validate_quantity


DISCOUNT_THRESHOLD_CENTS = 100_000
DISCOUNT_PERCENT = 10


def add_to_cart(cart, product, quantity):
    """Add units of a product, refusing quantities beyond available stock."""
    quantity = validate_quantity(quantity)
    product_id = product["product_id"]
    current_quantity = cart.get(product_id, {}).get("quantity", 0)
    if current_quantity + quantity > product["stock"]:
        raise ValueError(
            f"Only {product['stock']} unit(s) of {product['name']} are in stock."
        )
    cart[product_id] = {
        "product_id": product_id,
        "name": product["name"],
        "category": product["category"],
        "price": Decimal(product["price"]),
        "stock": product["stock"],
        "quantity": current_quantity + quantity,
    }
    return cart


def update_cart_quantity(cart, product_id, quantity):
    """Change a cart line quantity or remove it when quantity is zero."""
    if product_id not in cart:
        raise ValueError(f"Product '{product_id}' is not in the cart.")
    quantity = validate_quantity(quantity, allow_zero=True)
    if quantity == 0:
        del cart[product_id]
    elif quantity > cart[product_id]["stock"]:
        raise ValueError(
            f"Only {cart[product_id]['stock']} unit(s) are in stock."
        )
    else:
        cart[product_id]["quantity"] = quantity
    return cart


def calculate_cart(cart):
    """Calculate line totals, subtotal, discount, and amount payable in cents."""
    lines = []
    subtotal_cents = 0
    for item in cart.values():
        unit_price_cents = money_to_cents(item["price"])
        quantity = validate_quantity(item["quantity"])
        line_total_cents = unit_price_cents * quantity
        subtotal_cents += line_total_cents
        lines.append(
            {
                "product_id": item["product_id"],
                "name": item["name"],
                "category": item["category"],
                "unit_price_cents": unit_price_cents,
                "quantity": quantity,
                "line_total_cents": line_total_cents,
            }
        )
    discount_percent = DISCOUNT_PERCENT if subtotal_cents >= DISCOUNT_THRESHOLD_CENTS else 0
    discount_cents = (subtotal_cents * discount_percent + 50) // 100
    return {
        "lines": lines,
        "subtotal_cents": subtotal_cents,
        "discount_percent": discount_percent,
        "discount_cents": discount_cents,
        "total_cents": subtotal_cents - discount_cents,
    }


def cents_to_decimal(cents):
    """Format integer cents as an exact Decimal currency amount."""
    return Decimal(cents) / Decimal(100)


def format_pkr(cents):
    """Format integer cents as a Pakistani-rupee amount."""
    return f"PKR {cents_to_decimal(cents):,.2f}"
