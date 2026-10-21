from db import query, execute
from utils.validators import split_person_name

def all(search="", status="All"):
    sql = "SELECT student_id, first_name, last_name, CONCAT_WS(' ', first_name, last_name) AS full_name, email, phone, enrollment_date, status FROM students WHERE (CONCAT_WS(' ', first_name, last_name) LIKE %s OR email LIKE %s)"
    params = [f"%{search}%", f"%{search}%"]
    if status != "All": sql += " AND status=%s"; params.append(status)
    return query(sql + " ORDER BY last_name, first_name", params)
def save(data, student_id=None):
    first_name, last_name = split_person_name(data[0])
    values = (first_name, last_name, *data[1:])
    if student_id: return execute("UPDATE students SET first_name=%s,last_name=%s,email=%s,phone=%s,enrollment_date=%s,status=%s WHERE student_id=%s", (*values, student_id))
    return execute("INSERT INTO students(first_name,last_name,email,phone,enrollment_date,status) VALUES(%s,%s,%s,%s,%s,%s)", values)
def delete(student_id): return execute("DELETE FROM students WHERE student_id=%s", (student_id,))
