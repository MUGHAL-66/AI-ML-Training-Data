"""Stock overview and low-stock report."""

import pandas as pd
import streamlit as st

from products import list_products, low_stock_products
from utils.helpers import apply_theme


st.set_page_config(page_title="Inventory | Mini Supermarket", layout="wide")
apply_theme()
st.title("Inventory")
st.caption("Monitor available quantities and identify products that need replenishment.")
threshold = st.number_input("Low-stock alert threshold", min_value=0, value=10, step=1)
products = list_products()
st.metric("Units currently in stock", sum(product["stock"] for product in products))
low_stock = low_stock_products(threshold)
st.subheader(f"Low-stock products (at or below {threshold})")
if low_stock:
    st.warning(f"{len(low_stock)} product(s) need a stock review.")
    st.dataframe(
        pd.DataFrame(low_stock)[["product_id", "name", "category", "stock"]],
        hide_index=True, width="stretch",
    )
else:
    st.success("No products are below the selected stock threshold.")
st.subheader("Healthy stock")
healthy_stock = [product for product in products if product["stock"] > threshold]
if healthy_stock:
    st.success(f"{len(healthy_stock)} product(s) are above the low-stock threshold.")
    st.dataframe(
        pd.DataFrame(healthy_stock)[["product_id", "name", "category", "stock"]],
        hide_index=True, width="stretch",
    )
else:
    st.info("No products currently exceed the selected stock threshold.")
st.subheader("Full inventory")
if products:
    st.dataframe(
        pd.DataFrame(products)[["product_id", "name", "category", "stock"]],
        hide_index=True, width="stretch",
    )
else:
    st.info("No products in the catalogue.")
st.caption("Adjust stock on the Products page. Completed checkouts automatically deduct inventory.")
