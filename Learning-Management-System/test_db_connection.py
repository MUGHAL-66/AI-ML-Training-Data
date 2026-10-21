"""Read-only connection and schema diagnostic; safe to run from any directory."""
import sys
from pathlib import Path

# Make project imports resolve even when invoked outside the repository root.
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import safe_connection_settings  # noqa: E402
from db import DatabaseError, diagnose_connection, inspect_database_schema  # noqa: E402


def main():
    settings = safe_connection_settings()
    print("MySQL LMS connection diagnostic (password is never displayed)")
    print(f"Host: {settings['host']}  Port: {settings['port']}")
    print(f"User: {settings['user']}  Database: {settings['database']}")
    try:
        schema = inspect_database_schema()
        for table, columns in schema["tables"].items():
            description = ", ".join(
                column["name"] + (" (generated)" if "GENERATED" in column["extra"].upper() else "")
                for column in columns
            )
            print(f"{table}: {description}")
        if schema["missing_tables"]:
            print("Missing tables: " + ", ".join(schema["missing_tables"]))
        diagnose_connection()
    except DatabaseError as exc:
        print(f"FAILED: {exc}")
        return 1
    print("SUCCESS: connected and verified all five LMS tables and required columns.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
