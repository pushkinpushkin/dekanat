from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Mapping

from flask import send_file

def _font_path() -> Path:
    # app/pdf_utils.py -> app/assets/fonts/DejaVuSans.ttf
    return Path(__file__).resolve().parent / "assets" / "fonts" / "DejaVuSans.ttf"


def render_transcript_pdf(download_name: str, student: Mapping[str, Any], grades: List[Mapping[str, Any]]):
    """
    Генерирует PDF "Выписка/ведомость" для студента.
    Входные структуры совпадают с тем, что возвращает _load_transcript_data в reports.py.
    """
    from reportlab.lib import pagesizes
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib import colors

    buf = BytesIO()

    font_file = _font_path()
    if not font_file.exists():
        raise FileNotFoundError(
            f"Не найден шрифт для кириллицы: {font_file}. "
            f"Положи DejaVuSans.ttf в app/assets/fonts/DejaVuSans.ttf"
        )

    # Регистрируем шрифт один раз на процесс (безопасно повторять)
    try:
        pdfmetrics.registerFont(TTFont("DejaVuSans", str(font_file)))
    except Exception:
        # если уже зарегистрирован
        pass

    doc = SimpleDocTemplate(
        buf,
        pagesize=pagesizes.A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="Transcript",
    )

    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontName = "DejaVuSans"
    base.fontSize = 10
    base.leading = 12

    title = styles["Title"]
    title.fontName = "DejaVuSans"

    story = []

    full_name = _format_fio(student)
    group_name = student.get("group_name", "")
    program_name = student.get("program_name", "")
    faculty_name = student.get("faculty_name", "")

    story.append(Paragraph("Ведомость успеваемости", title))
    story.append(Spacer(1, 6))

    story.append(Paragraph(f"<b>Студент:</b> {full_name}", base))
    story.append(Paragraph(f"<b>Факультет:</b> {faculty_name}", base))
    story.append(Paragraph(f"<b>Направление:</b> {program_name}", base))
    story.append(Paragraph(f"<b>Группа:</b> {group_name}", base))
    story.append(Spacer(1, 10))

    # Таблица
    data = [["Дисциплина", "Год", "Сессия", "Оценка"]]
    for row in grades:
        data.append([
            row.get("course_name", "") or "",
            str(row.get("session_year", "") or ""),
            str(row.get("session_term", "") or ""),
            str(row.get("grade", "") or ""),
        ])

    table = Table(
        data,
        colWidths=[95 * mm, 20 * mm, 25 * mm, 25 * mm],
        repeatRows=1,
    )

    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    story.append(table)

    doc.build(story)
    buf.seek(0)
    return send_file(buf, download_name=download_name, as_attachment=True, mimetype="application/pdf")


def render_gradebook_pdf(download_name: str, gradebook, grades):
    from reportlab.lib import pagesizes
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib import colors
    from io import BytesIO
    from pathlib import Path

    buf = BytesIO()

    font_file = Path(__file__).resolve().parent / "assets" / "fonts" / "DejaVuSans.ttf"
    try:
        pdfmetrics.registerFont(TTFont("DejaVuSans", str(font_file)))
    except Exception:
        pass  # шрифт мог быть уже зарегистрирован

    doc = SimpleDocTemplate(
        buf,
        pagesize=pagesizes.A4,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="Gradebook",
    )

    styles = getSampleStyleSheet()
    base = styles["Normal"]
    base.fontName = "DejaVuSans"
    base.fontSize = 10
    base.leading = 12

    title = styles["Title"]
    title.fontName = "DejaVuSans"

    story = []
    story.append(Paragraph("Ведомость", title))
    story.append(Spacer(1, 6))

    course_name = gradebook.get("course_name", "")
    group_name = gradebook.get("group_name", "")
    session_year = gradebook.get("session_year", "")
    session_term = gradebook.get("session_term", "")

    story.append(Paragraph(f"<b>Дисциплина:</b> {course_name}", base))
    story.append(Paragraph(f"<b>Группа:</b> {group_name}", base))
    story.append(Paragraph(f"<b>Период:</b> {session_year} / {session_term}", base))
    story.append(Spacer(1, 10))

    table_data = [["Студент", "Оценка"]]
    for g in grades:
        student_name = _format_fio(g)

        table_data.append([student_name, (g.get("grade") or "")])

    table = Table(
        table_data,
        colWidths=[130 * mm, 30 * mm],
        repeatRows=1,
    )

    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "DejaVuSans"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 1), (1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    story.append(table)
    doc.build(story)

    buf.seek(0)
    return send_file(buf, download_name=download_name, as_attachment=True, mimetype="application/pdf")

def _format_fio(person: Mapping[str, Any]) -> str:
    # Поддерживаем оба варианта ключей: surname/name и last_name/first_name
    last = (person.get("surname") or person.get("last_name") or "").strip()
    first = (person.get("name") or person.get("first_name") or "").strip()
    pat = (person.get("patronymic") or "").strip()

    fio = " ".join(x for x in [last, first, pat] if x)
    if fio:
        return fio

    # Если внезапно есть готовое поле
    ready = (person.get("full_name") or person.get("student_name") or "").strip()
    return ready