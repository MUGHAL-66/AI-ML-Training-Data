-- LMS Database | MySQL 8+
DROP DATABASE IF EXISTS lms_db;
CREATE DATABASE lms_db CHARACTER SET utf8mb4;
USE lms_db;

CREATE TABLE students (
  student_id      INT AUTO_INCREMENT PRIMARY KEY,
  full_name       VARCHAR(100) NOT NULL,
  email           VARCHAR(120) NOT NULL UNIQUE,
  phone           VARCHAR(20),
  enrollment_date DATE NOT NULL,
  status          ENUM('Active','Inactive','Graduated') NOT NULL DEFAULT 'Active'
);

CREATE TABLE instructors (
  instructor_id  INT AUTO_INCREMENT PRIMARY KEY,
  full_name      VARCHAR(100) NOT NULL,
  specialization VARCHAR(100) NOT NULL,
  email          VARCHAR(120) NOT NULL UNIQUE,
  status         ENUM('Active','Inactive') NOT NULL DEFAULT 'Active'
);

CREATE TABLE courses (
  course_id      INT AUTO_INCREMENT PRIMARY KEY,
  course_name    VARCHAR(120) NOT NULL UNIQUE,
  description    TEXT,
  instructor_id  INT NOT NULL,
  duration_weeks INT NOT NULL CHECK (duration_weeks > 0),
  fee            DECIMAL(10,2) NOT NULL CHECK (fee >= 0),
  status         ENUM('Active','Inactive') NOT NULL DEFAULT 'Active',
  FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
);

CREATE TABLE enrollments (
  enrollment_id   INT AUTO_INCREMENT PRIMARY KEY,
  student_id      INT NOT NULL,
  course_id       INT NOT NULL,
  enrollment_date DATE NOT NULL,
  status          ENUM('Enrolled','Completed','Dropped') NOT NULL DEFAULT 'Enrolled',
  UNIQUE (student_id, course_id),
  FOREIGN KEY (student_id) REFERENCES students(student_id),
  FOREIGN KEY (course_id)  REFERENCES courses(course_id)
);

CREATE TABLE grades (
  grade_id          INT AUTO_INCREMENT PRIMARY KEY,
  enrollment_id     INT NOT NULL UNIQUE,
  assignment_marks  DECIMAL(5,2) NOT NULL DEFAULT 0 CHECK (assignment_marks BETWEEN 0 AND 30),
  quiz_marks        DECIMAL(5,2) NOT NULL DEFAULT 0 CHECK (quiz_marks BETWEEN 0 AND 20),
  final_marks       DECIMAL(5,2) NOT NULL DEFAULT 0 CHECK (final_marks BETWEEN 0 AND 50),
  total_marks       DECIMAL(5,2) AS (assignment_marks + quiz_marks + final_marks) STORED,
  FOREIGN KEY (enrollment_id) REFERENCES enrollments(enrollment_id) ON DELETE CASCADE
);

-- Sample data
INSERT INTO students (full_name,email,phone,enrollment_date,status) VALUES
('Ayesha Khan','ayesha@mail.com','0300-1111111','2026-01-10','Active'),
('Bilal Ahmed','bilal@mail.com','0301-2222222','2026-01-12','Active'),
('Sara Malik','sara@mail.com','0302-3333333','2026-02-01','Active'),
('Usman Tariq','usman@mail.com','0303-4444444','2026-02-15','Inactive'),
('Hina Raza','hina@mail.com','0304-5555555','2026-03-03','Active'),
('Zain Ali','zain@mail.com','0305-6666666','2026-03-20','Graduated');

INSERT INTO instructors (full_name,specialization,email,status) VALUES
('Dr. Imran Shah','Databases','imran@lms.com','Active'),
('Ms. Farah Noor','Python Programming','farah@lms.com','Active'),
('Mr. Hamza Qureshi','Web Development','hamza@lms.com','Active'),
('Ms. Rabia Iqbal','Data Science','rabia@lms.com','Inactive');

INSERT INTO courses (course_name,description,instructor_id,duration_weeks,fee,status) VALUES
('MySQL Fundamentals','Relational design and SQL',1,8,15000,'Active'),
('Python for Beginners','Core Python',2,10,18000,'Active'),
('Web Development','HTML, CSS, JS',3,12,22000,'Active'),
('Data Analysis with Pandas','Pandas and charts',2,6,16000,'Active'),
('Machine Learning Intro','ML basics',4,10,25000,'Inactive');

INSERT INTO enrollments (student_id,course_id,enrollment_date,status) VALUES
(1,1,'2026-01-15','Completed'),(1,2,'2026-02-01','Enrolled'),
(2,1,'2026-01-20','Completed'),(2,3,'2026-02-10','Enrolled'),
(3,2,'2026-02-05','Enrolled'),(3,1,'2026-02-06','Dropped'),
(4,3,'2026-02-20','Dropped'),(5,2,'2026-03-05','Enrolled'),
(5,4,'2026-03-06','Enrolled'),(6,1,'2026-03-22','Completed');

INSERT INTO grades (enrollment_id,assignment_marks,quiz_marks,final_marks) VALUES
(1,27,18,45),(3,22,15,38),(10,25,17,42),(2,20,12,30),(5,24,16,35);
