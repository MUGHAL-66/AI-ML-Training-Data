import os
from datetime import date
import mysql.connector
from mysql.connector import Error
import pandas as pd
import streamlit as st

st.set_page_config(page_title="LMS", page_icon="🎓", layout="wide")

# ---------- Database helpers (all queries parameterized) ----------
def get_conn():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "lms_db"),
    )

def query(sql, params=None):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        return pd.DataFrame(cur.fetchall())
    finally:
        conn.close()

def execute(sql, params=None):
    """Returns (ok, message) with friendly handling of constraint errors."""
    conn = get_conn()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        return True, "Done."
    except Error as e:
        conn.rollback()
        msgs = {1062: "Duplicate value: a record with this unique value already exists.",
                1451: "Cannot delete: other records depend on this one.",
                1452: "Invalid reference: the related record does not exist.",
                3819: "Value violates a check rule (e.g. marks or fee out of range)."}
        return False, msgs.get(e.errno, f"Database error: {e.msg}")
    finally:
        conn.close()

def report(ok_msg, result, rerun=True):
    ok, msg = result
    if ok:
        st.success(ok_msg)
        if rerun:
            st.rerun()
    else:
        st.error(msg)

def options(df, id_col, label_col):
    return {f"{r[label_col]} (#{r[id_col]})": r[id_col] for _, r in df.iterrows()}

def valid_email(e):
    return "@" in e and "." in e.split("@")[-1]

def search_table(df, key):
    term = st.text_input("Search", key=key)
    if term and not df.empty:
        mask = df.astype(str).apply(lambda c: c.str.contains(term, case=False)).any(axis=1)
        df = df[mask]
    st.dataframe(df, use_container_width=True, hide_index=True)

def confirm_delete(label, key, sql, params):
    sure = st.checkbox(f"Yes, permanently delete {label}", key=f"chk_{key}")
    if st.button("Delete", key=f"del_{key}", disabled=not sure, type="primary"):
        report("Deleted.", execute(sql, params))

# ---------- Pages ----------
def dashboard():
    st.title("📊 Dashboard")
    k = query("""SELECT
      (SELECT COUNT(*) FROM students) AS students,
      (SELECT COUNT(*) FROM students WHERE status='Active') AS active_students,
      (SELECT COUNT(*) FROM instructors) AS instructors,
      (SELECT COUNT(*) FROM courses) AS courses,
      (SELECT COUNT(*) FROM enrollments) AS enrollments""").iloc[0]
    cols = st.columns(5)
    for c, (label, key) in zip(cols, [("Students","students"),("Active Students","active_students"),
            ("Instructors","instructors"),("Courses","courses"),("Enrollments","enrollments")]):
        c.metric(label, int(k[key]))
    a, b = st.columns(2)
    with a:
        st.subheader("Enrollments by status")
        df = query("SELECT status, COUNT(*) AS total FROM enrollments GROUP BY status")
        if not df.empty: st.bar_chart(df.set_index("status"))
    with b:
        st.subheader("Top courses by enrollment")
        df = query("""SELECT c.course_name, COUNT(e.enrollment_id) AS total
                      FROM courses c LEFT JOIN enrollments e ON e.course_id=c.course_id
                      GROUP BY c.course_id, c.course_name ORDER BY total DESC LIMIT 5""")
        if not df.empty: st.bar_chart(df.set_index("course_name"))
    st.subheader("Recent enrollments")
    st.dataframe(query("""SELECT e.enrollment_id, s.full_name AS student, c.course_name AS course,
                          e.enrollment_date, e.status FROM enrollments e
                          JOIN students s ON s.student_id=e.student_id
                          JOIN courses c ON c.course_id=e.course_id
                          ORDER BY e.enrollment_date DESC LIMIT 10"""),
                 use_container_width=True, hide_index=True)

