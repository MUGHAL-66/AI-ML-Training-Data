import streamlit as st

from utils.ui_helpers import apply_theme

st.set_page_config(page_title="Academia LMS", page_icon="assets/logo.svg", layout="wide", initial_sidebar_state="expanded")
apply_theme()

pages = [st.Page("pages/0_Dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)]
for path, title, icon in [
    ("pages/1_Students.py", "Students", ":material/groups:"),
    ("pages/2_Instructors.py", "Instructors", ":material/person:"),
    ("pages/3_Courses.py", "Courses", ":material/menu_book:"),
    ("pages/4_Enrollments.py", "Enrollments", ":material/how_to_reg:"),
    ("pages/5_Grades.py", "Grades", ":material/grade:"),
    ("pages/6_Reports.py", "Reports", ":material/assessment:"),
]:
    pages.append(st.Page(path, title=title, icon=icon))

with st.sidebar:
    st.markdown("<div style='padding:1.1rem .55rem 1.3rem'><div style='display:flex;align-items:center;gap:.65rem'><span class='material-symbols-rounded' style='font-size:30px;color:#D4A853'>school</span><strong style='font-size:1.12rem;color:#fff'>Academia LMS</strong></div><div style='font-size:.75rem;color:#D7C4CA;margin:.35rem 0 0 2.55rem'>Learning Management System</div></div>", unsafe_allow_html=True)
    nav = st.navigation(pages)
    st.divider()
    st.caption("Academic Administration")
nav.run()
