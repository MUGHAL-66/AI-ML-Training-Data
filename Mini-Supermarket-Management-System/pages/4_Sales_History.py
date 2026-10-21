"""Receipt lookup and previous completed sales."""

import pandas as pd
import streamlit as st

from billing import get_receipt, sales_history
from utils.helpers import apply_theme, format_money


st.set_page_config(page_title="Sales History | Mini Supermarket", layout="wide")
apply_theme()
st.title("Receipts / Sales history")
st.caption("Review completed transactions and open saved receipt details.")
history = sales_history(limit=500)
if not history:
    st.info("No completed sales have been recorded yet.")
else:
    rows = [
        {
            "Invoice": sale["invoice_number"],
            "Date and time": sale["created_at"],
            "Items": sum(line["quantity"] for line in sale["lines"]),
            "Subtotal": format_money(sale["subtotal_cents"]),
            "Discount": format_money(sale["discount_cents"]),
            "Total": format_money(sale["total_cents"]),
        }
        for sale in history
    ]
    st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")
    invoice = st.selectbox("Open receipt", [sale["invoice_number"] for sale in history])
    receipt = get_receipt(invoice)
    st.subheader(receipt["supermarket_name"])
    st.write(f"**Invoice:** {receipt['invoice_number']}  |  **Date:** {receipt['created_at']}")
    st.dataframe(
        [
            {
                "Product": line["name"],
                "Unit price": format_money(line["unit_price_cents"]),
                "Quantity": line["quantity"],
                "Line total": format_money(line["line_total_cents"]),
            }
            for line in receipt["lines"]
        ],
        hide_index=True, width="stretch",
    )
    st.write(f"Subtotal: {format_money(receipt['subtotal_cents'])}")
    st.write(
        f"Discount ({receipt['discount_percent']}%): "
        f"-{format_money(receipt['discount_cents'])}"
    )
    st.metric("Final payable", format_money(receipt["total_cents"]))
