from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

ROLES = {
    "DB_ADMIN",
    "TEACHER",
    "DEANERY",
    "DEPUTY_DEAN",
    "DEAN",
}


def role_required(allowed_roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.role not in allowed_roles:
                flash("Недостаточно прав", "danger")
                return redirect(url_for("index"))
            return view(*args, **kwargs)

        return wrapped

    return decorator


def require_gradebook_edit(gradebook, user):
    if gradebook["status"] != "OPEN":
        return False
    if user.role == "TEACHER" and gradebook["teacher_user_id"] != user.id:
        return False
    if user.role in {"DEANERY", "DB_ADMIN"}:
        return True
    if user.role == "TEACHER" and gradebook["teacher_user_id"] == user.id:
        return True
    return False


def can_manage_entities(user):
    return user.role != "TEACHER"


def can_close_gradebook(user):
    return user.role in {"DEPUTY_DEAN", "DEAN", "DB_ADMIN"}


def can_finalize_gradebook(user):
    return user.role in {"DEAN", "DB_ADMIN"}
