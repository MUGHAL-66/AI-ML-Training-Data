"""Reusable, database-independent input and grading validation."""
import re
from decimal import Decimal, InvalidOperation

STATUSES = {
    "student": ("Active", "Inactive", "Graduated"),
    "instructor": ("Active", "Inactive"),
    "course": ("Active", "Inactive", "Completed"),
    "enrollment": ("Enrolled", "Completed", "Dropped"),
}


def required(value, label="Value"):
    if value is None or not str(value).strip():
        raise ValueError(f"{label} is required.")
    return str(value).strip()


def split_person_name(value):
    """Split the UI's full-name field into the existing DB first/last columns."""
    parts = required(value, "Full name").split(maxsplit=1)
    if len(parts) != 2:
        raise ValueError("Enter both a first name and a last name.")
    return parts[0], parts[1]


def valid_email(value):
    value = required(value, "Email")
    if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
        raise ValueError("Enter a valid email address.")
    return value.lower()


def valid_phone(value):
    value = (value or "").strip()
    if value and not re.fullmatch(r"\+?[0-9().\-\s]{7,20}", value):
        raise ValueError("Enter a valid phone number (7–20 characters, digits and common phone symbols).")
    return value or None


def valid_duration(value):
    value = int(value)
    if value < 1:
        raise ValueError("Course duration must be at least 1 week.")
    return value


def valid_fee(value):
    try:
        amount = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValueError("Enter a valid course fee.") from exc
    if not amount.is_finite() or amount < 0:
        raise ValueError("Course fee cannot be negative.")
    return amount


def valid_status(kind, value):
    if value not in STATUSES[kind]:
        raise ValueError("Select a valid status.")
    return value


def calculate_grade(assignment, quiz, final_exam):
    vals = [Decimal(str(v)) for v in (assignment, quiz, final_exam)]
    for label, value, maximum in zip(("Assignment", "Quiz", "Final exam"), vals, (20, 20, 60)):
        if not value.is_finite() or value < 0 or value > maximum:
            raise ValueError(f"{label} marks must be between 0 and {maximum}.")
    total = sum(vals)
    band = "A" if total >= 85 else "B" if total >= 70 else "C" if total >= 55 else "D" if total >= 40 else "F"
    return total, band
