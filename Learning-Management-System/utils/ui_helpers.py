import pandas as pd
import streamlit as st
from db import DatabaseError

THEME_CSS = """
<style>
:root { color-scheme: light; --burgundy:#641E32; --burgundy-hover:#842B45; --gold:#D4A853; --canvas:#F5F3F2; --ink:#24212A; --muted:#77727B; }
.stApp { background:var(--canvas); color:var(--ink); }
.block-container { max-width:1440px; padding:2.25rem clamp(1.2rem,3vw,3rem) 3rem; }
h1,h2,h3,h4 { color:var(--ink); letter-spacing:-.025em; }
h1 { font-weight:750; }
p, label, [data-testid="stCaptionContainer"] { color:var(--muted); }
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child { background:var(--burgundy); border-right:0; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p, [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span { color:#F4EDEF; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#D7C4CA; }
[data-testid="stSidebar"] hr { border-color:#8A5968; }
[data-testid="stSidebarNav"] { padding-top:.8rem; }
[data-testid="stSidebarNav"] a { color:#F2E9EC; border-radius:10px; margin:.15rem .35rem; transition:background .18s ease,color .18s ease; }
[data-testid="stSidebarNav"] a:hover { background:#842B45; color:white; }
[data-testid="stSidebarNav"] a[aria-current="page"] { background:#842B45; color:white; border-left:3px solid var(--gold); }
[data-testid="stSidebarNav"] a span { color:inherit; }
[data-testid="stMetric"] { background:#fff; border:1px solid #ECE7E5; border-radius:14px; padding:18px 20px; box-shadow:0 4px 16px rgba(44,28,34,.045); min-height:112px; }
[data-testid="stMetricLabel"] { color:var(--muted); font-weight:600; }
[data-testid="stMetricValue"] { color:var(--ink); font-weight:750; }
[data-testid="stDataFrame"], [data-testid="stTable"] { border:1px solid #E9E4E2; border-radius:12px; overflow:hidden; }
[data-testid="stExpander"] { background:#fff; border:1px solid #E9E4E2; border-radius:12px; }
[data-testid="stVerticalBlockBorderWrapper"] { border-color:#E9E4E2 !important; border-radius:14px !important; background:#fff; }
.stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] button { border-radius:9px; border:1px solid var(--burgundy); color:white; background:var(--burgundy); font-weight:650; transition:background .18s ease, transform .18s ease; }
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stFormSubmitButton"] button:hover { background:var(--burgundy-hover); border-color:var(--burgundy-hover); color:white; transform:translateY(-1px); }
.stTextInput input, .stTextArea textarea, .stNumberInput input, [data-baseweb="select"] > div, [data-testid="stDateInput"] input { border-radius:8px; }
[data-testid="stAlert"] { border-radius:10px; }
@media (max-width: 700px) { .block-container { padding:1.2rem 1rem 2rem; } [data-testid="stMetric"] { padding:14px; } }
</style>
"""

def apply_theme():
    st.markdown(THEME_CSS, unsafe_allow_html=True)

def page_header(title, subtitle):
    st.title(title)
    st.caption(subtitle)

def run_page(fn):
    try:
        fn()
    except DatabaseError as exc:
        st.error(str(exc))
        st.info("Set DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, and DB_NAME in your local .env, then confirm the database schema is imported.")

def frame(rows, **kwargs):
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, **kwargs)
    else:
        st.info("No records match this view yet.")

def csv_download(rows, name):
    if rows:
        st.download_button("Download CSV", pd.DataFrame(rows).to_csv(index=False).encode("utf-8"), file_name=name, mime="text/csv")
