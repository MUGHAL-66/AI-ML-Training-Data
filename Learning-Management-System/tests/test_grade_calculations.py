from decimal import Decimal
import pytest
from utils.validators import calculate_grade

def test_total_is_decimal_and_capped_by_components():
    total,band=calculate_grade("19.5","18","57.25")
    assert total == Decimal("94.75")
    assert band == "A"

def test_grade_boundary_below_a():
    assert calculate_grade(20,20,44)[1] == "B"

def test_non_numeric_marks_rejected():
    with pytest.raises(Exception): calculate_grade("many",0,0)
