"""Shared presentation helpers for the Streamlit interface."""

import streamlit as st

from cart import format_pkr


def apply_theme():
    """Apply the shared accessible blue theme to every Streamlit page."""
    st.markdown(
        """
        <style>
        :root {
            color-scheme: light;
            --primary: #2563EB;
            --primary-dark: #1E3A8A;
            --navy: #0F172A;
            --navy-soft: #172554;
            --surface: #FFFFFF;
            --canvas: #F1F5F9;
            --ink: #0F172A;
            --muted: #475569;
            --border: #CBD5E1;
            --success: #16A34A;
            --warning: #D97706;
            --danger: #DC2626;
        }
        html, body, [class*="css"] { font-family: Inter, "Segoe UI", sans-serif; }
        .stApp { background: var(--canvas); color: var(--ink); }
        [data-testid="stAppViewContainer"] { background: var(--canvas); }
        [data-testid="stHeader"] {
            background: rgba(241, 245, 249, .94);
            color: var(--ink);
        }
        [data-testid="stMain"] { color: var(--ink); }
        [data-testid="stMain"] h1 {
            color: var(--ink); font-size: clamp(1.8rem, 3vw, 2.35rem);
            font-weight: 750; letter-spacing: -.035em; margin-bottom: .2rem;
        }
        [data-testid="stMain"] h2, [data-testid="stMain"] h3 { color: var(--ink); }
        [data-testid="stMain"] p, [data-testid="stCaptionContainer"],
        [data-testid="stMarkdownContainer"] { color: var(--muted); }
        [data-testid="stMain"] hr { border-color: var(--border); }

        /* Dark, high-contrast navigation with a subtle navy gradient. */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--navy) 0%, var(--navy-soft) 100%);
            border-right: 1px solid rgba(203, 213, 225, .16);
        }
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            padding-top: 1.1rem;
        }
        [data-testid="stSidebarNav"] {
            padding: .65rem .75rem 1rem;
        }
        [data-testid="stSidebarNav"]::before {
            content: "🏪  MINI SUPERMARKET";
            display: block; color: #FFFFFF; font-size: .98rem;
            font-weight: 750; letter-spacing: .035em;
            padding: .55rem .7rem 1.15rem;
        }
        [data-testid="stSidebarNav"] a {
            min-height: 2.75rem; border-radius: 9px; margin: .2rem 0;
            padding: .5rem .78rem;
            color: #E2E8F0 !important; transition: background-color .16s ease, color .16s ease;
        }
        [data-testid="stSidebarNav"] a[href$="/"] span {
            font-size: 0 !important; line-height: 1.2rem;
        }
        [data-testid="stSidebarNav"] a[href$="/"] span::after {
            content: "Dashboard"; font-size: .875rem; visibility: visible !important;
        }
        [data-testid="stSidebarNav"] a span {
            color: inherit !important; font-weight: 550;
        }
        [data-testid="stSidebarNav"] a:hover {
            background: #1D4ED8 !important; color: #FFFFFF !important;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            color: #FFFFFF !important; background: var(--primary) !important;
            box-shadow: inset 3px 0 #BFDBFE, 0 3px 12px rgba(15, 23, 42, .22);
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] small { color: #CBD5E1 !important; }

        /* White surfaces and navy text keep metrics readable in light mode. */
        [data-testid="stMetric"] {
            background: var(--surface); border: 1px solid #E2E8F0;
            border-left: 3px solid var(--primary); border-radius: 12px;
            padding: 16px 17px; min-height: 112px;
            box-shadow: 0 3px 12px rgba(15, 23, 42, .055);
        }
        [data-testid="stMetric"] label,
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"],
        [data-testid="stMetricDelta"] { color: var(--ink) !important; }
        [data-testid="stMetricLabel"] p {
            color: var(--muted) !important; font-size: .76rem !important;
            font-weight: 600; line-height: 1.25; white-space: normal;
            overflow: visible; text-overflow: clip;
        }
        [data-testid="stMetricValue"] {
            color: var(--ink) !important; font-size: clamp(1.3rem, 2.1vw, 1.9rem) !important;
            font-weight: 750; line-height: 1.2; white-space: normal;
            overflow-wrap: anywhere;
        }
        [data-testid="stMetricValue"] *,
        [data-testid="stMetricValue"] p {
            color: var(--ink) !important; white-space: normal !important;
            overflow: visible !important; text-overflow: clip !important;
            overflow-wrap: anywhere;
        }

        /* Inputs and menus use dark text on white, with visible keyboard focus. */
        [data-testid="stMain"] label,
        [data-testid="stMain"] [data-testid="stWidgetLabel"] p {
            color: var(--ink) !important; font-weight: 600;
        }
        [data-testid="stMain"] input,
        [data-testid="stMain"] textarea,
        [data-testid="stMain"] [data-baseweb="select"] > div,
        [data-testid="stMain"] [data-baseweb="input"] > div,
        [data-testid="stMain"] [data-baseweb="textarea"] > div {
            background: var(--surface) !important; color: var(--ink) !important;
            border-color: var(--border) !important; border-radius: 8px !important;
        }
        [data-testid="stMain"] input::placeholder,
        [data-testid="stMain"] textarea::placeholder { color: #64748B !important; opacity: 1; }
        [data-testid="stMain"] [data-baseweb="select"] *,
        [data-testid="stMain"] [data-baseweb="input"] *,
        [data-testid="stMain"] [data-baseweb="textarea"] * { color: var(--ink); }
        [data-baseweb="popover"], [data-baseweb="menu"], [role="listbox"] {
            background: var(--surface) !important; color: var(--ink) !important;
        }
        [role="option"] { color: var(--ink) !important; background: var(--surface) !important; }
        [role="option"]:hover, [role="option"][aria-selected="true"] {
            background: #DBEAFE !important; color: var(--primary-dark) !important;
        }
        [data-testid="stMain"] input:focus,
        [data-testid="stMain"] textarea:focus,
        [data-testid="stMain"] [data-baseweb="select"] > div:focus-within {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, .2) !important;
        }
        [data-testid="stMain"] input:disabled,
        [data-testid="stMain"] textarea:disabled {
            background: #E2E8F0 !important; color: #475569 !important;
        }

        /* Buttons have explicit contrast for primary and secondary actions. */
        [data-testid="stMain"] .stButton > button,
        [data-testid="stMain"] .stFormSubmitButton > button,
        [data-testid="stMain"] [data-testid="stDownloadButton"] > button {
            min-height: 2.55rem; border-radius: 8px; font-weight: 650;
            transition: background-color .15s ease, border-color .15s ease, transform .15s ease;
        }
        [data-testid="stMain"] button[kind="primary"] {
            background: var(--primary) !important; border: 1px solid var(--primary) !important;
            color: #FFFFFF !important;
        }
        [data-testid="stMain"] button[kind="primary"]:hover {
            background: var(--primary-dark) !important; border-color: var(--primary-dark) !important;
            color: #FFFFFF !important; transform: translateY(-1px);
        }
        [data-testid="stMain"] button[kind="secondary"],
        [data-testid="stMain"] .stButton > button:not([kind="primary"]) {
            background: #FFFFFF !important; border: 1px solid var(--border) !important;
            color: var(--ink) !important;
        }
        [data-testid="stMain"] button[kind="secondary"]:hover,
        [data-testid="stMain"] .stButton > button:not([kind="primary"]):hover {
            background: #EFF6FF !important; border-color: var(--primary) !important;
            color: var(--primary-dark) !important;
        }
        [data-testid="stMain"] button:disabled {
            background: #E2E8F0 !important; color: #64748B !important;
            border-color: #CBD5E1 !important; cursor: not-allowed;
        }
        [data-testid="stMain"] .st-key-delete-action button[kind="primary"] {
            background: var(--danger) !important; border-color: var(--danger) !important;
            color: #FFFFFF !important;
        }
        [data-testid="stMain"] .st-key-delete-action button[kind="primary"]:hover {
            background: #B91C1C !important; border-color: #B91C1C !important;
            color: #FFFFFF !important;
        }

        /* Tables, tabs, expanders, and feedback messages. */
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            border: 1px solid var(--border); border-radius: 10px; overflow: hidden;
        }
        [data-testid="stDataFrame"] * { color: var(--ink); }
        [data-testid="stTabs"] button {
            color: var(--muted) !important; font-weight: 650;
        }
        [data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--primary-dark) !important; border-bottom-color: var(--primary) !important;
        }
        [data-testid="stExpander"] {
            background: var(--surface); border: 1px solid var(--border);
            border-radius: 10px; color: var(--ink);
        }
        [data-testid="stAlert"] {
            border-radius: 9px; border: 1px solid currentColor;
        }
        [data-testid="stAlert"] p { color: var(--ink) !important; }
        [data-testid="stMain"] a { color: var(--primary-dark); }
        [data-testid="stMain"] a:hover { color: var(--primary); }

        @media (max-width: 760px) {
            [data-testid="stMain"] .block-container { padding: 1.1rem 1rem 2rem; }
            [data-testid="stMetric"] { min-height: 96px; padding: 12px; }
            [data-testid="stSidebarNav"] { padding-left: .45rem; padding-right: .45rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def style_chart(chart):
    """Set consistent chart backgrounds, fonts, grid lines, and readable hover."""
    chart.update_layout(
        template="plotly_white",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#0F172A", size=13),
        title_font=dict(color="#0F172A", size=16),
        legend=dict(font=dict(color="#334155")),
        hoverlabel=dict(
            bgcolor="#FFFFFF", bordercolor="#CBD5E1",
            font=dict(color="#0F172A", size=13),
        ),
        margin=dict(l=16, r=16, t=36, b=16),
    )
    chart.update_xaxes(
        title_font=dict(color="#334155"),
        tickfont=dict(color="#475569"),
        gridcolor="#E2E8F0",
        zerolinecolor="#CBD5E1",
    )
    chart.update_yaxes(
        title_font=dict(color="#334155"),
        tickfont=dict(color="#475569"),
        gridcolor="#E2E8F0",
        zerolinecolor="#CBD5E1",
    )
    return chart


def format_money(cents):
    """Display an integer number of cents as Pakistani rupees."""
    return format_pkr(int(cents))
