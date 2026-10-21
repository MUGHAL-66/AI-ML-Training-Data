# Learning Management System (MySQL + Python + Streamlit)

## Setup
1. Install MySQL 8+ and Python 3.9+.
2. `pip install -r requirements.txt`
3. Create the database: `mysql -u root -p < lms_database.sql`
4. Set credentials (defaults: localhost / root / empty password / lms_db):
   - Linux/macOS: `export DB_USER=root DB_PASSWORD=yourpass`
   - Windows PowerShell: `$env:DB_USER="root"; $env:DB_PASSWORD="yourpass"`
5. Run: `streamlit run app.py`

## Files
- `lms_database.sql` – schema, constraints, sample data
- `lms_reports.sql` – BR-01 to BR-06 queries
- `app.py` – Streamlit app with MySQL connection and CRUD (parameterized queries)

## Design notes
- UNIQUE email (students, instructors); UNIQUE(student_id, course_id) blocks duplicate enrollments.
- ENUM columns control statuses; CHECK constraints bound marks (30/20/50) and fees.
- `grades.total_marks` is a generated column; grade letters are calculated in SQL.
- Deleting a record still referenced elsewhere is refused with a clear message; grades cascade with their enrollment.

## Screenshots
Add screenshots of each page here after running the app.
