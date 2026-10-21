from db import query, execute

def all(search="", status="All"):
    sql="SELECT c.course_id,c.course_name,c.description,c.instructor_id,CONCAT_WS(' ',i.first_name,i.last_name) instructor,c.duration AS duration_weeks,c.fee,c.status,COUNT(e.enrollment_id) enrollment_count FROM courses c JOIN instructors i ON i.instructor_id=c.instructor_id LEFT JOIN enrollments e ON e.course_id=c.course_id WHERE c.course_name LIKE %s"
    p=[f"%{search}%"]
    if status!="All":sql+=" AND c.status=%s";p.append(status)
    return query(sql+" GROUP BY c.course_id ORDER BY c.course_name",p)
def instructors():return query("SELECT instructor_id,CONCAT_WS(' ',first_name,last_name) AS full_name FROM instructors WHERE status='Active' ORDER BY last_name,first_name")
def save(data, course_id=None):
    if course_id:return execute("UPDATE courses SET course_name=%s,description=%s,instructor_id=%s,duration=%s,fee=%s,status=%s WHERE course_id=%s",(*data,course_id))
    return execute("INSERT INTO courses(course_name,description,instructor_id,duration,fee,status) VALUES(%s,%s,%s,%s,%s,%s)",data)
def delete(course_id):return execute("DELETE FROM courses WHERE course_id=%s",(course_id,))
