from datetime import datetime


def list_gradebooks(conn, teacher_id=None):
    cur = conn.cursor(dictionary=True)
    params = []
    query = (
        """
        SELECT gb.*, c.name as course_name, c.teacher_user_id, g.name as group_name
        FROM gradebooks gb
        JOIN courses c ON gb.course_id = c.id
        JOIN `groups` g ON gb.group_id = g.id
        """
    )
    if teacher_id:
        query += " WHERE c.teacher_user_id = %s"
        params.append(teacher_id)
    query += " ORDER BY gb.session_year DESC, gb.session_term DESC"
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    return rows


def get_gradebook(conn, gradebook_id):
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT gb.*, c.name as course_name, c.teacher_user_id, g.name as group_name
        FROM gradebooks gb
        JOIN courses c ON gb.course_id = c.id
        JOIN `groups` g ON gb.group_id = g.id
        WHERE gb.id=%s
        """,
        (gradebook_id,),
    )
    row = cur.fetchone()
    cur.close()
    return row


def list_grades(conn, gradebook_id):
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT s.id as student_id, s.last_name, s.first_name, s.patronymic, gr.grade
        FROM students s
        JOIN `groups` g ON s.group_id = g.id
        JOIN gradebooks gb ON gb.group_id = g.id
        LEFT JOIN grades gr ON gr.student_id = s.id AND gr.gradebook_id = gb.id
        WHERE gb.id=%s
        ORDER BY s.last_name, s.first_name
        """,
        (gradebook_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def upsert_grade(conn, gradebook_id, student_id, grade, user_id):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO grades (gradebook_id, student_id, grade, updated_by, updated_at)
        VALUES (%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE grade=VALUES(grade), updated_by=VALUES(updated_by), updated_at=VALUES(updated_at)
        """,
        (gradebook_id, student_id, grade, user_id, datetime.utcnow()),
    )
    conn.commit()
    cur.close()


def close_gradebook(conn, gradebook_id, user_id):
    cur = conn.cursor()
    cur.execute(
        "UPDATE gradebooks SET status='CLOSED', closed_by=%s, closed_at=%s WHERE id=%s AND status='OPEN'",
        (user_id, datetime.utcnow(), gradebook_id),
    )
    conn.commit()
    cur.close()


def finalize_gradebook(conn, gradebook_id, user_id):
    cur = conn.cursor()
    cur.execute(
        "UPDATE gradebooks SET status='FINAL', finalized_by=%s, finalized_at=%s WHERE id=%s AND status='CLOSED'",
        (user_id, datetime.utcnow(), gradebook_id),
    )
    conn.commit()
    cur.close()
