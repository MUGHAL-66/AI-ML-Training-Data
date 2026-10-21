"""Sales reports; demonstration rows are always kept separate from real sales."""

from database import database_connection, initialize_database


def get_sales_analysis(db_path=None):
    """Calculate real-sales KPIs, product/category totals, and daily revenue."""
    initialize_database(db_path)
    with database_connection(db_path) as connection:
        totals = connection.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM sales WHERE status = 'completed') AS transactions,
                (SELECT COALESCE(SUM(si.quantity), 0)
                 FROM sale_items si JOIN sales s ON s.sale_id = si.sale_id
                 WHERE s.status = 'completed') AS units_sold,
                (SELECT COALESCE(SUM(total_cents), 0)
                 FROM sales WHERE status = 'completed') AS revenue_cents
            """
        ).fetchone()
        product_rows = connection.execute(
            """
            SELECT si.product_name AS name, si.product_category AS category,
                   SUM(si.quantity) AS units_sold,
                   SUM(si.line_total_cents) AS revenue_cents
            FROM sale_items si
            JOIN sales s ON s.sale_id = si.sale_id
            WHERE s.status = 'completed'
            GROUP BY si.product_name, si.product_category
            ORDER BY units_sold DESC, name COLLATE NOCASE
            """
        ).fetchall()
        category_rows = connection.execute(
            """
            SELECT si.product_category AS category,
                   SUM(si.quantity) AS units_sold,
                   SUM(si.line_total_cents) AS revenue_cents
            FROM sale_items si
            JOIN sales s ON s.sale_id = si.sale_id
            WHERE s.status = 'completed'
            GROUP BY si.product_category
            ORDER BY revenue_cents DESC
            """
        ).fetchall()
        daily_rows = connection.execute(
            """
            SELECT substr(created_at, 1, 10) AS date,
                   SUM(total_cents) AS revenue_cents
            FROM sales WHERE status = 'completed'
            GROUP BY substr(created_at, 1, 10) ORDER BY date
            """
        ).fetchall()
        sample_rows = connection.execute(
            """
            SELECT product_name AS name, category,
                   SUM(quantity) AS units_sold, SUM(revenue_cents) AS revenue_cents
            FROM sample_sale_items
            GROUP BY product_name, category
            ORDER BY units_sold DESC, name COLLATE NOCASE
            """
        ).fetchall()

    products = [dict(row) for row in product_rows]
    sample_products = [dict(row) for row in sample_rows]
    return {
        "total_units_sold": totals["units_sold"],
        "total_revenue_cents": totals["revenue_cents"],
        "completed_transactions": totals["transactions"],
        "best_selling_product": products[0]["name"] if products else None,
        "revenue_by_product": products,
        "sales_by_category": [dict(row) for row in category_rows],
        "daily_sales": [dict(row) for row in daily_rows],
        "sample_sales": sample_products,
        "sample_data_is_separate": True,
    }
