"""Product catalogue, search, and manager CRUD page."""

import pandas as pd
import streamlit as st

from products import add_product, delete_product, list_products, update_product
from utils.helpers import apply_theme


st.set_page_config(page_title="Products | Mini Supermarket", layout="wide")
apply_theme()
st.title("Product management")
st.caption("Search, add, update, and remove products from your catalogue.")
search = st.text_input("Search by product ID, name, or category")
products = list_products(search=search)
if products:
    frame = pd.DataFrame(products)
    frame["Price (PKR)"] = frame["price"].map(lambda value: f"PKR {value:,.2f}")
    st.dataframe(
        frame[["product_id", "name", "category", "Price (PKR)", "stock"]],
        hide_index=True, width="stretch",
    )
else:
    st.info("No products match your search.")

add_tab, edit_tab, delete_tab = st.tabs(["Add product", "Edit product", "Delete product"])
with add_tab:
    with st.form("add_product_form", clear_on_submit=True, border=True):
        product_id = st.text_input("Unique product ID")
        name = st.text_input("Product name")
        price = st.number_input("Price (PKR)", min_value=0.0, step=10.0, format="%.2f")
        stock = st.number_input("Initial stock", min_value=0, step=1)
        category = st.text_input("Category")
        submitted = st.form_submit_button("Add product", type="primary")
    if submitted:
        try:
            add_product(product_id, name, price, stock, category)
            st.success("Product added.")
            st.rerun()
        except ValueError as error:
            st.error(str(error))

with edit_tab:
    if products:
        product_ids = [product["product_id"] for product in products]
        selected_id = st.selectbox("Select product to edit", product_ids, key="edit_product_id")
        selected = next(item for item in products if item["product_id"] == selected_id)
        with st.form("edit_product_form", border=True):
            edit_name = st.text_input("Name", value=selected["name"])
            edit_price = st.number_input(
                "Price (PKR)", min_value=0.0, value=float(selected["price"]),
                step=10.0, format="%.2f",
            )
            edit_category = st.text_input("Category", value=selected["category"])
            edit_stock = st.number_input(
                "Stock", min_value=0, value=int(selected["stock"]), step=1,
            )
            submitted = st.form_submit_button("Save changes", type="primary")
        if submitted:
            try:
                update_product(selected_id, edit_name, edit_price, edit_category, edit_stock)
                st.success("Product updated.")
                st.rerun()
            except ValueError as error:
                st.error(str(error))
    else:
        st.info("Add a product before editing.")

with delete_tab:
    all_products = list_products()
    if all_products:
        selected_id = st.selectbox(
            "Select product to delete",
            [product["product_id"] for product in all_products],
            key="delete_product_id",
        )
        selected = next(item for item in all_products if item["product_id"] == selected_id)
        st.warning(
            f"Delete {selected['name']}? Saved receipts retain its name, price, and category."
        )
        with st.container(key="delete-action"):
            if st.button("Confirm delete", type="primary"):
                try:
                    delete_product(selected_id)
                    st.success("Product deleted; sales history is preserved.")
                    st.rerun()
                except ValueError as error:
                    st.error(str(error))
    else:
        st.info("There are no products to delete.")
