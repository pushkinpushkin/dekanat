from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
from app.db import get_db
from app.pdf_utils import render_transcript_pdf

reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


def _load_transcript_data(student_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        """
        SELECT s.*, g.name as group_name, sp.name as program_name, f.name as faculty_name
        FROM students s
        JOIN `groups` g ON s.group_id = g.id
        JOIN study_programs sp ON g.study_program_id = sp.id
        JOIN faculties f ON sp.faculty_id = f.id
        WHERE s.id=%s
        """,
        (student_id,),
    )
    student = cur.fetchone()
    if not student:
        cur.close()
        return None, []

    cur.execute(
        """
        SELECT c.name as course_name, gb.session_year, gb.session_term, gr.grade
        FROM gradebooks gb
        JOIN courses c ON gb.course_id = c.id
        LEFT JOIN grades gr ON gr.gradebook_id = gb.id AND gr.student_id = %s
        WHERE gb.group_id = %s
        ORDER BY gb.session_year DESC, gb.session_term DESC
        """,
        (student_id, student["group_id"]),
    )
    grades = cur.fetchall()
    cur.close()
    return student, grades


@reports_bp.route("/transcript/<int:student_id>")
@login_required
def transcript(student_id):
    student, grades = _load_transcript_data(student_id)
    if not student:
        flash("Студент не найден", "warning")
        return redirect(url_for("students.list_students"))
    return render_template("report_transcript.html", student=student, grades=grades, pdf_mode=False)


@reports_bp.route("/transcript/<int:student_id>/pdf")
@login_required
def transcript_pdf(student_id):
    student, grades = _load_transcript_data(student_id)
    if not student:
        flash("Студент не найден", "warning")
        return redirect(url_for("students.list_students"))

    return render_transcript_pdf(
        download_name="transcript.pdf",
        student=student,
        grades=grades,
    )
