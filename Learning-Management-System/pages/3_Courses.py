import streamlit as st
from services import course_service as svc
from utils.validators import required,valid_duration,valid_fee,STATUSES
from utils.ui_helpers import run_page,frame

def page():
 st.title("Courses");st.caption("Manage course catalog, teaching assignments, and enrollment counts.")
 rows=svc.all(st.text_input("Search course name"),st.selectbox("Status",["All",*STATUSES['course']]))
 frame(rows)
 ins=svc.instructors()
 with st.expander("Add a course"):
  if not ins:st.info("Add an active instructor before creating a course.")
  else:
   with st.form("add"):
    n=st.text_input("Course name *");desc=st.text_area("Description");opts={x['full_name']:x['instructor_id'] for x in ins};iid=st.selectbox("Instructor",opts);weeks=st.number_input("Duration (weeks)",min_value=1,value=8);fee=st.number_input("Fee",min_value=0.0,step=100.0);status=st.selectbox("Status",STATUSES['course'])
    if st.form_submit_button("Add course"):
     try:svc.save((required(n,"Course name"),desc,opts[iid],valid_duration(weeks),valid_fee(fee),status));st.success("Course added.");st.rerun()
     except ValueError as x:st.error(str(x))
 with st.expander("Edit or delete a course"):
  if rows and ins:
   opts={x['full_name']:x['instructor_id'] for x in ins};labels={f"{r['course_name']} · {r['instructor']}":r for r in rows};r=labels[st.selectbox("Choose course",labels)]
   with st.form("edit"):
    n=st.text_input("Course name",r['course_name']);desc=st.text_area("Description",r['description'] or "");names=list(opts);idx=next((i for i,x in enumerate(names) if opts[x]==r['instructor_id']),0);iname=st.selectbox("Instructor",names,index=idx);weeks=st.number_input("Duration",min_value=1,value=int(r['duration_weeks']));fee=st.number_input("Fee",min_value=0.0,value=float(r['fee']));status=st.selectbox("Status",STATUSES['course'],index=STATUSES['course'].index(r['status']))
    if st.form_submit_button("Save changes"):
     try:svc.save((required(n,"Course name"),desc,opts[iname],valid_duration(weeks),valid_fee(fee),status),r['course_id']);st.success("Course updated.");st.rerun()
     except ValueError as x:st.error(str(x))
   if st.checkbox("I understand this removes the course") and st.button("Delete course"):
    svc.delete(r['course_id']);st.success("Course deleted.");st.rerun()
run_page(page)
