"""Business Reports for the Learning Management System."""

import streamlit as st
import pandas as pd

from connection import get_connection


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="LMS Reports",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("📊 LMS Business Reports")

st.write(
    "The following reports answer the six required business "
    "questions for the Learning Management System."
)


# ---------------------------------------------------------
# HELPER FUNCTION
# ---------------------------------------------------------

def run_query(query):
    """Run a SQL query and return the result as a DataFrame."""

    conn = None

    try:
        conn = get_connection()

        df = pd.read_sql(query, conn)

        return df

    except Exception as e:

        st.error(f"Database error: {e}")

        return pd.DataFrame()

    finally:

        if conn is not None:
            conn.close()


# ---------------------------------------------------------
# BR-01
# COURSES WITH HIGHEST ENROLLMENTS
# ---------------------------------------------------------

st.header("BR-01: Courses with Highest Enrollments")

st.write(
    "Which courses have the highest number of enrolled students?"
)

query_br01 = """
SELECT
    c.course_id,
    c.course_name,
    COUNT(e.enrollment_id) AS total_enrollments
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id = e.course_id
GROUP BY
    c.course_id,
    c.course_name
ORDER BY
    total_enrollments DESC;
"""

br01 = run_query(query_br01)

if not br01.empty:

    st.dataframe(
        br01,
        use_container_width=True,
        hide_index=True
    )

    csv = br01.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download BR-01 CSV",
        data=csv,
        file_name="courses_highest_enrollments.csv",
        mime="text/csv"
    )

else:

    st.info("No course enrollment data available.")


st.divider()


# ---------------------------------------------------------
# BR-02
# COURSES EACH INSTRUCTOR TEACHES
# ---------------------------------------------------------

st.header("BR-02: Courses Each Instructor Teaches")

st.write(
    "How many courses does each instructor teach?"
)

query_br02 = """
SELECT
    i.instructor_id,
    CONCAT(
        i.first_name,
        ' ',
        i.last_name
    ) AS instructor_name,
    COUNT(c.course_id) AS total_courses
FROM instructors i
LEFT JOIN courses c
    ON i.instructor_id = c.instructor_id
GROUP BY
    i.instructor_id,
    instructor_name
ORDER BY
    total_courses DESC;
"""

br02 = run_query(query_br02)

if not br02.empty:

    st.dataframe(
        br02,
        use_container_width=True,
        hide_index=True
    )

    csv = br02.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download BR-02 CSV",
        data=csv,
        file_name="instructor_course_workload.csv",
        mime="text/csv"
    )

else:

    st.info("No instructor/course data available.")


st.divider()


# ---------------------------------------------------------
# BR-03
# STUDENTS WITH HIGHEST TOTAL MARKS
# ---------------------------------------------------------

st.header("BR-03: Students with Highest Total Marks")

st.write(
    "Which students have the highest total marks across their courses?"
)

query_br03 = """
SELECT
    s.student_id,
    CONCAT(
        s.first_name,
        ' ',
        s.last_name
    ) AS student_name,
    SUM(g.total_marks) AS total_marks
FROM students s
INNER JOIN enrollments e
    ON s.student_id = e.student_id
INNER JOIN grades g
    ON e.enrollment_id = g.enrollment_id
GROUP BY
    s.student_id,
    student_name
ORDER BY
    total_marks DESC;
"""

br03 = run_query(query_br03)

if not br03.empty:

    br03["total_marks"] = br03["total_marks"].round(2)

    st.dataframe(
        br03,
        use_container_width=True,
        hide_index=True
    )

    csv = br03.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download BR-03 CSV",
        data=csv,
        file_name="student_highest_marks.csv",
        mime="text/csv"
    )

else:

    st.info("No student grade data available.")


st.divider()


# ---------------------------------------------------------
# BR-04
# ACTIVE STUDENTS
# ---------------------------------------------------------

st.header("BR-04: Active Students")

st.write(
    "How many students are currently active?"
)

query_br04 = """
SELECT
    COUNT(*) AS active_students
FROM students
WHERE status = 'Active';
"""

br04 = run_query(query_br04)

if not br04.empty:

    active_count = int(br04.iloc[0]["active_students"])

    st.metric(
        "✅ Active Students",
        active_count
    )

    st.dataframe(
        br04,
        use_container_width=True,
        hide_index=True
    )

    csv = br04.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download BR-04 CSV",
        data=csv,
        file_name="active_students.csv",
        mime="text/csv"
    )

else:

    st.info("No student data available.")


st.divider()


# ---------------------------------------------------------
# BR-05
# ENROLLMENT STATUS COUNTS
# ---------------------------------------------------------

st.header("BR-05: Enrollment Status Counts")

st.write(
    "How many enrollments are Enrolled, Completed, or Dropped?"
)

query_br05 = """
SELECT
    status,
    COUNT(*) AS total
FROM enrollments
GROUP BY
    status
ORDER BY
    total DESC;
"""

br05 = run_query(query_br05)

if not br05.empty:

    st.dataframe(
        br05,
        use_container_width=True,
        hide_index=True
    )

    csv = br05.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download BR-05 CSV",
        data=csv,
        file_name="enrollment_status_counts.csv",
        mime="text/csv"
    )

else:

    st.info("No enrollment data available.")


st.divider()


# ---------------------------------------------------------
# BR-06
# COURSES WITH NO STUDENTS
# ---------------------------------------------------------

st.header("BR-06: Courses with No Students")

st.write(
    "Which courses currently have no enrolled students?"
)

query_br06 = """
SELECT
    c.course_id,
    c.course_name
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id = e.course_id
WHERE e.enrollment_id IS NULL;
"""

br06 = run_query(query_br06)

if not br06.empty:

    st.dataframe(
        br06,
        use_container_width=True,
        hide_index=True
    )

    csv = br06.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download BR-06 CSV",
        data=csv,
        file_name="courses_with_no_students.csv",
        mime="text/csv"
    )

else:

    st.success(
        "All current courses have at least one enrollment."
    )


st.divider()


# ---------------------------------------------------------
# ADDITIONAL REPORT
# INSTRUCTOR WORKLOAD
# ---------------------------------------------------------

st.header("📚 Additional Report: Instructor Workload")

query_instructor = """
SELECT
    i.instructor_id,
    CONCAT(
        i.first_name,
        ' ',
        i.last_name
    ) AS instructor_name,
    COUNT(c.course_id) AS courses_teaching
FROM instructors i
LEFT JOIN courses c
    ON i.instructor_id = c.instructor_id
GROUP BY
    i.instructor_id,
    instructor_name
ORDER BY
    courses_teaching DESC;
"""

instructor_report = run_query(query_instructor)

if not instructor_report.empty:

    st.dataframe(
        instructor_report,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# ADDITIONAL REPORT
# STUDENTS PER COURSE
# ---------------------------------------------------------

st.header("👨‍🎓 Additional Report: Students per Course")

query_students_course = """
SELECT
    c.course_id,
    c.course_name,
    COUNT(e.student_id) AS total_students
FROM courses c
LEFT JOIN enrollments e
    ON c.course_id = e.course_id
GROUP BY
    c.course_id,
    c.course_name
ORDER BY
    total_students DESC;
"""

students_course_report = run_query(query_students_course)

if not students_course_report.empty:

    st.dataframe(
        students_course_report,
        use_container_width=True,
        hide_index=True
    )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "LMS Business Reports | MySQL + Python + Streamlit + Pandas"
)