import streamlit as st
import pandas as pd
from mysql.connector import Error
from connection import get_connection

st.title("📚 Courses")

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

def instructor_options():
    return fetch_df("""
        SELECT instructor_id,
               CONCAT(first_name, ' ', last_name) AS instructor_name,
               status
        FROM instructors
        ORDER BY first_name, last_name
    """)

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add", "🔎 Search / View", "✏️ Update", "🗑️ Delete"])

with tab1:
    st.subheader("Add Course")
    instructors = instructor_options()
    if instructors.empty:
        st.warning("Add an instructor first.")
    else:
        labels = {
            int(r.instructor_id): f"{r.instructor_name} (ID {int(r.instructor_id)})"
            for _, r in instructors.iterrows()
        }
        with st.form("add_course"):
            name = st.text_input("Course Name")
            description = st.text_area("Description")
            iid = st.selectbox("Instructor", list(labels), format_func=lambda x: labels[x])
            duration = st.number_input("Duration (weeks)", min_value=1, step=1)
            fee = st.number_input("Fee", min_value=0.0, step=100.0, format="%.2f")
            status = st.selectbox("Status", ["Active", "Inactive"])
            submitted = st.form_submit_button("Add Course", type="primary")
            if submitted:
                if not name.strip():
                    st.error("Course name is required.")
                else:
                    try:
                        execute("""
                            INSERT INTO courses
                            (course_name, description, instructor_id, duration, fee, status)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (name.strip(), description.strip(), iid, duration, fee, status))
                        st.success("Course added successfully.")
                        st.rerun()
                    except Error as e:
                        st.error(f"Could not add course: {e}")

with tab2:
    st.subheader("Search Courses")
    search = st.text_input("Search by course ID, name, description or instructor")
    query = """
        SELECT c.course_id, c.course_name, c.description,
               CONCAT(i.first_name, ' ', i.last_name) AS instructor,
               c.duration, c.fee, c.status
        FROM courses c
        INNER JOIN instructors i ON c.instructor_id = i.instructor_id
    """
    params = None
    if search.strip():
        query += """
            WHERE CAST(c.course_id AS CHAR) LIKE %s
               OR c.course_name LIKE %s
               OR c.description LIKE %s
               OR i.first_name LIKE %s
               OR i.last_name LIKE %s
        """
        term = f"%{search.strip()}%"
        params = (term, term, term, term, term)
    query += " ORDER BY c.course_id DESC"
    st.dataframe(fetch_df(query, params), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Update Course")
    df = fetch_df("""
        SELECT c.course_id, c.course_name, c.description, c.instructor_id,
               c.duration, c.fee, c.status
        FROM courses c ORDER BY c.course_id
    """)
    instructors = instructor_options()
    if df.empty:
        st.info("No courses available.")
    elif instructors.empty:
        st.warning("No instructors available.")
    else:
        cid = st.selectbox("Select Course ID", df["course_id"].tolist())
        row = df[df.course_id == cid].iloc[0]
        instructor_ids = [int(x) for x in instructors["instructor_id"].tolist()]
        current_iid = int(row["instructor_id"])
        if current_iid not in instructor_ids:
            instructor_ids.append(current_iid)
        labels = {
            int(r.instructor_id): f"{r.instructor_name} (ID {int(r.instructor_id)})"
            for _, r in instructors.iterrows()
        }
        if current_iid not in labels:
            labels[current_iid] = f"Instructor ID {current_iid}"
        with st.form("update_course"):
            name = st.text_input("Course Name", value=str(row["course_name"]))
            description = st.text_area("Description", value="" if pd.isna(row["description"]) else str(row["description"]))
            iid = st.selectbox("Instructor", instructor_ids,
                               index=instructor_ids.index(current_iid),
                               format_func=lambda x: labels[x])
            duration = st.number_input("Duration (weeks)", min_value=1, step=1, value=int(row["duration"]))
            fee = st.number_input("Fee", min_value=0.0, step=100.0, format="%.2f", value=float(row["fee"]))
            status = st.selectbox("Status", ["Active", "Inactive"],
                                  index=0 if row["status"] == "Active" else 1)
            submitted = st.form_submit_button("Update Course", type="primary")
            if submitted:
                if not name.strip():
                    st.error("Course name is required.")
                else:
                    try:
                        execute("""
                            UPDATE courses
                            SET course_name=%s, description=%s, instructor_id=%s,
                                duration=%s, fee=%s, status=%s
                            WHERE course_id=%s
                        """, (name.strip(), description.strip(), iid, duration, fee, status, cid))
                        st.success("Course updated successfully.")
                        st.rerun()
                    except Error as e:
                        st.error(f"Could not update course: {e}")

with tab4:
    st.subheader("Delete Course")
    st.warning("Deleting a course also deletes its enrollments and grades because of the database foreign-key rules.")
    df = fetch_df("""
        SELECT c.course_id, c.course_name,
               CONCAT(i.first_name, ' ', i.last_name) AS instructor,
               COUNT(e.enrollment_id) AS enrollment_count
        FROM courses c
        INNER JOIN instructors i ON c.instructor_id = i.instructor_id
        LEFT JOIN enrollments e ON c.course_id = e.course_id
        GROUP BY c.course_id, c.course_name, instructor
        ORDER BY c.course_id
    """)
    if df.empty:
        st.info("No courses available.")
    else:
        cid = st.selectbox("Select Course ID to delete", df["course_id"].tolist(),
                           key="delete_course_id")
        row = df[df.course_id == cid].iloc[0]
        st.write(f"Selected: **{row['course_name']}** — Enrollments: **{row['enrollment_count']}**")
        confirm = st.checkbox("I understand this deletion cannot be undone.", key="confirm_course_delete")
        if st.button("Delete Course", type="primary", disabled=not confirm):
            try:
                execute("DELETE FROM courses WHERE course_id=%s", (cid,))
                st.success("Course deleted successfully.")
                st.rerun()
            except Error as e:
                st.error(f"Could not delete course: {e}")
