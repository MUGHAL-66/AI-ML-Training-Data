import streamlit as st
from datetime import date
from services import enrollment_service as svc
from utils.validators import STATUSES
from utils.ui_helpers import run_page,frame

def page():
 st.title("Enrollments");st.caption("Create and maintain student course enrollments.")
 search=st.text_input("Search student or course");status=st.selectbox("Status",["All",*STATUSES['enrollment']])
 use_dates=st.checkbox("Filter by enrollment date")
 start=end=None
 if use_dates:
  left,right=st.columns(2);start=left.date_input("From");end=right.date_input("Through")
  if start>end:st.error("The start date must be on or before the end date.")
 rows=svc.all(search,status,start if use_dates and start<=end else None,end if use_dates and start<=end else None)
 frame(rows)
 students,courses=svc.options()
 with st.expander("Create enrollment"):
  if not students or not courses:st.info("Create an active student and an active course before enrolling.")
  else:
   with st.form("add"):
    sm={x['full_name']:x['student_id'] for x in students};cm={x['course_name']:x['course_id'] for x in courses};s=st.selectbox("Student",sm);c=st.selectbox("Course",cm);d=st.date_input("Enrollment date",date.today())
    if st.form_submit_button("Enroll student"):
     svc.create(sm[s],cm[c],d);st.success("Enrollment created.");st.rerun()
 with st.expander("Update or delete an enrollment"):
  if rows:
   labels={f"{r['student']} · {r['course']} · {r['enrollment_date']}":r for r in rows};r=labels[st.selectbox("Choose enrollment",labels)]
   status=st.selectbox("Status",STATUSES['enrollment'],index=STATUSES['enrollment'].index(r['status']))
   if st.button("Update status"):
    svc.update(r['enrollment_id'],status);st.success("Enrollment updated.");st.rerun()
   if st.checkbox("I understand this removes this enrollment and its grade") and st.button("Delete enrollment"):
    svc.delete(r['enrollment_id']);st.success("Enrollment deleted.");st.rerun()
run_page(page)
