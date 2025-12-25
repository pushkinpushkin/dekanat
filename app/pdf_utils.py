from io import BytesIO
from typing import Any, Dict

from flask import render_template, send_file


class PdfUnavailable(RuntimeError):
    """Raised when WeasyPrint is not available for PDF generation."""


def render_pdf(template_name: str, download_name: str, context: Dict[str, Any]) -> Any:
    """Render a Jinja template into PDF using WeasyPrint.

    Args:
        template_name: Name of the Jinja template to render.
        download_name: File name for the generated PDF.
        context: Template context.

    Raises:
        PdfUnavailable: If WeasyPrint cannot be imported.

    Returns:
        Flask response with PDF as attachment.
    """
    try:
        from weasyprint import HTML
    except Exception as exc:  # pragma: no cover - optional dependency
        raise PdfUnavailable("WeasyPrint is not installed") from exc

    html = render_template(template_name, **context)
    pdf_bytes = HTML(string=html).write_pdf()
    return send_file(BytesIO(pdf_bytes), download_name=download_name, as_attachment=True)
