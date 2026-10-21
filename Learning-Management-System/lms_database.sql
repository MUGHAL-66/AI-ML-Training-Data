-- LMS schema and repeatable development seed. Safe for an existing database:
-- creates/updates the LMS objects only; never drops a database or table.
CREATE DATABASE IF NOT EXISTS lms_database CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE lms_database;

CREATE TABLE IF NOT EXISTS students (
 student_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
 first_name VARCHAR(60) NOT NULL,
 last_name VARCHAR(60) NOT NULL,
 email VARCHAR(254) NOT NULL,
 phone VARCHAR(30) NULL,
 enrollment_date DATE NOT NULL,
 status ENUM('Active','Inactive','Graduated') NOT NULL DEFAULT 'Active',
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY(student_id), UNIQUE KEY uq_students_email(email), KEY ix_students_status(status)
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS instructors (
 instructor_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
 first_name VARCHAR(60) NOT NULL,
 last_name VARCHAR(60) NOT NULL,
 email VARCHAR(254) NOT NULL,
 specialization VARCHAR(120) NOT NULL,
 status ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY(instructor_id), UNIQUE KEY uq_instructors_email(email), KEY ix_instructors_status(status)
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS courses (
 course_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
 course_name VARCHAR(160) NOT NULL,
 description TEXT NULL,
 instructor_id INT UNSIGNED NOT NULL,
 duration SMALLINT UNSIGNED NOT NULL,
 fee DECIMAL(10,2) NOT NULL DEFAULT 0,
 status ENUM('Active','Inactive','Completed') NOT NULL DEFAULT 'Active',
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY(course_id), UNIQUE KEY uq_courses_name(course_name), KEY ix_courses_instructor(instructor_id),
 CONSTRAINT chk_course_duration CHECK(duration > 0), CONSTRAINT chk_course_fee CHECK(fee >= 0),
 CONSTRAINT fk_courses_instructor FOREIGN KEY(instructor_id) REFERENCES instructors(instructor_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS enrollments (
 enrollment_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
 student_id INT UNSIGNED NOT NULL,
 course_id INT UNSIGNED NOT NULL,
 enrollment_date DATE NOT NULL,
 status ENUM('Enrolled','Completed','Dropped') NOT NULL DEFAULT 'Enrolled',
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 PRIMARY KEY(enrollment_id), UNIQUE KEY uq_student_course(student_id,course_id), KEY ix_enrollment_course(course_id), KEY ix_enrollment_date(enrollment_date), KEY ix_enrollment_status(status),
 CONSTRAINT fk_enrollments_student FOREIGN KEY(student_id) REFERENCES students(student_id) ON DELETE RESTRICT ON UPDATE CASCADE,
 CONSTRAINT fk_enrollments_course FOREIGN KEY(course_id) REFERENCES courses(course_id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS grades (
 grade_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
 enrollment_id INT UNSIGNED NOT NULL,
 assignment_marks DECIMAL(5,2) NOT NULL,
 quiz_marks DECIMAL(5,2) NOT NULL,
 final_exam_marks DECIMAL(5,2) NOT NULL,
 total_marks DECIMAL(6,2) GENERATED ALWAYS AS (assignment_marks+quiz_marks+final_exam_marks) STORED,
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
 PRIMARY KEY(grade_id), UNIQUE KEY uq_grade_enrollment(enrollment_id),
 CONSTRAINT chk_grade_assignment CHECK(assignment_marks BETWEEN 0 AND 20),
 CONSTRAINT chk_grade_quiz CHECK(quiz_marks BETWEEN 0 AND 20),
 CONSTRAINT chk_grade_final CHECK(final_exam_marks BETWEEN 0 AND 60),
 CONSTRAINT fk_grades_enrollment FOREIGN KEY(enrollment_id) REFERENCES enrollments(enrollment_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB;

-- Stable unique identifiers make seed rows safe to rerun without duplication.
INSERT INTO instructors(first_name,last_name,email,specialization,status) VALUES
 ('Aisha','Rahman','aisha.rahman@example.edu','Data Science','Active'),
 ('Bilal','Khan','bilal.khan@example.edu','Software Engineering','Active'),
 ('Sara','Ahmed','sara.ahmed@example.edu','Business Analytics','Active')
ON DUPLICATE KEY UPDATE first_name=VALUES(first_name),last_name=VALUES(last_name),specialization=VALUES(specialization),status=VALUES(status);
INSERT INTO students(first_name,last_name,email,enrollment_date,status) VALUES
 ('Maya','Hassan','maya.hassan@example.edu','2026-01-12','Active'),('Omar','Farooq','omar.farooq@example.edu','2026-01-15','Active'),
 ('Zara','Malik','zara.malik@example.edu','2026-02-02','Active'),('Hamza','Ali','hamza.ali@example.edu','2025-09-01','Active'),
 ('Noor','Siddiqui','noor.siddiqui@example.edu','2025-08-28','Graduated'),('Ibrahim','Shah','ibrahim.shah@example.edu','2026-03-04','Inactive')
ON DUPLICATE KEY UPDATE first_name=VALUES(first_name),last_name=VALUES(last_name),status=VALUES(status);
INSERT INTO courses(course_name,description,instructor_id,duration,fee,status)
SELECT seed.course_name,seed.description,i.instructor_id,seed.duration,seed.fee,'Active'
FROM (SELECT 'Data Foundations' course_name,'Core data analysis and SQL.' description,'aisha.rahman@example.edu' instructor_email,8 duration,18000.00 fee UNION ALL
 SELECT 'Python Application Development','Build maintainable Python applications.','bilal.khan@example.edu',10,22000.00 UNION ALL
 SELECT 'Business Intelligence','Reporting and decision support.','sara.ahmed@example.edu',6,16000.00 UNION ALL
 SELECT 'Machine Learning Essentials','Supervised learning and model evaluation.','aisha.rahman@example.edu',12,28000.00 UNION ALL
 SELECT 'Product Analytics','Metrics, experiments, and insights.','sara.ahmed@example.edu',5,14000.00) seed
JOIN instructors i ON i.email=seed.instructor_email
ON DUPLICATE KEY UPDATE description=VALUES(description),instructor_id=VALUES(instructor_id),duration=VALUES(duration),fee=VALUES(fee);
INSERT INTO enrollments(student_id,course_id,enrollment_date,status)
SELECT s.student_id,c.course_id,x.enrollment_date,x.status FROM (
 SELECT 'maya.hassan@example.edu' email,'Data Foundations' course,'2026-01-16' enrollment_date,'Completed' status UNION ALL
 SELECT 'maya.hassan@example.edu','Python Application Development','2026-02-01','Enrolled' UNION ALL
 SELECT 'omar.farooq@example.edu','Data Foundations','2026-01-17','Completed' UNION ALL
 SELECT 'omar.farooq@example.edu','Business Intelligence','2026-02-10','Enrolled' UNION ALL
 SELECT 'zara.malik@example.edu','Python Application Development','2026-02-04','Enrolled' UNION ALL
 SELECT 'zara.malik@example.edu','Machine Learning Essentials','2026-03-01','Enrolled' UNION ALL
 SELECT 'hamza.ali@example.edu','Data Foundations','2025-09-05','Completed' UNION ALL
 SELECT 'hamza.ali@example.edu','Business Intelligence','2025-09-08','Dropped' UNION ALL
 SELECT 'noor.siddiqui@example.edu','Python Application Development','2025-09-02','Completed' UNION ALL
 SELECT 'ibrahim.shah@example.edu','Machine Learning Essentials','2026-03-06','Enrolled'
) x JOIN students s ON s.email=x.email JOIN courses c ON c.course_name=x.course
ON DUPLICATE KEY UPDATE enrollment_date=VALUES(enrollment_date),status=VALUES(status);
INSERT INTO grades(enrollment_id,assignment_marks,quiz_marks,final_exam_marks)
SELECT e.enrollment_id,x.assignment_marks,x.quiz_marks,x.final_exam_marks FROM (
 SELECT 'maya.hassan@example.edu' email,'Data Foundations' course,18.00 assignment_marks,17.00 quiz_marks,54.00 final_exam_marks UNION ALL
 SELECT 'omar.farooq@example.edu','Data Foundations',16.00,18.00,48.00 UNION ALL
 SELECT 'hamza.ali@example.edu','Data Foundations',14.00,15.00,42.00 UNION ALL
 SELECT 'maya.hassan@example.edu','Python Application Development',19.00,18.00,56.00 UNION ALL
 SELECT 'noor.siddiqui@example.edu','Python Application Development',17.00,16.00,49.00
) x JOIN students s ON s.email=x.email JOIN courses c ON c.course_name=x.course JOIN enrollments e ON e.student_id=s.student_id AND e.course_id=c.course_id
ON DUPLICATE KEY UPDATE assignment_marks=VALUES(assignment_marks),quiz_marks=VALUES(quiz_marks),final_exam_marks=VALUES(final_exam_marks);
