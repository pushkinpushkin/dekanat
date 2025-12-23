
def list_courses(conn):
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT c.*, u.full_name as teacher_name
        FROM courses c
        LEFT JOIN users u ON c.teacher_user_id = u.id
        ORDER BY c.name
        """
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def get_course(conn, course_id):
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM courses WHERE id=%s", (course_id,))
    row = cur.fetchone()
    cur.close()
    return row


def create_course(conn, data):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO courses (name, semester, hours, teacher_user_id) VALUES (%s,%s,%s,%s)",
        (data["name"], data["semester"], data["hours"], data.get("teacher_user_id")),
    )
    conn.commit()
    cur.close()


def update_course(conn, course_id, data):
    cur = conn.cursor()
    cur.execute(
        "UPDATE courses SET name=%s, semester=%s, hours=%s, teacher_user_id=%s WHERE id=%s",
        (data["name"], data["semester"], data["hours"], data.get("teacher_user_id"), course_id),
    )
    conn.commit()
    cur.close()
