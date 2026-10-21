from datetime import date

import plotly.express as px
import streamlit as st

from services.report_service import dashboard
from utils.chart_data import course_popularity_long_frame, enrollment_status_frame
from utils.ui_helpers import page_header, run_page, frame


def chart_layout(fig):
    fig.update_layout(
        template="plotly_white", height=330, margin=dict(l=12, r=12, t=22, b=12),
        font=dict(family="Arial, sans-serif", color="#4C4650", size=12),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, automargin=True)
    fig.update_yaxes(gridcolor="#EEE9E7", zeroline=False, automargin=True)
    return fig


def page():
    page_header("Dashboard", "A clear overview of academic activity across your institution.")
    left, right = st.columns([3, 1])
    left.caption("ACADEMIC OVERVIEW  ·  " + date.today().strftime("%B %d, %Y"))
    if right.button("Refresh data", use_container_width=True):
        st.rerun()

    data = dashboard()
    main_metrics = st.columns(4)
    for col, label, value in zip(
        main_metrics,
        ["Total students", "Active students", "Instructors", "Courses"],
        [data["students"], data["active"], data["instructors"], data["courses"]],
    ):
        col.metric(label, value)

    enrollments = enrollment_status_frame(data["enrollments"])
    status = dict(zip(enrollments["status"], enrollments["count"]))
    total = int(enrollments["count"].sum()) if not enrollments.empty else 0
    st.markdown("#### Enrollment and performance")
    secondary = st.columns(5)
    values = [
        ("Total enrollments", total),
        ("Currently enrolled", int(status.get("Enrolled", 0))),
        ("Completed", int(status.get("Completed", 0))),
        ("Dropped", int(status.get("Dropped", 0))),
        ("Average marks", "—" if data["average"] is None else f"{float(data['average']):.1f} / 100"),
    ]
    for col, (label, value) in zip(secondary, values):
        col.metric(label, value)

    st.markdown("#### Quick actions")
    actions = st.columns(4)
    for col, label, target in zip(
        actions,
        ["Add student", "Add instructor", "Add course", "View reports"],
        ["pages/1_Students.py", "pages/2_Instructors.py", "pages/3_Courses.py", "pages/6_Reports.py"],
    ):
        if col.button(label, use_container_width=True):
            st.switch_page(target)

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            st.markdown("#### Enrollment status")
            if not enrollments.empty and total > 0:
                fig = px.pie(
                    enrollments, names="status", values="count", hole=.66,
                    color="status", color_discrete_map={"Enrolled": "#641E32", "Completed": "#6F927C", "Dropped": "#D4A853"},
                )
                fig.update_traces(textposition="inside", textinfo="percent", insidetextfont=dict(color="white"), hole=0.66)
                fig.update_layout(showlegend=True, annotations=[dict(text=f"{total}<br><span style='font-size:11px'>enrollments</span>", x=.5, y=.5, showarrow=False, font=dict(size=20, color="#24212A"))])
                st.plotly_chart(chart_layout(fig), use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Enrollment status will appear here when records are available.")
        with st.container(border=True):
            st.markdown("#### Course popularity")
            popularity = course_popularity_long_frame(data["popular"])
            if not popularity.empty and popularity["Enrollments"].sum() > 0:
                fig = px.bar(
                    popularity, x="course_name", y="Enrollments", color="Measure", barmode="group",
                    labels={"course_name": "Course", "Enrollments": "Enrollments", "Measure": ""},
                    color_discrete_map={"Current enrollments": "#641E32", "All enrollments": "#D4A853"},
                )
                st.plotly_chart(chart_layout(fig), use_container_width=True, config={"displayModeBar": False})
            else:
                st.info("Course enrollment data will appear here when available.")
    with right:
        with st.container(border=True):
            st.markdown("#### Recent enrollments")
            frame(data["recent"])
        with st.container(border=True):
            st.markdown("#### Top-performing students")
            frame(data["top"])
        with st.container(border=True):
            st.markdown("#### Instructor course count")
            frame(data["workload"])


run_page(page)
