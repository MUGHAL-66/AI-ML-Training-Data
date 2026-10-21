import pytest
from utils.validators import required, valid_email, valid_phone, valid_duration, valid_fee, valid_status, calculate_grade

def test_required_and_email():
    with pytest.raises(ValueError): required("   ","Name")
    assert valid_email("Student@Example.edu") == "student@example.edu"
    with pytest.raises(ValueError): valid_email("not-an-email")

def test_phone_duration_fee_and_status():
    assert valid_phone("+1 (555) 123-4567") == "+1 (555) 123-4567"
    assert valid_phone("") is None
    with pytest.raises(ValueError): valid_duration(0)
    with pytest.raises(ValueError): valid_fee(-1)
    assert valid_status("student","Active") == "Active"
    with pytest.raises(ValueError): valid_status("student","Unknown")

@pytest.mark.parametrize("assignment,quiz,final_exam,total,band",[
    (0,0,0,0,"F"),(8,8,24,40,"D"),(15,10,30,55,"C"),
    (15,15,40,70,"B"),(20,10,55,85,"A"),(20,20,60,100,"A")])
def test_grade_boundaries(assignment,quiz,final_exam,total,band):
    result,actual=calculate_grade(assignment,quiz,final_exam)
    assert result == total
    assert actual == band

@pytest.mark.parametrize("marks",[(-.1,0,0),(20.1,0,0),(0,20.1,0),(0,0,60.1)])
def test_invalid_marks(marks):
    with pytest.raises(ValueError): calculate_grade(*marks)
