from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.db import get_db
from app.permissions import can_manage_entities
from app.repositories import courses as courses_repo
from app.repositories.users import list_teachers

courses_bp = Blueprint("courses", __name__, url_prefix="/courses")


def _ensure_can_manage():
    if not can_manage_entities(current_user):
        flash("Недостаточно прав для изменения дисциплин", "danger")
        return False
    return True


@courses_bp.route("/")
@login_required
def list_courses():
    courses = courses_repo.list_courses(get_db())
    return render_template("courses.html", courses=courses)


@courses_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_course():
    if request.method == "POST":
        if not _ensure_can_manage():
            return redirect(url_for("courses.list_courses"))
        try:
            courses_repo.create_course(get_db(), request.form)
            flash("Дисциплина добавлена", "success")
            return redirect(url_for("courses.list_courses"))
        except Exception as exc:
            flash(f"Ошибка: {exc}", "danger")
    teachers = list_teachers(get_db())
    return render_template("course_form.html", teachers=teachers)


@courses_bp.route("/<int:course_id>/edit", methods=["GET", "POST"])
@login_required
def edit_course(course_id):
    conn = get_db()
    course = courses_repo.get_course(conn, course_id)
    if not course:
        flash("Дисциплина не найдена", "warning")
        return redirect(url_for("courses.list_courses"))
    if request.method == "POST":
        if not _ensure_can_manage():
            return redirect(url_for("courses.list_courses"))
        try:
            courses_repo.update_course(conn, course_id, request.form)
            flash("Дисциплина обновлена", "success")
            return redirect(url_for("courses.list_courses"))
        except Exception as exc:
            flash(f"Ошибка: {exc}", "danger")
    teachers = list_teachers(conn)
    return render_template("course_form.html", course=course, teachers=teachers)