def students():
    st.title("🎓 Students")
    t1, t2, t3 = st.tabs(["View / Search", "Add", "Edit / Delete"])
    df = query("SELECT * FROM students ORDER BY student_id")
    with t1:
        search_table(df, "s_search")
    with t2:
        with st.form("add_student", clear_on_submit=True):
            name = st.text_input("Full name"); email = st.text_input("Email")
            phone = st.text_input("Phone"); d = st.date_input("Enrollment date", date.today())
            status = st.selectbox("Status", ["Active", "Inactive", "Graduated"])
            if st.form_submit_button("Add student"):
                if not name.strip() or not valid_email(email):
                    st.error("Name and a valid email are required.")
                else:
                    report("Student added.", execute(
                        "INSERT INTO students (full_name,email,phone,enrollment_date,status) VALUES (%s,%s,%s,%s,%s)",
                        (name.strip(), email.strip(), phone.strip(), d, status)))
    with t3:
        if df.empty: st.info("No students."); return
        opts = options(df, "student_id", "full_name")
        sid = opts[st.selectbox("Select student", list(opts))]
        r = df[df.student_id == sid].iloc[0]
        name = st.text_input("Full name", r.full_name, key="s_n"); email = st.text_input("Email", r.email, key="s_e")
        phone = st.text_input("Phone", r.phone or "", key="s_p")
        d = st.date_input("Enrollment date", r.enrollment_date, key="s_d")
        sts = ["Active", "Inactive", "Graduated"]
        status = st.selectbox("Status", sts, sts.index(r.status), key="s_s")
        if st.button("Update student"):
            if not name.strip() or not valid_email(email): st.error("Name and a valid email are required.")
            else:
                report("Student updated.", execute(
                    "UPDATE students SET full_name=%s,email=%s,phone=%s,enrollment_date=%s,status=%s WHERE student_id=%s",
                    (name.strip(), email.strip(), phone.strip(), d, status, sid)))
        st.divider()
        confirm_delete(r.full_name, "stu", "DELETE FROM students WHERE student_id=%s", (sid,))

def instructors():
    st.title("👩‍🏫 Instructors")
    t1, t2, t3 = st.tabs(["View / Search", "Add", "Edit / Delete"])
    df = query("SELECT * FROM instructors ORDER BY instructor_id")
    with t1:
        search_table(df, "i_search")
    with t2:
        with st.form("add_inst", clear_on_submit=True):
            name = st.text_input("Full name"); spec = st.text_input("Specialization")
            email = st.text_input("Email"); status = st.selectbox("Status", ["Active", "Inactive"])
            if st.form_submit_button("Add instructor"):
                if not name.strip() or not spec.strip() or not valid_email(email):
                    st.error("Name, specialization and a valid email are required.")
                else:
                    report("Instructor added.", execute(
                        "INSERT INTO instructors (full_name,specialization,email,status) VALUES (%s,%s,%s,%s)",
                        (name.strip(), spec.strip(), email.strip(), status)))
    with t3:
        if df.empty: st.info("No instructors."); return
        opts = options(df, "instructor_id", "full_name")
        iid = opts[st.selectbox("Select instructor", list(opts))]
        r = df[df.instructor_id == iid].iloc[0]
        name = st.text_input("Full name", r.full_name, key="i_n"); spec = st.text_input("Specialization", r.specialization, key="i_sp")
        email = st.text_input("Email", r.email, key="i_e")
        sts = ["Active", "Inactive"]; status = st.selectbox("Status", sts, sts.index(r.status), key="i_s")
        if st.button("Update instructor"):
            if not name.strip() or not valid_email(email): st.error("Name and a valid email are required.")
            else:
                report("Instructor updated.", execute(
                    "UPDATE instructors SET full_name=%s,specialization=%s,email=%s,status=%s WHERE instructor_id=%s",
                    (name.strip(), spec.strip(), email.strip(), status, iid)))
        st.divider()
        confirm_delete(r.full_name, "ins", "DELETE FROM instructors WHERE instructor_id=%s", (iid,))

