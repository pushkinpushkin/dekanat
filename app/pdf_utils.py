from io import BytesIO
from typing import Any, Dict

from flask import render_template, send_file


class PdfUnavailable(RuntimeError):
    """Raised when PDF generation is not available."""


def _render_with_weasyprint(html: str) -> bytes:
    from weasyprint import HTML  # type: ignore

    return HTML(string=html).write_pdf()


def _render_with_pisa(html: str) -> bytes:
    from xhtml2pdf import pisa  # type: ignore

    result = BytesIO()
    status = pisa.CreatePDF(html, dest=result)  # pragma: no cover - external lib
    if status.err:
        raise PdfUnavailable("xhtml2pdf failed to render PDF")
    return result.getvalue()


def render_pdf(template_name: str, download_name: str, context: Dict[str, Any]) -> Any:
    """Render a Jinja template into PDF using available engines.

    Prefers WeasyPrint if installed (for better CSS support),
    otherwise falls back to pure-Python xhtml2pdf.
    """
    html = render_template(template_name, **context)

    renderers = (_render_with_weasyprint, _render_with_pisa)
    last_error: Exception | None = None
    for renderer in renderers:
        try:
            pdf_bytes = renderer(html)
            return send_file(BytesIO(pdf_bytes), download_name=download_name, as_attachment=True)
        except Exception as exc:  # pragma: no cover - optional deps
            last_error = exc
            continue
    raise PdfUnavailable(f"PDF generation failed: {last_error}")
