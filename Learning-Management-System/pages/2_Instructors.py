import streamlit as st
from services import instructor_service as svc
from utils.validators import required,valid_email,STATUSES
from utils.ui_helpers import run_page,frame

def page():
 st.title("Instructors");st.caption("Manage instructor profiles and teaching assignments.")
 rows=svc.all(st.text_input("Search name, email or specialization"),st.selectbox("Status",["All",*STATUSES['instructor']]))
 frame(rows)
 with st.expander("Add an instructor"):
  with st.form("add"):
   n=st.text_input("Full name *");e=st.text_input("Email *");sp=st.text_input("Specialization *");s=st.selectbox("Status",STATUSES['instructor'])
   if st.form_submit_button("Add instructor"):
    try:svc.save((required(n,"Full name"),valid_email(e),required(sp,"Specialization"),s));st.success("Instructor added.");st.rerun()
    except ValueError as x:st.error(str(x))
 with st.expander("Edit or delete an instructor"):
  if rows:
   labels={f"{r['full_name']} · {r['email']}":r for r in rows};r=labels[st.selectbox("Choose instructor",labels)]
   with st.form("edit"):
    n=st.text_input("Full name",r['full_name']);e=st.text_input("Email",r['email']);sp=st.text_input("Specialization",r['specialization']);s=st.selectbox("Status",STATUSES['instructor'],index=STATUSES['instructor'].index(r['status']))
    if st.form_submit_button("Save changes"):
     try:svc.save((required(n,"Full name"),valid_email(e),required(sp,"Specialization"),s),r['instructor_id']);st.success("Instructor updated.");st.rerun()
     except ValueError as x:st.error(str(x))
   if st.checkbox("I understand this removes the instructor record") and st.button("Delete instructor"):
    svc.delete(r['instructor_id']);st.success("Instructor deleted.");st.rerun()
run_page(page)
