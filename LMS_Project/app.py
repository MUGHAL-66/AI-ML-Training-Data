"""Entry point for the Learning Management System."""

import streamlit as st
import pandas as pd
import plotly.express as px

from connection import get_connection


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="LMS Management System",
    page_icon="🎓",
    layout="wide"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🎓 Learning Management System")
st.subheader("Management Dashboard")

st.write(
    "This dashboard provides an overview of students, instructors, "
    "courses, enrollments, and student performance."
)


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

try:
    conn = get_connection()

    # Students
    students = pd.read_sql(
        """
        SELECT *
        FROM students
        """,
        conn
    )

    # Instructors
    instructors = pd.read_sql(
        """
        SELECT *
        FROM instructors
        """,
        conn
    )

    # Courses
    courses = pd.read_sql(
        """
        SELECT *
        FROM courses
        """,
        conn
    )

    # Enrollments
    enrollments = pd.read_sql(
        """
        SELECT *
        FROM enrollments
        """,
        conn
    )

    # Grades
    grades = pd.read_sql(
        """
        SELECT *
        FROM grades
        """,
        conn
    )

    conn.close()

except Exception as e:

    st.error("Unable to connect to the database.")

    st.error(str(e))

    st.stop()


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

total_students = len(students)

active_students = len(
    students[students["status"] == "Active"]
)

total_instructors = len(instructors)

total_courses = len(courses)

total_enrollments = len(enrollments)

completed_enrollments = len(
    enrollments[enrollments["status"] == "Completed"]
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

st.markdown("## 📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "👨‍🎓 Total Students",
    total_students
)

col2.metric(
    "✅ Active Students",
    active_students
)

col3.metric(
    "👨‍🏫 Total Instructors",
    total_instructors
)


col4, col5, col6 = st.columns(3)

col4.metric(
    "📚 Total Courses",
    total_courses
)

col5.metric(
    "📝 Total Enrollments",
    total_enrollments
)

col6.metric(
    "🎓 Completed Enrollments",
    completed_enrollments
)


# ---------------------------------------------------------
# DIVIDER
# ---------------------------------------------------------

st.divider()


# ---------------------------------------------------------
# ENROLLMENT STATUS CHART
# ---------------------------------------------------------

st.markdown("## 📌 Enrollment Status")

if not enrollments.empty:

    status_data = (
        enrollments
        .groupby("status")
        .size()
        .reset_index(name="total")
    )

    fig_status = px.pie(
        status_data,
        names="status",
        values="total",
        title="Enrollment Status Distribution"
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )

else:

    st.info("No enrollment data available.")


# ---------------------------------------------------------
# COURSE POPULARITY
# ---------------------------------------------------------

st.markdown("## 📚 Course Popularity")

try:

    conn = get_connection()

    course_popularity = pd.read_sql(
        """
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
            total_enrollments DESC
        """,
        conn
    )

    conn.close()

    if not course_popularity.empty:

        fig_courses = px.bar(
            course_popularity,
            x="course_name",
            y="total_enrollments",
            title="Number of Students Enrolled in Each Course",
            labels={
                "course_name": "Course",
                "total_enrollments": "Enrollments"
            }
        )

        st.plotly_chart(
            fig_courses,
            use_container_width=True
        )

        st.dataframe(
            course_popularity,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No course enrollment data available.")

except Exception as e:

    st.error(f"Could not load course popularity data: {e}")


# ---------------------------------------------------------
# STUDENT PERFORMANCE
# ---------------------------------------------------------

st.markdown("## 🏆 Student Performance")

try:

    conn = get_connection()

    student_performance = pd.read_sql(
        """
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
            total_marks DESC
        """,
        conn
    )

    conn.close()

    if not student_performance.empty:

        st.dataframe(
            student_performance,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No student performance data available.")

except Exception as e:

    st.error(f"Could not load student performance data: {e}")


# ---------------------------------------------------------
# RECENT STUDENTS
# ---------------------------------------------------------

st.markdown("## 👨‍🎓 Students")

if not students.empty:

    recent_students = students.sort_values(
        by="student_id",
        ascending=False
    ).head(10)

    st.dataframe(
        recent_students,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No students found.")


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Learning Management System | MySQL + Python + Streamlit + Pandas"
)