def courses():
    st.title("📚 Courses")
    t1, t2, t3 = st.tabs(["View / Search", "Add", "Edit / Delete"])
    df = query("""SELECT c.course_id, c.course_name, c.description, c.instructor_id, i.full_name AS instructor,
                  c.duration_weeks, c.fee, c.status FROM courses c
                  JOIN instructors i ON i.instructor_id=c.instructor_id ORDER BY c.course_id""")
    inst = query("SELECT instructor_id, full_name FROM instructors WHERE status='Active' ORDER BY full_name")
    inst_all = query("SELECT instructor_id, full_name FROM instructors ORDER BY full_name")
    with t1:
        search_table(df.drop(columns=["instructor_id"]) if not df.empty else df, "c_search")
    with t2:
        if inst.empty: st.warning("Add an active instructor first.")
        else:
            io = options(inst, "instructor_id", "full_name")
            with st.form("add_course", clear_on_submit=True):
                name = st.text_input("Course name"); desc = st.text_area("Description")
                ins = st.selectbox("Instructor", list(io))
                dur = st.number_input("Duration (weeks)", 1, 104, 8); fee = st.number_input("Fee", 0.0, step=500.0)
                status = st.selectbox("Status", ["Active", "Inactive"])
                if st.form_submit_button("Add course"):
                    if not name.strip(): st.error("Course name is required.")
                    else:
                        report("Course added.", execute(
                            "INSERT INTO courses (course_name,description,instructor_id,duration_weeks,fee,status) VALUES (%s,%s,%s,%s,%s,%s)",
                            (name.strip(), desc, io[ins], dur, fee, status)))
    with t3:
        if df.empty: st.info("No courses."); return
        opts = options(df, "course_id", "course_name")
        cid = opts[st.selectbox("Select course", list(opts))]
        r = df[df.course_id == cid].iloc[0]
        io = options(inst_all, "instructor_id", "full_name"); labels = list(io)
        cur = next(l for l, v in io.items() if v == r.instructor_id)
        name = st.text_input("Course name", r.course_name, key="c_n"); desc = st.text_area("Description", r.description or "", key="c_d")
        ins = st.selectbox("Instructor", labels, labels.index(cur), key="c_i")
        dur = st.number_input("Duration (weeks)", 1, 104, int(r.duration_weeks), key="c_w")
        fee = st.number_input("Fee", 0.0, value=float(r.fee), step=500.0, key="c_f")
        sts = ["Active", "Inactive"]; status = st.selectbox("Status", sts, sts.index(r.status), key="c_s")
        if st.button("Update course"):
            if not name.strip(): st.error("Course name is required.")
            else:
                report("Course updated.", execute(
                    "UPDATE courses SET course_name=%s,description=%s,instructor_id=%s,duration_weeks=%s,fee=%s,status=%s WHERE course_id=%s",
                    (name.strip(), desc, io[ins], dur, fee, status, cid)))
        st.divider()
        confirm_delete(r.course_name, "crs", "DELETE FROM courses WHERE course_id=%s", (cid,))

def enrollments():
    st.title("📝 Enrollments")
    t1, t2, t3 = st.tabs(["History", "Enroll student", "Update status / Delete"])
    df = query("""SELECT e.enrollment_id, s.full_name AS student, c.course_name AS course,
                  e.enrollment_date, e.status FROM enrollments e
                  JOIN students s ON s.student_id=e.student_id
                  JOIN courses c ON c.course_id=e.course_id ORDER BY e.enrollment_id DESC""")
    with t1:
        search_table(df, "e_search")
    with t2:
        stu = query("SELECT student_id, full_name FROM students WHERE status='Active' ORDER BY full_name")
        crs = query("SELECT course_id, course_name FROM courses WHERE status='Active' ORDER BY course_name")
        if stu.empty or crs.empty: st.warning("Need at least one active student and one active course.")
        else:
            so, co = options(stu, "student_id", "full_name"), options(crs, "course_id", "course_name")
            with st.form("enroll", clear_on_submit=True):
                s = st.selectbox("Student", list(so)); c = st.selectbox("Course", list(co))
                d = st.date_input("Enrollment date", date.today())
                if st.form_submit_button("Enroll"):
                    report("Student enrolled.", execute(
                        "INSERT INTO enrollments (student_id,course_id,enrollment_date) VALUES (%s,%s,%s)",
                        (so[s], co[c], d)))
    with t3:
        if df.empty: st.info("No enrollments."); return
        labels = {f"#{r.enrollment_id} {r.student} → {r.course} [{r.status}]": r.enrollment_id for _, r in df.iterrows()}
        eid = labels[st.selectbox("Select enrollment", list(labels))]
        sts = ["Enrolled", "Completed", "Dropped"]
        cur = df[df.enrollment_id == eid].iloc[0].status
        new = st.selectbox("New status", sts, sts.index(cur))
        if st.button("Update status"):
            report("Status updated.", execute("UPDATE enrollments SET status=%s WHERE enrollment_id=%s", (new, eid)))
        st.divider()
        confirm_delete(f"enrollment #{eid}", "enr", "DELETE FROM enrollments WHERE enrollment_id=%s", (eid,))

