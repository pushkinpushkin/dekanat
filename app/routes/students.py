from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.db import get_db
from app.permissions import can_manage_entities
from app.repositories import students as students_repo

students_bp = Blueprint("students", __name__, url_prefix="/students")


def _ensure_can_manage():
    if not can_manage_entities(current_user):
        flash("Недостаточно прав для изменения студентов", "danger")
        return False
    return True


@students_bp.route("/")
@login_required
def list_students():
    conn = get_db()
    students = students_repo.list_students(conn)
    return render_template("students.html", students=students)


@students_bp.route("/new", methods=["GET", "POST"])
@login_required
def create_student():
    if request.method == "POST":
        if not _ensure_can_manage():
            return redirect(url_for("students.list_students"))
        try:
            students_repo.create_student(get_db(), request.form)
            flash("Студент добавлен", "success")
            return redirect(url_for("students.list_students"))
        except Exception as exc:  # short educational handling
            flash(f"Ошибка: {exc}", "danger")
    groups = students_repo.list_groups(get_db())
    return render_template("student_form.html", groups=groups)


@students_bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    conn = get_db()
    student = students_repo.get_student(conn, student_id)
    if not student:
        flash("Студент не найден", "warning")
        return redirect(url_for("students.list_students"))
    if request.method == "POST":
        if not _ensure_can_manage():
            return redirect(url_for("students.list_students"))
        try:
            students_repo.update_student(conn, student_id, request.form)
            flash("Данные обновлены", "success")
            return redirect(url_for("students.list_students"))
        except Exception as exc:
            flash(f"Ошибка: {exc}", "danger")
    groups = students_repo.list_groups(conn)
    return render_template("student_form.html", student=student, groups=groups)


@students_bp.route("/<int:student_id>/delete", methods=["POST"])
@login_required
def delete_student(student_id):
    if not _ensure_can_manage():
        return redirect(url_for("students.list_students"))
    try:
        students_repo.delete_student(get_db(), student_id)
        flash("Студент удален", "info")
    except Exception as exc:
        flash(f"Ошибка удаления: {exc}", "danger")
    return redirect(url_for("students.list_students"))
