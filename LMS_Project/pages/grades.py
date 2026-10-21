import streamlit as st
import pandas as pd
from mysql.connector import Error
from connection import get_connection

st.title("📊 Grades")

def fetch_df(query, params=None):
    conn = None
    try:
        conn = get_connection()
        return pd.read_sql(query, conn, params=params)
    finally:
        if conn:
            conn.close()

def execute(query, params=None):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, params or ())
        conn.commit()
        return cur.lastrowid
    finally:
        if conn:
            conn.close()

def validate_marks(a, q, f):
    return 0 <= a <= 100 and 0 <= q <= 100 and 0 <= f <= 100

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add", "🔎 Search / View", "✏️ Update", "🗑️ Delete"])

with tab1:
    st.subheader("Add Grade")
    enrollments = fetch_df("""
        SELECT e.enrollment_id,
               CONCAT(s.first_name, ' ', s.last_name) AS student,
               c.course_name
        FROM enrollments e
        INNER JOIN students s ON e.student_id=s.student_id
        INNER JOIN courses c ON e.course_id=c.course_id
        LEFT JOIN grades g ON e.enrollment_id=g.enrollment_id
        WHERE g.grade_id IS NULL
        ORDER BY e.enrollment_id
    """)
    if enrollments.empty:
        st.info("All enrollments already have grades, or there are no enrollments.")
    else:
        labels = {
            int(r.enrollment_id): f"Enrollment {int(r.enrollment_id)} — {r.student} — {r.course_name}"
            for _, r in enrollments.iterrows()
        }
        with st.form("add_grade"):
            eid = st.selectbox("Enrollment", list(labels), format_func=lambda x: labels[x])
            c1, c2, c3 = st.columns(3)
            assignment = c1.number_input("Assignment Marks", min_value=0.0, max_value=100.0, step=1.0)
            quiz = c2.number_input("Quiz Marks", min_value=0.0, max_value=100.0, step=1.0)
            final_exam = c3.number_input("Final Exam Marks", min_value=0.0, max_value=100.0, step=1.0)
            st.caption("Total Marks = Assignment + Quiz + Final Exam")
            submitted = st.form_submit_button("Add Grade", type="primary")
            if submitted:
                if not validate_marks(assignment, quiz, final_exam):
                    st.error("Each mark must be between 0 and 100.")
                else:
                    try:
                        execute("""
                            INSERT INTO grades
                            (enrollment_id, assignment_marks, quiz_marks, final_exam_marks)
                            VALUES (%s, %s, %s, %s)
                        """, (eid, assignment, quiz, final_exam))
                        st.success("Grade added successfully.")
                        st.rerun()
                    except Error as e:
                        st.error(f"Could not add grade: {e}")

with tab2:
    st.subheader("Search / View Grades")
    search = st.text_input("Search by grade ID, enrollment ID, student or course")
    query = """
        SELECT g.grade_id, g.enrollment_id,
               CONCAT(s.first_name, ' ', s.last_name) AS student,
               c.course_name,
               g.assignment_marks,
               g.quiz_marks,
               g.final_exam_marks,
               g.total_marks
        FROM grades g
        INNER JOIN enrollments e ON g.enrollment_id=e.enrollment_id
        INNER JOIN students s ON e.student_id=s.student_id
        INNER JOIN courses c ON e.course_id=c.course_id
    """
    params = None
    if search.strip():
        query += """
            WHERE CAST(g.grade_id AS CHAR) LIKE %s
               OR CAST(g.enrollment_id AS CHAR) LIKE %s
               OR s.first_name LIKE %s
               OR s.last_name LIKE %s
               OR c.course_name LIKE %s
        """
        term = f"%{search.strip()}%"
        params = (term, term, term, term, term)
    query += " ORDER BY g.grade_id DESC"
    st.dataframe(fetch_df(query, params), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Update Grade")
    df = fetch_df("""
        SELECT g.grade_id, g.enrollment_id,
               CONCAT(s.first_name, ' ', s.last_name) AS student,
               c.course_name,
               g.assignment_marks, g.quiz_marks, g.final_exam_marks
        FROM grades g
        INNER JOIN enrollments e ON g.enrollment_id=e.enrollment_id
        INNER JOIN students s ON e.student_id=s.student_id
        INNER JOIN courses c ON e.course_id=c.course_id
        ORDER BY g.grade_id
    """)
    if df.empty:
        st.info("No grades available.")
    else:
        gid = st.selectbox("Select Grade ID", df["grade_id"].tolist())
        row = df[df.grade_id == gid].iloc[0]
        st.write(f"Student: **{row['student']}** | Course: **{row['course_name']}**")
        with st.form("update_grade"):
            c1, c2, c3 = st.columns(3)
            assignment = c1.number_input("Assignment Marks", min_value=0.0, max_value=100.0, step=1.0, value=float(row["assignment_marks"]))
            quiz = c2.number_input("Quiz Marks", min_value=0.0, max_value=100.0, step=1.0, value=float(row["quiz_marks"]))
            final_exam = c3.number_input("Final Exam Marks", min_value=0.0, max_value=100.0, step=1.0, value=float(row["final_exam_marks"]))
            submitted = st.form_submit_button("Update Grade", type="primary")
            if submitted:
                if not validate_marks(assignment, quiz, final_exam):
                    st.error("Each mark must be between 0 and 100.")
                else:
                    try:
                        execute("""
                            UPDATE grades
                            SET assignment_marks=%s, quiz_marks=%s, final_exam_marks=%s
                            WHERE grade_id=%s
                        """, (assignment, quiz, final_exam, gid))
                        st.success("Grade updated successfully.")
                        st.rerun()
                    except Error as e:
                        st.error(f"Could not update grade: {e}")

with tab4:
    st.subheader("Delete Grade")
    df = fetch_df("""
        SELECT g.grade_id,
               CONCAT(s.first_name, ' ', s.last_name) AS student,
               c.course_name,
               g.total_marks
        FROM grades g
        INNER JOIN enrollments e ON g.enrollment_id=e.enrollment_id
        INNER JOIN students s ON e.student_id=s.student_id
        INNER JOIN courses c ON e.course_id=c.course_id
        ORDER BY g.grade_id
    """)
    if df.empty:
        st.info("No grades available.")
    else:
        gid = st.selectbox("Select Grade ID to delete", df["grade_id"].tolist(),
                           key="delete_grade_id")
        row = df[df.grade_id == gid].iloc[0]
        st.write(f"Selected: **{row['student']}** — **{row['course_name']}** — Total: **{row['total_marks']}**")
        confirm = st.checkbox("I understand this deletion cannot be undone.", key="confirm_grade_delete")
        if st.button("Delete Grade", type="primary", disabled=not confirm):
            try:
                execute("DELETE FROM grades WHERE grade_id=%s", (gid,))
                st.success("Grade deleted successfully.")
                st.rerun()
            except Error as e:
                st.error(f"Could not delete grade: {e}")
