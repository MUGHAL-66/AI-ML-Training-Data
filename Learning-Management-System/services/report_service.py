from db import query, one

def dashboard():
    return {
      "students":one("SELECT COUNT(*) n FROM students")["n"],"active":one("SELECT COUNT(*) n FROM students WHERE status='Active'")["n"],
      "instructors":one("SELECT COUNT(*) n FROM instructors")["n"],"courses":one("SELECT COUNT(*) n FROM courses")["n"],
      "enrollments":query("SELECT status,COUNT(*) count FROM enrollments GROUP BY status"),
      "average":one("SELECT AVG(total_marks) avg FROM grades")["avg"],
      "popular":query("SELECT c.course_name, SUM(e.status='Enrolled') current_count,COUNT(e.enrollment_id) total_count FROM courses c LEFT JOIN enrollments e ON e.course_id=c.course_id GROUP BY c.course_id ORDER BY current_count DESC,c.course_name"),
      "recent":query("SELECT CONCAT_WS(' ',s.first_name,s.last_name) student,c.course_name course,e.enrollment_date,e.status FROM enrollments e JOIN students s ON s.student_id=e.student_id JOIN courses c ON c.course_id=e.course_id ORDER BY e.enrollment_date DESC,e.enrollment_id DESC LIMIT 8"),
      "top":query("SELECT CONCAT_WS(' ',s.first_name,s.last_name) full_name,AVG(g.total_marks) average_marks,COUNT(g.grade_id) recorded_grades FROM students s LEFT JOIN enrollments e ON e.student_id=s.student_id LEFT JOIN grades g ON g.enrollment_id=e.enrollment_id GROUP BY s.student_id,s.first_name,s.last_name HAVING COUNT(g.grade_id)>0 ORDER BY average_marks DESC LIMIT 8"),
      "workload":query("SELECT CONCAT_WS(' ',i.first_name,i.last_name) full_name,COUNT(c.course_id) course_count FROM instructors i LEFT JOIN courses c ON c.instructor_id=i.instructor_id GROUP BY i.instructor_id,i.first_name,i.last_name ORDER BY course_count DESC,i.last_name,i.first_name")}

def reports():
    return {
      "BR-01 · Course popularity":("Courses with highest current and historical enrollment", "SELECT c.course_name,SUM(e.status='Enrolled') current_enrollments,COUNT(e.enrollment_id) all_enrollments FROM courses c LEFT JOIN enrollments e ON e.course_id=c.course_id GROUP BY c.course_id ORDER BY current_enrollments DESC,all_enrollments DESC"),
      "BR-02 · Instructor workload":("Courses assigned to each instructor, including instructors with none", "SELECT CONCAT_WS(' ',i.first_name,i.last_name) instructor,COUNT(c.course_id) course_count FROM instructors i LEFT JOIN courses c ON c.instructor_id=i.instructor_id GROUP BY i.instructor_id,i.first_name,i.last_name ORDER BY course_count DESC,i.last_name,i.first_name"),
      "BR-03 · Top performers":("Average across recorded grades; students without a grade are excluded", "SELECT CONCAT_WS(' ',s.first_name,s.last_name) full_name,ROUND(AVG(g.total_marks),2) average_marks,COUNT(g.grade_id) grades_recorded FROM students s JOIN enrollments e ON e.student_id=s.student_id JOIN courses c ON c.course_id=e.course_id JOIN grades g ON g.enrollment_id=e.enrollment_id GROUP BY s.student_id,s.first_name,s.last_name ORDER BY average_marks DESC"),
      "BR-04 · Active students":("Count of students whose status is Active", "SELECT COUNT(*) active_students FROM students WHERE status='Active'"),
      "BR-05 · Enrollment status":("Distribution across Enrolled, Completed, and Dropped", "SELECT status,COUNT(*) enrollments FROM enrollments GROUP BY status ORDER BY status"),
      "BR-06 · Courses without enrollments":("Courses with no enrollment history", "SELECT c.course_id,c.course_name,CONCAT_WS(' ',i.first_name,i.last_name) instructor FROM courses c JOIN instructors i ON i.instructor_id=c.instructor_id LEFT JOIN enrollments e ON e.course_id=c.course_id WHERE e.enrollment_id IS NULL ORDER BY c.course_name")}
