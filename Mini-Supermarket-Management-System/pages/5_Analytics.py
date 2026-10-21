"""Real sales analytics and separately labelled demonstration data."""

import pandas as pd
import plotly.express as px
import streamlit as st

from cart import format_pkr
from sales_analysis import get_sales_analysis
from utils.helpers import apply_theme, style_chart


st.set_page_config(page_title="Sales Analytics | Mini Supermarket", layout="wide")
apply_theme()
st.title("Sales analytics")
st.caption("Explore completed customer sales. Demonstration examples remain separate.")
report = get_sales_analysis()
metric_columns = st.columns(4)
metric_columns[0].metric("Completed transactions", report["completed_transactions"])
metric_columns[1].metric("Units sold", report["total_units_sold"])
metric_columns[2].metric("Real revenue", format_pkr(report["total_revenue_cents"]))
metric_columns[3].metric("Best seller", report["best_selling_product"] or "No sales yet")

if report["revenue_by_product"]:
    left, right = st.columns(2)
    with left:
        st.subheader("Revenue by product")
        frame = pd.DataFrame(report["revenue_by_product"])
        frame["Revenue (PKR)"] = frame["revenue_cents"] / 100
        st.plotly_chart(
            style_chart(px.bar(
                frame, x="name", y="Revenue (PKR)",
                color_discrete_sequence=["#2563EB"],
            )),
            width="stretch",
        )
    with right:
        st.subheader("Sales by category")
        frame = pd.DataFrame(report["sales_by_category"])
        frame["Revenue (PKR)"] = frame["revenue_cents"] / 100
        st.plotly_chart(
            style_chart(px.pie(
                frame, names="category", values="Revenue (PKR)", hole=0.4,
                color_discrete_sequence=["#2563EB", "#1E3A8A", "#60A5FA", "#93C5FD"],
            )),
            width="stretch",
        )
    st.subheader("Daily sales totals")
    daily = pd.DataFrame(report["daily_sales"])
    daily["Revenue (PKR)"] = daily["revenue_cents"] / 100
    st.plotly_chart(
        style_chart(px.bar(
            daily, x="date", y="Revenue (PKR)",
            color_discrete_sequence=["#2563EB"],
        )),
        width="stretch",
    )
else:
    st.info("No completed customer sales yet. Actual sales charts appear after successful checkout.")

st.divider()
st.subheader("Demonstration data — not customer sales")
st.caption("These sample rows are provided for practice. They are excluded from every actual-sales KPI and chart.")
sample = report["sample_sales"]
if sample:
    frame = pd.DataFrame(sample)
    frame["Example revenue"] = frame["revenue_cents"].map(format_pkr)
    st.dataframe(frame[["name", "category", "units_sold", "Example revenue"]], hide_index=True)
