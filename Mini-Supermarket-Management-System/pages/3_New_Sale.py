"""Point-of-sale page with a cart stored safely in Streamlit session state."""

import streamlit as st

from billing import checkout
from cart import add_to_cart, calculate_cart, format_pkr, update_cart_quantity
from products import list_products
from utils.helpers import apply_theme


st.set_page_config(page_title="New Sale | Mini Supermarket", layout="wide")
apply_theme()
st.title("New sale / Point of sale")
st.caption("Build a customer cart, review the total, and complete checkout securely.")
if "cart" not in st.session_state:
    st.session_state.cart = {}
if "last_receipt" not in st.session_state:
    st.session_state.last_receipt = None

available = [product for product in list_products() if product["stock"] > 0]
with st.form("add_to_cart_form", border=True):
    if available:
        selected_id = st.selectbox(
            "Product", [item["product_id"] for item in available],
            format_func=lambda product_id: next(
                f"{item['name']} — {format_pkr(int(item['price'] * 100))} "
                f"({item['stock']} in stock)"
                for item in available if item["product_id"] == product_id
            ),
        )
        product = next(item for item in available if item["product_id"] == selected_id)
        quantity = st.number_input(
            "Quantity", min_value=1, max_value=int(product["stock"]), value=1, step=1,
        )
        add_clicked = st.form_submit_button("Add to cart", type="primary")
    else:
        st.info("There are no products currently in stock.")
        add_clicked = False
if add_clicked:
    try:
        add_to_cart(st.session_state.cart, product, quantity)
        st.success(f"Added {quantity} × {product['name']}.")
    except ValueError as error:
        st.error(str(error))

cart = st.session_state.cart
st.subheader("Shopping cart")
if cart:
    calculation = calculate_cart(cart)
    st.dataframe(
        [
            {
                "Product": line["name"],
                "Unit price": format_pkr(line["unit_price_cents"]),
                "Quantity": line["quantity"],
                "Line total": format_pkr(line["line_total_cents"]),
            }
            for line in calculation["lines"]
        ],
        hide_index=True, width="stretch",
    )
    update_col, remove_col = st.columns(2)
    with update_col:
        selected_to_update = st.selectbox("Change/remove item", list(cart), key="cart_line")
        new_quantity = st.number_input(
            "New quantity (choose 0 to remove)", min_value=0,
            max_value=int(cart[selected_to_update]["stock"]),
            value=int(cart[selected_to_update]["quantity"]), step=1,
        )
        if st.button("Update cart item"):
            try:
                update_cart_quantity(cart, selected_to_update, new_quantity)
                st.rerun()
            except ValueError as error:
                st.error(str(error))
    with remove_col:
        st.metric("Subtotal", format_pkr(calculation["subtotal_cents"]))
        if calculation["discount_percent"]:
            st.success(
                f"10% discount applied — you save "
                f"{format_pkr(calculation['discount_cents'])}."
            )
        else:
            amount_to_discount = max(0, 100000 - calculation["subtotal_cents"])
            st.info(
                f"Spend {format_pkr(amount_to_discount)} more to unlock the 10% discount."
            )
        st.metric(
            f"Discount ({calculation['discount_percent']}%)",
            f"-{format_pkr(calculation['discount_cents'])}",
        )
        st.metric("Final payable", format_pkr(calculation["total_cents"]))
        if st.button("Complete sale", type="primary"):
            try:
                st.session_state.last_receipt = checkout(cart)
                st.session_state.cart = {}
                st.success("Sale completed and stock updated.")
                st.rerun()
            except ValueError as error:
                st.error(str(error))
else:
    st.info("The cart is empty. Select products above to begin a sale.")

receipt = st.session_state.last_receipt
if receipt:
    st.divider()
    st.subheader("Latest receipt")
    st.markdown(f"**{receipt['supermarket_name']}**  \nInvoice: `{receipt['invoice_number']}`  \nDate: {receipt['created_at']}")
    for line in receipt["lines"]:
        st.write(
            f"{line['name']} — {line['quantity']} × "
            f"{format_pkr(line['unit_price_cents'])} = "
            f"{format_pkr(line['line_total_cents'])}"
        )
    st.write(f"Subtotal: {format_pkr(receipt['subtotal_cents'])}")
    st.write(
        f"Discount ({receipt['discount_percent']}%): "
        f"-{format_pkr(receipt['discount_cents'])}"
    )
    st.metric("Final payable", format_pkr(receipt["total_cents"]))
    st.success("Thank you for shopping with us!")
    st.caption("Use your browser's Print command to print this receipt.")
