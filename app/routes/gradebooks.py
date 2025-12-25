from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.db import get_db
from app.permissions import require_gradebook_edit, can_close_gradebook, can_finalize_gradebook
from app.repositories import gradebooks as gb_repo
from app.pdf_utils import PdfUnavailable, render_pdf


gradebooks_bp = Blueprint("gradebooks", __name__, url_prefix="/gradebooks")


def _can_view(gradebook):
    if current_user.role == "TEACHER" and gradebook["teacher_user_id"] != current_user.id:
        flash("Можно работать только со своими ведомостями", "danger")
        return False
    return True


@gradebooks_bp.route("/")
@login_required
def list_gradebooks():
    teacher_id = current_user.id if current_user.role == "TEACHER" else None
    gradebooks = gb_repo.list_gradebooks(get_db(), teacher_id)
    return render_template("gradebooks.html", gradebooks=gradebooks)


@gradebooks_bp.route("/<int:gradebook_id>", methods=["GET", "POST"])
@login_required
def view_gradebook(gradebook_id):
    conn = get_db()
    gradebook = gb_repo.get_gradebook(conn, gradebook_id)
    if not gradebook:
        flash("Ведомость не найдена", "warning")
        return redirect(url_for("gradebooks.list_gradebooks"))
    if not _can_view(gradebook):
        return redirect(url_for("gradebooks.list_gradebooks"))

    if request.method == "POST":
        student_id = request.form.get("student_id")
        grade = request.form.get("grade")
        if require_gradebook_edit(gradebook, current_user):
            gb_repo.upsert_grade(conn, gradebook_id, student_id, grade, current_user.id)
            flash("Оценка сохранена", "success")
        else:
            flash("Редактирование запрещено", "danger")
        return redirect(url_for("gradebooks.view_gradebook", gradebook_id=gradebook_id))

    grades = gb_repo.list_grades(conn, gradebook_id)
    grade_options = ['неуд','удов','хор','отл','зач','не зач','отсутствие']
    return render_template(
        "gradebook.html",
        gradebook=gradebook,
        grades=grades,
        grade_options=grade_options,
        can_edit=require_gradebook_edit(gradebook, current_user),
        can_close=can_close_gradebook(current_user),
        can_finalize=can_finalize_gradebook(current_user),
        pdf_mode=False,
    )


@gradebooks_bp.route("/<int:gradebook_id>/close", methods=["POST"])
@login_required
def close_gradebook(gradebook_id):
    conn = get_db()
    gradebook = gb_repo.get_gradebook(conn, gradebook_id)
    if not gradebook:
        flash("Ведомость не найдена", "warning")
    elif not can_close_gradebook(current_user):
        flash("Недостаточно прав", "danger")
    else:
        gb_repo.close_gradebook(conn, gradebook_id, current_user.id)
        flash("Ведомость закрыта", "info")
    return redirect(url_for("gradebooks.view_gradebook", gradebook_id=gradebook_id))


@gradebooks_bp.route("/<int:gradebook_id>/finalize", methods=["POST"])
@login_required
def finalize_gradebook(gradebook_id):
    conn = get_db()
    gradebook = gb_repo.get_gradebook(conn, gradebook_id)
    if not gradebook:
        flash("Ведомость не найдена", "warning")
    elif not can_finalize_gradebook(current_user):
        flash("Недостаточно прав", "danger")
    else:
        gb_repo.finalize_gradebook(conn, gradebook_id, current_user.id)
        flash("Ведомость финализирована", "success")
    return redirect(url_for("gradebooks.view_gradebook", gradebook_id=gradebook_id))


@gradebooks_bp.route("/<int:gradebook_id>/pdf")
@login_required
def gradebook_pdf(gradebook_id):
    conn = get_db()
    gradebook = gb_repo.get_gradebook(conn, gradebook_id)
    if not gradebook:
        flash("Ведомость не найдена", "warning")
        return redirect(url_for("gradebooks.list_gradebooks"))
    if not _can_view(gradebook):
        return redirect(url_for("gradebooks.list_gradebooks"))

    grades = gb_repo.list_grades(conn, gradebook_id)
    try:
        return render_pdf(
            "gradebook.html",
            download_name="gradebook.pdf",
            context={
                "gradebook": gradebook,
                "grades": grades,
                "grade_options": [],
                "can_edit": False,
                "can_close": False,
                "can_finalize": False,
                "pdf_mode": True,
            },
        )
    except PdfUnavailable:
        flash("WeasyPrint не установлен. Установите зависимость или используйте печать в браузере.", "warning")
        return redirect(url_for("gradebooks.view_gradebook", gradebook_id=gradebook_id))
