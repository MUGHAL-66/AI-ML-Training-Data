from db import query, execute
from utils.validators import split_person_name

def all(search="", status="All"):
    sql = "SELECT i.instructor_id,i.first_name,i.last_name,CONCAT_WS(' ',i.first_name,i.last_name) AS full_name,i.email,i.specialization,i.status,COUNT(c.course_id) course_count FROM instructors i LEFT JOIN courses c ON c.instructor_id=i.instructor_id WHERE (CONCAT_WS(' ',i.first_name,i.last_name) LIKE %s OR i.email LIKE %s OR i.specialization LIKE %s)"
    p=[f"%{search}%"]*3
    if status!="All": sql+=" AND i.status=%s"; p.append(status)
    return query(sql+" GROUP BY i.instructor_id ORDER BY i.last_name,i.first_name",p)
def save(data, instructor_id=None):
    first_name,last_name=split_person_name(data[0]);values=(first_name,last_name,*data[1:])
    if instructor_id:return execute("UPDATE instructors SET first_name=%s,last_name=%s,email=%s,specialization=%s,status=%s WHERE instructor_id=%s",(*values,instructor_id))
    return execute("INSERT INTO instructors(first_name,last_name,email,specialization,status) VALUES(%s,%s,%s,%s,%s)",values)
def delete(instructor_id):return execute("DELETE FROM instructors WHERE instructor_id=%s",(instructor_id,))
