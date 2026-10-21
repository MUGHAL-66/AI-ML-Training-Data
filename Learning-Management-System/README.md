# Learning Management System

A Streamlit application for maintaining students, instructors, courses, enrollments, and grades, with live academic operations reporting backed by MySQL 8+.

## Business problem and objectives

Small academic teams often track course assignments and student results across separate spreadsheets. This application centralizes those records, validates relationships, prevents duplicate enrollment, and provides current workload, participation, and grade summaries.

## Stack and features

Python 3.10+, Streamlit, MySQL 8+, Pandas, Plotly, `mysql-connector-python`, `python-dotenv`, and pytest. Features include CRUD for all five core entities, grade entry with component limits and derived total, live dashboard, six business reports, searchable tables, CSV report export, and safe relationship constraints.

## Architecture

`app.py` defines the shared light theme and navigation. `pages/` contains the dashboard and six work areas. `services/` contains entity and report queries. `db.py` owns short-lived connections, parameterized execution, transaction handling, and read-only schema diagnostics. `config.py` loads `.env` from the directory containing the project files, even when Streamlit or the test command starts from another working directory. `utils/` contains validation and shared UI helpers. Tests for pure calculations and query binding do not require a live database.

## Database schema

`students` and `instructors` store `first_name` and `last_name`. Courses store the course length in `duration`. Courses reference instructors. Enrollments associate a student with a course and have a unique `(student_id, course_id)` pair. Grades have a unique enrollment reference; `total_marks` is a generated database column derived from assignment (0–20), quiz (0–20), and final exam (0–60) marks. Foreign keys prevent deleting referenced students, instructors, or courses; deleting an enrollment cascades to its grade. The application formats first/last names for display and writes only the component marks, preserving the existing generated total.

## Prerequisites

- Windows with Python 3.10 or newer and MySQL Server 8.0 or newer.
- MySQL Workbench (or another MySQL client) to import the schema.
- The MySQL server running locally or reachable at the host in `.env`.

## Setup with MySQL Workbench

1. Open `lms_database.sql` in Workbench and connect to the intended MySQL server.
2. Since your database and sample data already exist, do not re-import the initialization script as part of connection troubleshooting. The script is provided for a fresh development setup; its upserts can update the matching sample records.
3. Your Workbench connection currently reports host `localhost`, port `3306`, and user `root`; it has no default schema selected. The application selects `lms_database` using `DB_NAME`. Match those values to the Workbench connection you actually use. The Workbench password is not copied or read by this application.
4. In the project folder, copy the example environment file and edit the local copy with your own connection settings:

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

   Set `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, and `DB_NAME`. For the Workbench connection inspected on this machine, use `localhost`, `3306`, `root`, and `lms_database`; enter your own password. `.env` is loaded from the project root and ignored by Git. No password is included in the application or printed by diagnostics.

5. Run the read-only connection/schema check from the project root:

   ```powershell
   .\.venv\Scripts\python.exe test_db_connection.py
   ```

   The diagnostic distinguishes authentication failure, refused connections, an unknown database, missing tables, and mismatched required columns. It also verifies that `grades.total_marks` remains generated. It does not create, update, or delete database objects or rows.

## Run in Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python test_db_connection.py
streamlit run app.py
```

If PowerShell blocks activation, use `Set-ExecutionPolicy -Scope Process RemoteSigned` in that PowerShell window, then activate again. An alternative that avoids activation is `.\.venv\Scripts\python.exe -m streamlit run app.py`.

## Tests

```powershell
python -m pytest -q
```

The suite covers email and input validation, grade ranges/boundaries, parameter binding, and insert ID handling without requiring MySQL. To test integration with a separate database, configure a dedicated test schema and add explicit integration tests; the included suite never drops or modifies any database.

## SQL concepts demonstrated

| Concept | Location |
| --- | --- |
| CREATE DATABASE/TABLE, PK, FK, UNIQUE, NOT NULL, checks, controlled statuses | `lms_database.sql` |
| INSERT and idempotent sample upserts | `lms_database.sql` |
| SELECT, WHERE, LIKE, ORDER BY, parameterized updates/deletes | `services/student_service.py` and entity services |
| INNER JOIN and LEFT JOIN, aliases, calculated fields | `services/report_service.py`, entity services |
| COUNT, SUM/AVG, GROUP BY | Dashboard and report queries in `services/report_service.py` |

## Required business reports

Reports provides: BR-01 course popularity (current and historical enrollment), BR-02 instructor workload including zero-course instructors, BR-03 student averages across recorded grades, BR-04 active-student count, BR-05 enrollment status distribution, and BR-06 courses with no enrollment history. Tables are queried on page load and support CSV download.

## Troubleshooting

- **Connection refused / cannot connect:** verify MySQL Server is running, `DB_HOST` and `DB_PORT` are correct, and the server accepts local TCP connections.
- **Access denied:** check `DB_USER` and `DB_PASSWORD` in `.env`. This project never changes account passwords.
- **Unknown database/table:** confirm `DB_NAME=lms_database` and use the read-only diagnostic. The connection diagnostic does not execute the SQL initialization script.
- **Duplicate email or record:** email addresses and course names are unique; choose another value.
- **Cannot delete a record:** a related course or enrollment refers to it. Reassign/remove those relationships first.
- **Python/Streamlit command missing:** activate `.venv` and install `requirements.txt`.

## Limitations and future work

This academic project has no authentication or role-based access, pagination, or production migration framework. Future work could add sign-in, audit trails, pagination, configurable grading, and a managed deployment setup.
