USE lms_db;
-- BR-01 Courses with most enrolled students
SELECT c.course_name, COUNT(e.enrollment_id) AS total_enrollments
FROM courses c JOIN enrollments e ON e.course_id = c.course_id
GROUP BY c.course_id, c.course_name ORDER BY total_enrollments DESC;

-- BR-02 Courses per instructor
SELECT i.full_name AS instructor, COUNT(c.course_id) AS courses_taught
FROM instructors i LEFT JOIN courses c ON c.instructor_id = i.instructor_id
GROUP BY i.instructor_id, i.full_name ORDER BY courses_taught DESC;

-- BR-03 Students with highest total marks
SELECT s.full_name, SUM(g.total_marks) AS total_marks
FROM students s JOIN enrollments e ON e.student_id = s.student_id
JOIN grades g ON g.enrollment_id = e.enrollment_id
GROUP BY s.student_id, s.full_name ORDER BY total_marks DESC;

-- BR-04 Active students
SELECT COUNT(*) AS active_students FROM students WHERE status = 'Active';

-- BR-05 Enrollment status counts
SELECT status, COUNT(*) AS total FROM enrollments GROUP BY status;

-- BR-06 Courses with no students
SELECT c.course_name FROM courses c
LEFT JOIN enrollments e ON e.course_id = c.course_id
WHERE e.enrollment_id IS NULL;
