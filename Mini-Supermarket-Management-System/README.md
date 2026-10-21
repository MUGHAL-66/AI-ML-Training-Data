# Mini Supermarket Management System

A beginner-friendly supermarket point-of-sale and inventory project built with Python, SQLite, Streamlit, Pandas, and Plotly. It includes two interfaces—an independent console program and a responsive web dashboard—backed by the same product, cart, checkout, and reporting logic.

## Objectives

- Practise Python data types, variables, lists, dictionaries, loops, conditions, functions, validation, exceptions, and calculations.
- Manage a persistent product catalogue and stock with SQLite.
- Complete sales consistently, calculate discounts, preserve receipt snapshots, and analyse actual sales.
- Build and test a simple web dashboard using Streamlit and interactive Plotly charts.

## Features

- Ten starter products, inserted only when a database has no products.
- Product search, add, edit, delete, price/quantity validation, and low-stock reporting.
- Shared shopping-cart calculations and 10% discount for subtotals of Rs. 1,000.00 or more.
- Atomic checkout: stock deductions, transaction, and sale items succeed or roll back together.
- Invoice numbers, date/time, saved receipts, and sales history.
- Integer-paisa currency storage for reliable calculations and two-decimal PKR display.
- Console menu and Streamlit sections: Dashboard, Products, Inventory, New Sale / POS, Receipts / Sales History, and Analytics.
- Dashboard charts for daily revenue, best-selling products, category inventory, and category sales.
- Separate, clearly labelled sample sales. Demo rows never contribute to actual sales totals.
- Automated tests that use a temporary SQLite database and cannot modify the application database.

## Technologies

- Python 3.10 or later
- SQLite (`sqlite3`, included with Python)
- Streamlit
- Pandas
- Plotly
- `unittest` (included with Python)

## Python concepts demonstrated

- **Variables and data types:** strings, integers, `Decimal`, dictionaries, lists, and SQLite rows.
- **Conditions and loops:** menu choices, input validation, cart lines, and report generation.
- **Functions and modules:** database, product, cart, billing, and analysis responsibilities are separated.
- **Exceptions:** invalid input and checkout conflicts are reported with useful messages.
- **Data analysis:** SQL aggregation and Python report structures support revenue and best-seller metrics.
- **Persistence:** SQLite retains products, inventory, completed sales, and receipt line snapshots across restarts.

## Project structure

```text
Mini-Supermarket-Management-System/
├── app.py                     # Streamlit dashboard
├── main.py                    # Independent console program
├── database.py                # Schema, starter products, demo-only data
├── products.py                # Product and inventory operations
├── cart.py                    # Cart validation and exact money calculations
├── billing.py                 # Transactional checkout and receipt queries
├── sales_analysis.py          # Actual-sales reporting
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── .gitkeep               # Local database is created here on first run
├── pages/
│   ├── 1_Products.py
│   ├── 2_Inventory.py
│   ├── 3_New_Sale.py
│   ├── 4_Sales_History.py
│   └── 5_Analytics.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── tests/
    └── test_supermarket.py
```

## Setup in VS Code on Windows

1. Install Python 3.10+ and VS Code's Python extension.
2. Open the project folder in VS Code and open **Terminal → New Terminal** (PowerShell).
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use the VS Code interpreter picker to select `.venv\Scripts\python.exe`, or run `.venv\Scripts\python.exe` directly in the commands below.

4. Install the web-interface dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. In VS Code, select the `.venv` interpreter (`Ctrl+Shift+P` → **Python: Select Interpreter**).

SQLite is part of Python; no database server or separate database package is required.

## Run the console application

From the project folder with the virtual environment active:

```powershell
python main.py
```

The console interface uses options 1–9 and works independently of Streamlit.

## Run the Streamlit application

```powershell
python -m streamlit run app.py
```

Streamlit opens the dashboard in your browser. Use the sidebar to open the Products, Inventory, New Sale, Sales History, and Analytics sections.

## Run tests and compilation checks

```powershell
python -m unittest discover -s tests -v
python -m compileall -q .
```

Tests create a fresh temporary database for each test. They do not alter the local application database.

## Example billing output

```text
Mini Supermarket
Invoice: INV-20261019-XXXXXXXX
Date: 2026-10-19T18:29:27+05:00
Milk  3 x PKR 180.00 = PKR 540.00
Rice  2 x PKR 320.00 = PKR 640.00
Subtotal: PKR 1,180.00
Discount (10%): -PKR 118.00
Final payable: PKR 1,062.00
Thank you for shopping with us!
```

Invoice IDs and time are generated at the time of checkout.

## Example sales analysis output

```text
SALES ANALYSIS (actual completed transactions only)
Completed transactions: 1
Units sold: 5
Revenue: PKR 1,062.00
Best seller: Milk
```

Revenue reflects the final paid receipt total. Product/category sales charts use saved line-item totals before receipt-level discount.

## Screenshots

Screenshots can be added here after running the dashboard:

- `screenshots/dashboard.png` — dashboard and KPI cards
- `screenshots/point-of-sale.png` — cart and printable receipt
- `screenshots/products.png` — product management

## Local database and Git

The default database is `data\supermarket.db`. `.gitignore` excludes SQLite database files because inventory and customer sales change locally and may contain business/customer records. The tracked `data\.gitkeep` preserves the empty folder. Back up `data\supermarket.db` separately if you need to preserve the live database.

To use another database without changing code, set an environment variable in PowerShell before launching either interface:

```powershell
$env:SUPERMARKET_DB_PATH = "C:\path\to\my-supermarket.db"
python main.py
```

Use the same value for Streamlit if both interfaces should share that alternate database.

## Limitations and future improvements

- This is a local, single-store demonstration; it has no logins, roles, or multi-user synchronization.
- Tax, refunds, supplier purchasing, and export-to-PDF are not included.
- Product IDs are entered by the manager and must be unique.
- A future version could add role-based access, barcode scanning, supplier/restock workflows, database backups, and PDF receipt export.
