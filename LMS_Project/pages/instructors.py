import streamlit as st
import pandas as pd
from mysql.connector import Error
from connection import get_connection

st.title("👨‍🏫 Instructors")

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

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add", "🔎 Search / View", "✏️ Update", "🗑️ Delete"])

with tab1:
    st.subheader("Add Instructor")
    with st.form("add_instructor"):
        c1, c2 = st.columns(2)
        first = c1.text_input("First Name")
        last = c2.text_input("Last Name")
        specialization = c1.text_input("Specialization")
        email = c2.text_input("Email")
        status = c1.selectbox("Status", ["Active", "Inactive"])
        submitted = st.form_submit_button("Add Instructor", type="primary")
        if submitted:
            if not first.strip() or not last.strip() or not specialization.strip() or not email.strip():
                st.error("All required fields must be filled.")
            elif "@" not in email or "." not in email:
                st.error("Please enter a valid email.")
            else:
                try:
                    execute("""
                        INSERT INTO instructors
                        (first_name, last_name, specialization, email, status)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (first.strip(), last.strip(), specialization.strip(), email.strip(), status))
                    st.success("Instructor added successfully.")
                    st.rerun()
                except Error as e:
                    st.error(f"Could not add instructor: {e}")

with tab2:
    st.subheader("Search Instructors")
    search = st.text_input("Search by ID, name, specialization or email")
    query = """
        SELECT instructor_id, first_name, last_name, specialization, email, status
        FROM instructors
    """
    params = None
    if search.strip():
        query += """
            WHERE CAST(instructor_id AS CHAR) LIKE %s
               OR first_name LIKE %s
               OR last_name LIKE %s
               OR specialization LIKE %s
               OR email LIKE %s
        """
        term = f"%{search.strip()}%"
        params = (term, term, term, term, term)
    query += " ORDER BY instructor_id DESC"
    st.dataframe(fetch_df(query, params), use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Update Instructor")
    df = fetch_df("""
        SELECT instructor_id, first_name, last_name, specialization, email, status
        FROM instructors ORDER BY instructor_id
    """)
    if df.empty:
        st.info("No instructors available.")
    else:
        iid = st.selectbox("Select Instructor ID", df["instructor_id"].tolist())
        row = df[df.instructor_id == iid].iloc[0]
        with st.form("update_instructor"):
            c1, c2 = st.columns(2)
            first = c1.text_input("First Name", value=str(row["first_name"]))
            last = c2.text_input("Last Name", value=str(row["last_name"]))
            specialization = c1.text_input("Specialization", value=str(row["specialization"]))
            email = c2.text_input("Email", value=str(row["email"]))
            status = c1.selectbox("Status", ["Active", "Inactive"],
                                  index=0 if row["status"] == "Active" else 1)
            submitted = st.form_submit_button("Update Instructor", type="primary")
            if submitted:
                if not first.strip() or not last.strip() or not specialization.strip() or not email.strip():
                    st.error("All required fields must be filled.")
                else:
                    try:
                        execute("""
                            UPDATE instructors
                            SET first_name=%s, last_name=%s, specialization=%s,
                                email=%s, status=%s
                            WHERE instructor_id=%s
                        """, (first.strip(), last.strip(), specialization.strip(),
                              email.strip(), status, iid))
                        st.success("Instructor updated successfully.")
                        st.rerun()
                    except Error as e:
                        st.error(f"Could not update instructor: {e}")

with tab4:
    st.subheader("Delete Instructor")
    st.warning("An instructor cannot be deleted while a course still references them.")
    df = fetch_df("""
        SELECT i.instructor_id,
               CONCAT(i.first_name, ' ', i.last_name) AS instructor_name,
               i.email,
               COUNT(c.course_id) AS course_count
        FROM instructors i
        LEFT JOIN courses c ON i.instructor_id = c.instructor_id
        GROUP BY i.instructor_id, instructor_name, i.email
        ORDER BY i.instructor_id
    """)
    if df.empty:
        st.info("No instructors available.")
    else:
        iid = st.selectbox("Select Instructor ID to delete", df["instructor_id"].tolist(),
                           key="delete_instructor_id")
        row = df[df.instructor_id == iid].iloc[0]
        st.write(f"Selected: **{row['instructor_name']}** — Courses: **{row['course_count']}**")
        confirm = st.checkbox("I understand this deletion cannot be undone.", key="confirm_instructor_delete")
        if st.button("Delete Instructor", type="primary", disabled=not confirm):
            try:
                execute("DELETE FROM instructors WHERE instructor_id=%s", (iid,))
                st.success("Instructor deleted successfully.")
                st.rerun()
            except Error as e:
                st.error(f"Could not delete instructor. Make sure the instructor has no courses. Details: {e}")
