from typing import Optional
from werkzeug.security import check_password_hash
from app.models.user import User


def get_by_username(conn, username: str) -> Optional[User]:
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE username=%s", (username,))
    row = cur.fetchone()
    cur.close()
    if row:
        return User(**row)
    return None


def get_by_id(conn, user_id: int) -> Optional[User]:
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
    row = cur.fetchone()
    cur.close()
    if row:
        return User(**row)
    return None


def validate_user(conn, username: str, password: str) -> Optional[User]:
    user = get_by_username(conn, username)
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


def list_teachers(conn):
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT id, full_name FROM users WHERE role='TEACHER' ORDER BY full_name")
    rows = cur.fetchall()
    cur.close()
    return rows
