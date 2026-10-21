"""Normalize database result rows before handing them to Plotly."""
import pandas as pd


def enrollment_status_frame(rows):
    columns = ["status", "count"]
    frame = pd.DataFrame(rows)
    if frame.empty or not set(columns).issubset(frame.columns):
        return pd.DataFrame(columns=columns)
    frame = frame[columns].copy()
    frame["status"] = frame["status"].astype("string").str.strip()
    frame["count"] = pd.to_numeric(frame["count"], errors="coerce").fillna(0)
    return frame[frame["status"].notna() & frame["status"].ne("")].reset_index(drop=True)


def course_popularity_long_frame(rows):
    """Return Plotly-ready long data with null/invalid counts treated as zero."""
    columns = ["course_name", "Measure", "Enrollments"]
    source = pd.DataFrame(rows)
    required = {"course_name", "current_count", "total_count"}
    if source.empty or not required.issubset(source.columns):
        return pd.DataFrame(columns=columns)

    source = source[["course_name", "current_count", "total_count"]].copy()
    source["course_name"] = source["course_name"].astype("string").str.strip()
    for column in ("current_count", "total_count"):
        source[column] = pd.to_numeric(source[column], errors="coerce").fillna(0)
    source = source[source["course_name"].notna() & source["course_name"].ne("")]
    if source.empty:
        return pd.DataFrame(columns=columns)

    result = source.melt(
        id_vars="course_name",
        value_vars=["current_count", "total_count"],
        var_name="Measure",
        value_name="Enrollments",
    )
    result["Measure"] = result["Measure"].map({
        "current_count": "Current enrollments",
        "total_count": "All enrollments",
    })
    result["Enrollments"] = pd.to_numeric(result["Enrollments"], errors="coerce").fillna(0)
    return result[columns]
