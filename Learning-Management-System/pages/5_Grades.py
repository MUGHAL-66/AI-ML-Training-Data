import streamlit as st
from services import grade_service as svc
from utils.ui_helpers import run_page,frame

def page():
 st.title("Grades");st.caption("Record component marks; totals are derived and grade bands use the documented 100 point scale.")
 rows=svc.all();frame(rows)
 missing=[r for r in rows if r['grade_id'] is None]
 options={f"{r['student']} · {r['course']} · enrollment {r['enrollment_id']}":r for r in rows}
 if options:
  with st.form("grade"):
   label=st.selectbox("Enrollment",options);r=options[label];defaults=[float(r[x] or 0) for x in ('assignment_marks','quiz_marks','final_exam_marks')]
   a=st.number_input("Assignment (0–20)",0.0,20.0,defaults[0]);q=st.number_input("Quiz (0–20)",0.0,20.0,defaults[1]);f=st.number_input("Final exam (0–60)",0.0,60.0,defaults[2])
   if st.form_submit_button("Save grade"):
    try:svc.save(r['enrollment_id'],a,q,f,r['grade_id']);st.success("Grade saved.");st.rerun()
    except ValueError as ex:st.error(str(ex))
 if rows:
  ranked=sorted((r for r in rows if r['total_marks'] is not None),key=lambda x:float(x['total_marks']),reverse=True)
  def band(mark):return "A" if mark>=85 else "B" if mark>=70 else "C" if mark>=55 else "D" if mark>=40 else "F"
  st.subheader("Ranked performance");frame([{"Rank":i+1,"Student":r['student'],"Course":r['course'],"Total":r['total_marks'],"Percentage":f"{float(r['total_marks']):.1f}%","Band":band(float(r['total_marks']))} for i,r in enumerate(ranked)])
 st.caption("Bands: A 85–100 · B 70–84.99 · C 55–69.99 · D 40–54.99 · F below 40. Missing grades remain unranked.")
run_page(page)