def grades():
    st.title("🏅 Grades")
    t1, t2, t3 = st.tabs(["View", "Record marks", "Edit / Delete"])
    df = query("""SELECT g.grade_id, s.full_name AS student, c.course_name AS course,
                  g.assignment_marks, g.quiz_marks, g.final_marks, g.total_marks,
                  CASE WHEN g.total_marks>=85 THEN 'A' WHEN g.total_marks>=70 THEN 'B'
                       WHEN g.total_marks>=50 THEN 'C' ELSE 'F' END AS grade
                  FROM grades g JOIN enrollments e ON e.enrollment_id=g.enrollment_id
                  JOIN students s ON s.student_id=e.student_id
                  JOIN courses c ON c.course_id=e.course_id ORDER BY g.total_marks DESC""")
    with t1:
        search_table(df, "g_search")
    with t2:
        pend = query("""SELECT e.enrollment_id, CONCAT(s.full_name,' → ',c.course_name) AS label
                        FROM enrollments e JOIN students s ON s.student_id=e.student_id
                        JOIN courses c ON c.course_id=e.course_id
                        LEFT JOIN grades g ON g.enrollment_id=e.enrollment_id
                        WHERE g.grade_id IS NULL AND e.status<>'Dropped'""")
        if pend.empty: st.info("All eligible enrollments already have grades.")
        else:
            po = options(pend, "enrollment_id", "label")
            with st.form("add_grade", clear_on_submit=True):
                e = st.selectbox("Enrollment", list(po))
                a = st.number_input("Assignment (max 30)", 0.0, 30.0, step=0.5)
                q = st.number_input("Quiz (max 20)", 0.0, 20.0, step=0.5)
                f = st.number_input("Final exam (max 50)", 0.0, 50.0, step=0.5)
                if st.form_submit_button("Save marks"):
                    report("Marks recorded.", execute(
                        "INSERT INTO grades (enrollment_id,assignment_marks,quiz_marks,final_marks) VALUES (%s,%s,%s,%s)",
                        (po[e], a, q, f)))
    with t3:
        if df.empty: st.info("No grades."); return
        labels = {f"#{r.grade_id} {r.student} – {r.course}": r.grade_id for _, r in df.iterrows()}
        gid = labels[st.selectbox("Select record", list(labels))]
        r = df[df.grade_id == gid].iloc[0]
        a = st.number_input("Assignment (max 30)", 0.0, 30.0, float(r.assignment_marks), 0.5, key="g_a")
        q = st.number_input("Quiz (max 20)", 0.0, 20.0, float(r.quiz_marks), 0.5, key="g_q")
        f = st.number_input("Final exam (max 50)", 0.0, 50.0, float(r.final_marks), 0.5, key="g_f")
        st.caption(f"Total: {a+q+f:.2f} / 100")
        if st.button("Update marks"):
            report("Marks updated.", execute(
                "UPDATE grades SET assignment_marks=%s,quiz_marks=%s,final_marks=%s WHERE grade_id=%s", (a, q, f, gid)))
        st.divider()
        confirm_delete("this grade record", "grd", "DELETE FROM grades WHERE grade_id=%s", (gid,))

def reports():
    st.title("📈 Reports")
    R = {
     "BR-01 Course popularity": """SELECT c.course_name, COUNT(e.enrollment_id) AS total_enrollments
        FROM courses c JOIN enrollments e ON e.course_id=c.course_id
        GROUP BY c.course_id, c.course_name ORDER BY total_enrollments DESC""",
     "BR-02 Instructor workload": """SELECT i.full_name AS instructor, COUNT(c.course_id) AS courses_taught
        FROM instructors i LEFT JOIN courses c ON c.instructor_id=i.instructor_id
        GROUP BY i.instructor_id, i.full_name ORDER BY courses_taught DESC""",
     "BR-03 Student performance": """SELECT s.full_name AS student, SUM(g.total_marks) AS total_marks,
        ROUND(AVG(g.total_marks),2) AS avg_marks FROM students s
        JOIN enrollments e ON e.student_id=s.student_id JOIN grades g ON g.enrollment_id=e.enrollment_id
        GROUP BY s.student_id, s.full_name ORDER BY total_marks DESC""",
     "BR-04 Active students": "SELECT COUNT(*) AS active_students FROM students WHERE status='Active'",
     "BR-05 Enrollment status": "SELECT status, COUNT(*) AS total FROM enrollments GROUP BY status",
     "BR-06 Courses with no students": """SELECT c.course_name FROM courses c
        LEFT JOIN enrollments e ON e.course_id=c.course_id WHERE e.enrollment_id IS NULL""",
    }
    pick = st.selectbox("Report", list(R))
    df = query(R[pick])
    if df.empty: st.info("No rows for this report.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)
        if len(df.columns) == 2 and pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
            st.bar_chart(df.set_index(df.columns[0]))
        st.download_button("Download CSV", df.to_csv(index=False), f"{pick[:5]}.csv", "text/csv")

PAGES = {"Dashboard": dashboard, "Students": students, "Instructors": instructors,
         "Courses": courses, "Enrollments": enrollments, "Grades": grades, "Reports": reports}

st.sidebar.title("🎓 LMS")
choice = st.sidebar.radio("Navigate", list(PAGES))
try:
    PAGES[choice]()
except Error as e:
    st.error(f"Cannot reach the database: {e.msg}. Check DB_* environment variables and that lms_database.sql was loaded.")
