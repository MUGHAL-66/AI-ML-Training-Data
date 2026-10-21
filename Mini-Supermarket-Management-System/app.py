"""Streamlit dashboard for the Mini Supermarket Management System."""

import pandas as pd
import plotly.express as px
import streamlit as st

from database import initialize_database
from products import list_products, low_stock_products
from sales_analysis import get_sales_analysis
from utils.helpers import apply_theme, format_money, style_chart


st.set_page_config(page_title="Mini Supermarket | Dashboard", page_icon="🛒", layout="wide")
initialize_database()
apply_theme()

st.title("Retail overview")
st.caption("Monitor your catalogue, inventory, and completed customer sales at a glance.")

products = list_products()
analysis = get_sales_analysis()
stock_total = sum(product["stock"] for product in products)
low_stock = low_stock_products()
best_seller = analysis["best_selling_product"] or "No sales yet"

first_kpis = st.columns(3)
first_kpis[0].metric("▦  Total products", len(products))
first_kpis[1].metric("□  Available stock", f"{stock_total:,}")
first_kpis[2].metric("↗  Total sales", analysis["completed_transactions"])
second_kpis = st.columns(3)
second_kpis[0].metric("₨  Total revenue", format_money(analysis["total_revenue_cents"]))
second_kpis[1].metric("★  Best-selling product", best_seller)
second_kpis[2].metric("!  Low-stock products", len(low_stock))

left, right = st.columns(2)
with left:
    st.subheader("Daily revenue trend")
    daily = analysis["daily_sales"]
    if daily:
        frame = pd.DataFrame(daily)
        frame["Revenue (PKR)"] = frame["revenue_cents"] / 100
        chart = px.line(
            frame, x="date", y="Revenue (PKR)", markers=True,
            color_discrete_sequence=["#2563EB"],
        )
        style_chart(chart)
        st.plotly_chart(chart, width="stretch")
    else:
        st.info("No real completed sales yet. Daily revenue will appear here after checkout.")

with right:
    st.subheader("Best-selling products")
    product_sales = analysis["revenue_by_product"]
    if product_sales:
        frame = pd.DataFrame(product_sales).sort_values("units_sold", ascending=True)
        chart = px.bar(
            frame, x="units_sold", y="name", orientation="h",
            labels={"units_sold": "Units sold", "name": "Product"},
            color_discrete_sequence=["#2563EB"],
        )
        style_chart(chart)
        st.plotly_chart(chart, width="stretch")
    else:
        st.info("No real completed sales yet. Product rankings will appear after checkout.")

left, right = st.columns(2)
with left:
    st.subheader("Inventory by category")
    if products:
        inventory = pd.DataFrame(products)
        category_stock = inventory.groupby("category", as_index=False)["stock"].sum()
        chart = px.pie(
            category_stock, names="category", values="stock", hole=0.45,
            color_discrete_sequence=["#2563EB", "#1E3A8A", "#60A5FA", "#93C5FD", "#475569"],
        )
        style_chart(chart)
        st.plotly_chart(chart, width="stretch")
    else:
        st.info("Add products to view inventory by category.")

with right:
    st.subheader("Sales distribution by category")
    categories = analysis["sales_by_category"]
    if categories:
        frame = pd.DataFrame(categories)
        frame["Revenue (PKR)"] = frame["revenue_cents"] / 100
        chart = px.pie(
            frame, names="category", values="Revenue (PKR)", hole=0.45,
            color_discrete_sequence=["#2563EB", "#1E3A8A", "#60A5FA", "#93C5FD", "#475569"],
        )
        style_chart(chart)
        st.plotly_chart(chart, width="stretch")
    else:
        st.info("No real completed sales yet, so category revenue is not available.")

st.subheader("Sample sales data (demonstration only)")
st.caption("These preloaded examples are stored separately and are never included in actual sales KPIs.")
if analysis["sample_sales"]:
    sample = pd.DataFrame(analysis["sample_sales"])
    sample["Example revenue"] = sample["revenue_cents"].map(format_money)
    st.dataframe(sample[["name", "category", "units_sold", "Example revenue"]], hide_index=True)
