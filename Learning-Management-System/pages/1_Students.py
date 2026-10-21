import streamlit as st
from datetime import date
from services import student_service as svc
from utils.validators import required,valid_email,valid_phone,valid_status,STATUSES
from utils.ui_helpers import run_page,frame

def page():
 st.title("Students"); st.caption("Maintain student records and enrollment status.")
 rows=svc.all(st.text_input("Search name or email"),st.selectbox("Status",["All",*STATUSES['student']]))
 frame(rows)
 with st.expander("Add a student",expanded=False):
  with st.form("add"):
   n=st.text_input("Full name *");e=st.text_input("Email *");p=st.text_input("Phone");d=st.date_input("Enrollment date",date.today());s=st.selectbox("Status",STATUSES['student'])
   if st.form_submit_button("Add student"):
    try: svc.save((required(n,"Full name"),valid_email(e),valid_phone(p),d,s));st.success("Student added.");st.rerun()
    except ValueError as ex:st.error(str(ex))
 with st.expander("Edit or delete a student"):
  if rows:
   labels={f"{r['full_name']} · {r['email']}":r for r in rows};r=labels[st.selectbox("Choose student",labels)]
   with st.form("edit"):
    n=st.text_input("Full name",r['full_name']);e=st.text_input("Email",r['email']);p=st.text_input("Phone",r['phone'] or "");d=st.date_input("Enrollment date",r['enrollment_date']);s=st.selectbox("Status",STATUSES['student'],index=STATUSES['student'].index(r['status']))
    if st.form_submit_button("Save changes"):
     try:svc.save((required(n,"Full name"),valid_email(e),valid_phone(p),d,s),r['student_id']);st.success("Student updated.");st.rerun()
     except ValueError as ex:st.error(str(ex))
   if st.checkbox("I understand this removes the student record") and st.button("Delete student",type="secondary"):
    svc.delete(r['student_id']);st.success("Student deleted.");st.rerun()
run_page(page)
