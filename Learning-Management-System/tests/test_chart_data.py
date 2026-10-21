import pandas as pd
import pytest
from utils.chart_data import course_popularity_long_frame, enrollment_status_frame


def test_course_popularity_converts_mixed_nullable_counts_to_long_numeric_data():
    result = course_popularity_long_frame([
        {"course_name": "Python", "current_count": None, "total_count": 4},
        {"course_name": "SQL", "current_count": "2", "total_count": float("nan")},
    ])
    assert list(result.columns) == ["course_name", "Measure", "Enrollments"]
    assert len(result) == 4
    assert pd.api.types.is_numeric_dtype(result["Enrollments"])
    python_current = result[(result.course_name == "Python") & (result.Measure == "Current enrollments")]
    assert python_current.iloc[0].Enrollments == 0


@pytest.mark.parametrize("rows", [[], None])
def test_course_popularity_empty_input_returns_empty_chart_data(rows):
    result = course_popularity_long_frame(rows)
    assert result.empty
    assert list(result.columns) == ["course_name", "Measure", "Enrollments"]


def test_enrollment_status_makes_counts_numeric_and_null_safe():
    result = enrollment_status_frame([
        {"status": "Enrolled", "count": "3"},
        {"status": "Completed", "count": None},
        {"status": None, "count": 9},
    ])
    assert result.to_dict("records") == [
        {"status": "Enrolled", "count": 3.0},
        {"status": "Completed", "count": 0.0},
    ]


def test_enrollment_status_empty_input_returns_empty_chart_data():
    result = enrollment_status_frame([])
    assert result.empty
    assert list(result.columns) == ["status", "count"]
