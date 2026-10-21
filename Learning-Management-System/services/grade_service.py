from db import query, execute
from utils.validators import calculate_grade

def all():
    return query("SELECT e.enrollment_id,CONCAT_WS(' ',s.first_name,s.last_name) student,c.course_name course,e.status enrollment_status,g.grade_id,g.assignment_marks,g.quiz_marks,g.final_exam_marks,g.total_marks FROM enrollments e JOIN students s ON s.student_id=e.student_id JOIN courses c ON c.course_id=e.course_id LEFT JOIN grades g ON g.enrollment_id=e.enrollment_id ORDER BY s.last_name,s.first_name,c.course_name")
def save(enrollment_id, assignment, quiz, final_exam, grade_id=None):
    total,_=calculate_grade(assignment,quiz,final_exam)
    if grade_id:return execute("UPDATE grades SET assignment_marks=%s,quiz_marks=%s,final_exam_marks=%s WHERE grade_id=%s",(assignment,quiz,final_exam,grade_id))
    return execute("INSERT INTO grades(enrollment_id,assignment_marks,quiz_marks,final_exam_marks) VALUES(%s,%s,%s,%s)",(enrollment_id,assignment,quiz,final_exam))
