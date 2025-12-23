INSERT INTO users (username, password_hash, role, full_name) VALUES
('admin', 'pbkdf2:sha256:260000$ZiwDB9m+bbUeOwVa48n4NQ==$0e2ae7f482c2c0d6ae36d23bb4e8a455cb5db88cc745df07837fb5e1452d697b', 'DB_ADMIN', 'Администратор БД'),
('teacher1', 'pbkdf2:sha256:260000$ssroXcZKCRF+6y6ahae0Xg==$292bbb3ed3aa1065714a6767f71a26974ea6ada40ba108c54feaac5182140634', 'TEACHER', 'Преподаватель 1'),
('deanery', 'pbkdf2:sha256:260000$CytEJHKZeSjgysDQ7vL5kA==$d1b1871f69bb5b13e52b90b8ac55d32cdba544608a4604d2ce015ac149091eab', 'DEANERY', 'Оператор деканата'),
('deputy', 'pbkdf2:sha256:260000$TjN/rJJ6gTKy9T5DhbqbXA==$a64f59e7dadba37db69d87fdb3f6550e3a3c8c70634cd4bbef3af8f506f85a17', 'DEPUTY_DEAN', 'Заместитель декана'),
('dean', 'pbkdf2:sha256:260000$TteWI7XV9v6epjHyTOCpmQ==$ebfc97d38f7a1dbc6d3c4598540078b35d8e921675065cccd14b9f946586c220', 'DEAN', 'Декан');

INSERT INTO faculties (name) VALUES ('Факультет информационных технологий');
INSERT INTO study_programs (faculty_id, name) VALUES (1, 'Прикладная информатика');
INSERT INTO `groups` (study_program_id, name, admission_year) VALUES (1, 'ПИ-101', 2023);

INSERT INTO students (student_number, last_name, first_name, patronymic, group_id) VALUES
('S001', 'Иванов', 'Иван', 'Иванович', 1),
('S002', 'Петрова', 'Анна', 'Сергеевна', 1),
('S003', 'Сидоров', 'Петр', 'Алексеевич', 1);

INSERT INTO courses (name, semester, hours, teacher_user_id) VALUES
('Базы данных', 2, 72, 2),
('Веб-разработка', 2, 72, 2),
('Алгоритмы', 1, 72, NULL);

INSERT INTO gradebooks (course_id, group_id, session_year, session_term, status) VALUES
(1, 1, 2024, 'WINTER', 'OPEN');

INSERT INTO grades (gradebook_id, student_id, grade, updated_by) VALUES
(1, 1, 'удов', 2),
(1, 2, 'хор', 2),
(1, 3, 'зач', 2);
