from db import query, execute

def all(search="", status="All", date_from=None, date_to=None):
    sql="SELECT e.enrollment_id,CONCAT_WS(' ',s.first_name,s.last_name) student,c.course_name course,e.enrollment_date,e.status,g.total_marks FROM enrollments e JOIN students s ON s.student_id=e.student_id JOIN courses c ON c.course_id=e.course_id LEFT JOIN grades g ON g.enrollment_id=e.enrollment_id WHERE (CONCAT_WS(' ',s.first_name,s.last_name) LIKE %s OR c.course_name LIKE %s)"
    p=[f"%{search}%"]*2
    if status!="All":sql+=" AND e.status=%s";p.append(status)
    if date_from is not None:sql+=" AND e.enrollment_date >= %s";p.append(date_from)
    if date_to is not None:sql+=" AND e.enrollment_date <= %s";p.append(date_to)
    return query(sql+" ORDER BY e.enrollment_date DESC,e.enrollment_id DESC",p)
def options():
    return query("SELECT student_id,CONCAT_WS(' ',first_name,last_name) AS full_name FROM students WHERE status='Active' ORDER BY last_name,first_name"), query("SELECT course_id,course_name FROM courses WHERE status='Active' ORDER BY course_name")
def create(student,course,date):return execute("INSERT INTO enrollments(student_id,course_id,enrollment_date,status) VALUES(%s,%s,%s,'Enrolled')",(student,course,date))
def update(enrollment_id,status):return execute("UPDATE enrollments SET status=%s WHERE enrollment_id=%s",(status,enrollment_id))
def delete(enrollment_id):return execute("DELETE FROM enrollments WHERE enrollment_id=%s",(enrollment_id,))
