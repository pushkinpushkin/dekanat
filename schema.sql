DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS gradebooks;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS `groups`;
DROP TABLE IF EXISTS study_programs;
DROP TABLE IF EXISTS faculties;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('DB_ADMIN','TEACHER','DEANERY','DEPUTY_DEAN','DEAN') NOT NULL,
  full_name VARCHAR(150) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE faculties (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE study_programs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  faculty_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  FOREIGN KEY (faculty_id) REFERENCES faculties(id) ON DELETE CASCADE
);

CREATE TABLE `groups` (
  id INT AUTO_INCREMENT PRIMARY KEY,
  study_program_id INT NOT NULL,
  name VARCHAR(50) NOT NULL,
  admission_year INT NOT NULL,
  FOREIGN KEY (study_program_id) REFERENCES study_programs(id) ON DELETE CASCADE
);

CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  student_number VARCHAR(50) NOT NULL UNIQUE,
  last_name VARCHAR(50) NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  patronymic VARCHAR(50),
  group_id INT NOT NULL,
  FOREIGN KEY (group_id) REFERENCES `groups`(id) ON DELETE CASCADE
);

CREATE TABLE courses (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  semester INT NOT NULL,
  hours INT NOT NULL,
  teacher_user_id INT,
  FOREIGN KEY (teacher_user_id) REFERENCES users(id)
);

CREATE TABLE gradebooks (
  id INT AUTO_INCREMENT PRIMARY KEY,
  course_id INT NOT NULL,
  group_id INT NOT NULL,
  session_year INT NOT NULL,
  session_term ENUM('WINTER','SUMMER') NOT NULL,
  status ENUM('OPEN','CLOSED','FINAL') NOT NULL DEFAULT 'OPEN',
  closed_by INT,
  closed_at DATETIME,
  finalized_by INT,
  finalized_at DATETIME,
  UNIQUE(course_id, group_id, session_year, session_term),
  FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
  FOREIGN KEY (group_id) REFERENCES `groups`(id) ON DELETE CASCADE,
  FOREIGN KEY (closed_by) REFERENCES users(id),
  FOREIGN KEY (finalized_by) REFERENCES users(id)
);

CREATE TABLE grades (
  id INT AUTO_INCREMENT PRIMARY KEY,
  gradebook_id INT NOT NULL,
  student_id INT NOT NULL,
  grade ENUM('неуд','удов','хор','отл','зач','не зач','отсутствие') NOT NULL,
  updated_by INT,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE(gradebook_id, student_id),
  FOREIGN KEY (gradebook_id) REFERENCES gradebooks(id) ON DELETE CASCADE,
  FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
  FOREIGN KEY (updated_by) REFERENCES users(id)
);
