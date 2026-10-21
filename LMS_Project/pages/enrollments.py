import streamlit as st
import pandas as pd
from mysql.connector import Error
from connection import get_connection

st.title("📝 Enrollments")

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

def students():
    return fetch_df("""
        SELECT student_id,
               CONCAT(first_name, ' ', last_name) AS student_name,
               email
        FROM students
        WHERE status='Active'
        ORDER BY first_name, last_name
    """)

def courses():
    return fetch_df("""
        SELECT course_id, course_name, status
        FROM courses
        WHERE status='Active'
        ORDER BY course_name
    """)

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add", "🔎 Search / View", "✏️ Update", "🗑️ Delete"])

with tab1:
    st.subheader("Enroll Student")
    s = students()
    c = courses()
    if s.empty:
        st.warning("No active students available.")
    elif c.empty:
        st.warning("No active courses available.")
    else:
        student_labels = {int(r.student_id): f"{r.student_name} — {r.email}" for _, r in s.iterrows()}
        course_labels = {int(r.course_id): f"{r.course_name} (ID {int(r.course_id)})" for _, r in c.iterrows()}
        with st.form("add_enrollment"):
            sid = st.selectbox("Student", list(student_labels), format_func=lambda x: student_labels[x])
            cid = st.selectbox("Course", list(course_labels), format_func=lambda x: course_labels[x])
            enrollment_date = st.date_input("Enrollment Date")
            status = st.selectbox("Status", ["Enrolled", "Completed", "Dropped"])
            submitted = st.form_submit_button("Create Enrollment", type="primary")
            if submitted:
                try:
                    execute("""
                        INSERT INTO enrollments
                        (student_id, course_id, enrollment_date, status)
                        VALUES (%s, %s, %s, %s)
                    """, (sid, cid, enrollment_date, status))
                    st.success("Enrollment created successfully.")
                    st.rerun()
                except Error as e:
                    if "Duplicate entry" in str(e):
                        st.error("This student is already enrolled in this course.")
                    else:
                        st.error(f"Could not create enrollment: {e}")

with tab2:
    st.subheader("Search / View Enrollments")
    search = st.text_input("Search by enrollment ID, student, course or status")
    query = """
        SELECT e.enrollment_id,
               CONCAT(s.first_name, ' ', s.last_name) AS student,
               c.course_name,
               e.enrollment_date,
               e.status
        FROM enrollments e
        INNER JOIN students s ON e.student_id = s.student_id
        INNER JOIN courses c ON e.course_id = c.course_id
    """
    params = None
    if search.strip():
        query += """
            WHERE CAST(e.enrollment_id AS CHAR) LIKE %s
               OR s.first_name LIKE %s
               OR s.last_name LIKE %s
               OR c.course_name LIKE %s
               OR e.status LIKE %s
        """
        term = f"%{search.strip()}%"
        params = (term, term, term, term, term)
    query += " ORDER BY e.enrollment_id DESC"
    st.dataframe(fetch_df(query, params), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Update Enrollment")
    df = fetch_df("""
        SELECT e.enrollment_id, e.student_id, e.course_id,
               e.enrollment_date, e.status,
               CONCAT(s.first_name, ' ', s.last_name) AS student,
               c.course_name
        FROM enrollments e
        INNER JOIN students s ON e.student_id=s.student_id
        INNER JOIN courses c ON e.course_id=c.course_id
        ORDER BY e.enrollment_id
    """)
    if df.empty:
        st.info("No enrollments available.")
    else:
        eid = st.selectbox("Select Enrollment ID", df["enrollment_id"].tolist())
        row = df[df.enrollment_id == eid].iloc[0]
        with st.form("update_enrollment"):
            st.write(f"Student: **{row['student']}**")
            st.write(f"Course: **{row['course_name']}**")
            enrollment_date = st.date_input(
                "Enrollment Date",
                value=pd.to_datetime(row["enrollment_date"]).date()
            )
            status = st.selectbox(
                "Status",
                ["Enrolled", "Completed", "Dropped"],
                index=["Enrolled", "Completed", "Dropped"].index(row["status"])
            )
            submitted = st.form_submit_button("Update Enrollment", type="primary")
            if submitted:
                try:
                    execute("""
                        UPDATE enrollments
                        SET enrollment_date=%s, status=%s
                        WHERE enrollment_id=%s
                    """, (enrollment_date, status, eid))
                    st.success("Enrollment updated successfully.")
                    st.rerun()
                except Error as e:
                    st.error(f"Could not update enrollment: {e}")

with tab4:
    st.subheader("Delete Enrollment")
    st.warning("Deleting an enrollment also deletes its grade record.")
    df = fetch_df("""
        SELECT e.enrollment_id,
               CONCAT(s.first_name, ' ', s.last_name) AS student,
               c.course_name
        FROM enrollments e
        INNER JOIN students s ON e.student_id=s.student_id
        INNER JOIN courses c ON e.course_id=c.course_id
        ORDER BY e.enrollment_id
    """)
    if df.empty:
        st.info("No enrollments available.")
    else:
        eid = st.selectbox("Select Enrollment ID to delete", df["enrollment_id"].tolist(),
                           key="delete_enrollment_id")
        row = df[df.enrollment_id == eid].iloc[0]
        st.write(f"Selected: **{row['student']}** → **{row['course_name']}**")
        confirm = st.checkbox("I understand this deletion cannot be undone.", key="confirm_enrollment_delete")
        if st.button("Delete Enrollment", type="primary", disabled=not confirm):
            try:
                execute("DELETE FROM enrollments WHERE enrollment_id=%s", (eid,))
                st.success("Enrollment deleted successfully.")
                st.rerun()
            except Error as e:
                st.error(f"Could not delete enrollment: {e}")
