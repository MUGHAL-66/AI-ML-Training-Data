import streamlit as st
import pandas as pd
from mysql.connector import Error
from connection import get_connection

st.title("👨‍🎓 Students")

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
    st.subheader("Add Student")
    with st.form("add_student"):
        c1, c2 = st.columns(2)
        first = c1.text_input("First Name")
        last = c2.text_input("Last Name")
        email = c1.text_input("Email")
        phone = c2.text_input("Phone")
        enrollment_date = c1.date_input("Enrollment Date")
        status = c2.selectbox("Status", ["Active", "Inactive"])
        submitted = st.form_submit_button("Add Student", type="primary")

        if submitted:
            if not first.strip() or not last.strip() or not email.strip():
                st.error("First name, last name and email are required.")
            elif "@" not in email or "." not in email:
                st.error("Please enter a valid email.")
            else:
                try:
                    execute("""
                        INSERT INTO students
                        (first_name, last_name, email, phone, enrollment_date, status)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (first.strip(), last.strip(), email.strip(), phone.strip(),
                          enrollment_date, status))
                    st.success("Student added successfully.")
                    st.rerun()
                except Error as e:
                    st.error(f"Could not add student: {e}")

with tab2:
    st.subheader("Search Students")
    search = st.text_input("Search by ID, name, email or phone")
    query = """
        SELECT student_id, first_name, last_name, email, phone,
               enrollment_date, status
        FROM students
    """
    params = None
    if search.strip():
        query += """
            WHERE CAST(student_id AS CHAR) LIKE %s
               OR first_name LIKE %s
               OR last_name LIKE %s
               OR email LIKE %s
               OR phone LIKE %s
        """
        term = f"%{search.strip()}%"
        params = (term, term, term, term, term)
    query += " ORDER BY student_id DESC"
    df = fetch_df(query, params)
    st.dataframe(df, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("Update Student")
    students = fetch_df("""
        SELECT student_id, first_name, last_name, email, phone,
               enrollment_date, status
        FROM students ORDER BY student_id
    """)
    if students.empty:
        st.info("No students available.")
    else:
        sid = st.selectbox("Select Student ID", students["student_id"].tolist())
        row = students[students.student_id == sid].iloc[0]
        with st.form("update_student"):
            c1, c2 = st.columns(2)
            first = c1.text_input("First Name", value=str(row["first_name"]))
            last = c2.text_input("Last Name", value=str(row["last_name"]))
            email = c1.text_input("Email", value=str(row["email"]))
            phone = c2.text_input("Phone", value="" if pd.isna(row["phone"]) else str(row["phone"]))
            enrollment_date = c1.date_input("Enrollment Date", value=pd.to_datetime(row["enrollment_date"]).date())
            status = c2.selectbox("Status", ["Active", "Inactive"],
                                  index=0 if row["status"] == "Active" else 1)
            submitted = st.form_submit_button("Update Student", type="primary")
            if submitted:
                if not first.strip() or not last.strip() or not email.strip():
                    st.error("Required fields cannot be empty.")
                else:
                    try:
                        execute("""
                            UPDATE students
                            SET first_name=%s, last_name=%s, email=%s, phone=%s,
                                enrollment_date=%s, status=%s
                            WHERE student_id=%s
                        """, (first.strip(), last.strip(), email.strip(), phone.strip(),
                              enrollment_date, status, sid))
                        st.success("Student updated successfully.")
                        st.rerun()
                    except Error as e:
                        st.error(f"Could not update student: {e}")

with tab4:
    st.subheader("Delete Student")
    st.warning("Deleting a student also deletes their enrollments and grades because of the database foreign-key rules.")
    students = fetch_df("""
        SELECT student_id,
               CONCAT(first_name, ' ', last_name) AS student_name,
               email
        FROM students ORDER BY student_id
    """)
    if students.empty:
        st.info("No students available.")
    else:
        sid = st.selectbox(
            "Select Student ID to delete",
            students["student_id"].tolist(),
            key="delete_student_id"
        )
        selected = students[students.student_id == sid].iloc[0]
        st.write(f"Selected: **{selected['student_name']}** — {selected['email']}")
        confirm = st.checkbox("I understand this deletion cannot be undone.", key="confirm_student_delete")
        if st.button("Delete Student", type="primary", disabled=not confirm):
            try:
                execute("DELETE FROM students WHERE student_id=%s", (sid,))
                st.success("Student deleted successfully.")
                st.rerun()
            except Error as e:
                st.error(f"Could not delete student: {e}")
