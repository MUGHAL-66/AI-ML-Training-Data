"""Environment-backed configuration for the LMS."""
import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / ".env"
# Use the project's .env regardless of the shell's current directory. Existing
# process environment variables retain precedence, which is useful for hosting.
load_dotenv(dotenv_path=ENV_FILE, override=False)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "lms_database"),
    "connection_timeout": 5,
}


def safe_connection_settings():
    """Return non-secret connection settings suitable for diagnostic output."""
    return {key: DB_CONFIG[key] for key in ("host", "port", "user", "database")}
