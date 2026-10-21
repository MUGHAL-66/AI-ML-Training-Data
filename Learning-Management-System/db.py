"""Small, transaction-safe MySQL access layer. All values are bound parameters."""
from contextlib import contextmanager
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

REQUIRED_COLUMNS = {
    "students": {"student_id", "first_name", "last_name", "email", "phone", "enrollment_date", "status"},
    "instructors": {"instructor_id", "first_name", "last_name", "email", "specialization", "status"},
    "courses": {"course_id", "course_name", "description", "instructor_id", "duration", "fee", "status"},
    "enrollments": {"enrollment_id", "student_id", "course_id", "enrollment_date", "status"},
    "grades": {"grade_id", "enrollment_id", "assignment_marks", "quiz_marks", "final_exam_marks", "total_marks"},
}


def safe_mysql_message(exc):
    """Map connector errors to actionable categories without including server text."""
    code = getattr(exc, "errno", None)
    messages = {
        1045: "MySQL authentication failed. Match DB_USER and DB_PASSWORD to the Workbench connection.",
        1698: "MySQL rejected this account's authentication method. Match DB_USER and use the account's configured authentication method.",
        2002: "MySQL connection was refused or its local socket/pipe is unavailable. Check that the MySQL service is running and DB_HOST/DB_PORT match Workbench.",
        2003: "MySQL connection was refused. Check that the MySQL service is running and DB_HOST/DB_PORT match Workbench.",
        2005: "MySQL host could not be resolved. Check DB_HOST against the Workbench connection.",
        1049: "The configured MySQL database does not exist or is not accessible. Match DB_NAME to the Workbench schema.",
        1146: "A required table is missing from the configured database. Select the intended schema and check its table names.",
        1054: "A required column is missing. The selected database schema does not match the LMS columns.",
        2006: "The MySQL server disconnected during the request. Check that the server is running, then retry.",
        2013: "The MySQL connection was lost during the request. Check the server and network, then retry.",
        1062: "That email or record already exists. Choose a different value.",
        1451: "This record is still used by related records. Remove or reassign those records first.",
        1452: "The selected related record no longer exists. Refresh and choose a valid record.",
        3819: "One or more values are outside the allowed range. Review the field limits.",
    }
    return messages.get(code, "The database operation could not be completed. Check the connection and schema settings.")


class DatabaseError(RuntimeError):
    """Safe, user-displayable database operation failure."""


def connect():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as exc:
        raise DatabaseError(safe_mysql_message(exc)) from exc


def inspect_database_schema(connection=None):
    """Return read-only table/column metadata for the five LMS tables."""
    owns_connection = connection is None
    conn = connection or connect()
    cur = None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SHOW TABLES")
        table_key = cur.description[0][0]
        tables = {row[table_key] for row in cur.fetchall()}
        report = {"missing_tables": sorted(set(REQUIRED_COLUMNS) - tables), "tables": {}}
        for table in REQUIRED_COLUMNS.keys() & tables:
            # Identifiers come only from the fixed allowlist above, never user input.
            cur.execute(f"SHOW COLUMNS FROM `{table}`")
            report["tables"][table] = [
                {"name": row["Field"], "extra": row.get("Extra") or ""}
                for row in cur.fetchall()
            ]
        return report
    except Error as exc:
        raise DatabaseError(safe_mysql_message(exc)) from exc
    finally:
        if cur:
            cur.close()
        if owns_connection and conn.is_connected():
            conn.close()


def validate_database_schema(connection=None):
    """Check required columns against read-only metadata from the selected DB."""
    owns_connection = connection is None
    conn = connection or connect()
    try:
        report = inspect_database_schema(conn)
        issues = []
        if report["missing_tables"]:
            issues.append("Missing tables: " + ", ".join(report["missing_tables"]))
        for table, required in REQUIRED_COLUMNS.items():
            columns = report["tables"].get(table)
            if columns is None:
                continue
            actual = {column["name"] for column in columns}
            missing_columns = sorted(required - actual)
            if missing_columns:
                issues.append(f"{table} missing columns: " + ", ".join(missing_columns))
            if table == "grades" and "total_marks" in actual:
                total = next(column for column in columns if column["name"] == "total_marks")
                if "GENERATED" not in total["extra"].upper():
                    issues.append("grades.total_marks is not a generated column")
        if issues:
            raise DatabaseError("Schema check failed: " + "; ".join(issues) + ".")
        return True
    finally:
        if owns_connection and conn.is_connected():
            conn.close()


def diagnose_connection():
    """Open a connection and validate the expected LMS schema, without writes."""
    conn = connect()
    try:
        validate_database_schema(conn)
        return True
    finally:
        if conn.is_connected():
            conn.close()


@contextmanager
def cursor(dictionary=True, commit=False):
    conn = None
    cur = None
    try:
        conn = connect()
        cur = conn.cursor(dictionary=dictionary)
        yield cur
        if commit:
            conn.commit()
    except DatabaseError:
        raise
    except Error as exc:
        if conn:
            conn.rollback()
        raise DatabaseError(safe_mysql_message(exc)) from exc
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cur:
            cur.close()
        if conn and conn.is_connected():
            conn.close()


def query(sql, params=()):
    with cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def one(sql, params=()):
    with cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def execute(sql, params=()):
    with cursor(commit=True) as cur:
        cur.execute(sql, params)
        return cur.lastrowid
