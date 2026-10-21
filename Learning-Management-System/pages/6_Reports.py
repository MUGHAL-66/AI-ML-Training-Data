import streamlit as st
import plotly.express as px
from services.report_service import reports
from db import query
from utils.ui_helpers import run_page,frame,csv_download

def page():
 st.title("Reports");st.caption("Six live reports that answer core academic operations questions.")
 for title,(question,sql) in reports().items():
  with st.container(border=True):
   st.subheader(title);st.caption(question);rows=query(sql);frame(rows);csv_download(rows,title[:5].replace(" ","_").lower()+".csv")
   if rows and "current_enrollments" in rows[0]:st.plotly_chart(px.bar(rows,x="course_name",y="current_enrollments",labels={"course_name":"Course","current_enrollments":"Current enrollments"}),use_container_width=True)
run_page(page)
