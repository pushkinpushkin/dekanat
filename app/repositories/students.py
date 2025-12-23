
def list_students(conn):
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT s.*, g.name as group_name, sp.name as program_name, f.name as faculty_name
        FROM students s
        JOIN `groups` g ON s.group_id = g.id
        JOIN study_programs sp ON g.study_program_id = sp.id
        JOIN faculties f ON sp.faculty_id = f.id
        ORDER BY s.last_name, s.first_name
        """
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def get_student(conn, student_id):
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM students WHERE id=%s", (student_id,))
    row = cur.fetchone()
    cur.close()
    return row


def create_student(conn, data):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students (student_number, last_name, first_name, patronymic, group_id) VALUES (%s,%s,%s,%s,%s)",
        (
            data["student_number"],
            data["last_name"],
            data["first_name"],
            data.get("patronymic"),
            data["group_id"],
        ),
    )
    conn.commit()
    cur.close()


def update_student(conn, student_id, data):
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE students SET student_number=%s, last_name=%s, first_name=%s, patronymic=%s, group_id=%s
        WHERE id=%s
        """,
        (
            data["student_number"],
            data["last_name"],
            data["first_name"],
            data.get("patronymic"),
            data["group_id"],
            student_id,
        ),
    )
    conn.commit()
    cur.close()


def delete_student(conn, student_id):
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    cur.close()


def list_groups(conn):
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT g.id, g.name, g.admission_year, sp.name as program_name, f.name as faculty_name
        FROM `groups` g
        JOIN study_programs sp ON g.study_program_id = sp.id
        JOIN faculties f ON sp.faculty_id = f.id
        ORDER BY f.name, sp.name, g.name
        """
    )
    rows = cur.fetchall()
    cur.close()
    return rows
