from io import BytesIO
from typing import Any, Dict

from flask import render_template, send_file


class PdfUnavailable(RuntimeError):
    """Raised when PDF generation is not available."""


def _render_with_weasyprint(html: str) -> bytes:
    from weasyprint import HTML  # type: ignore

    return HTML(string=html).write_pdf()


def _render_with_pypdf(html: str) -> bytes:
    from pypdf import PdfWriter  # type: ignore
    from pypdf.generic import DictionaryObject, NameObject, StreamObject  # type: ignore

    writer = PdfWriter()
    page = writer.add_blank_page(width=612, height=792)  # US Letter

    # Use a built-in font so no system fonts are required.
    font = writer._get_standard_font("Helvetica")  # type: ignore[attr-defined]
    resources = DictionaryObject()
    resources[NameObject("/Font")] = DictionaryObject({NameObject(font.name): font})
    page[NameObject("/Resources")] = resources

    # Strip tags and place the text onto the page as a simple fallback.
    import re

    plain_text = re.sub(r"<[^>]+>", "", html)
    escaped_text = (
        plain_text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    )
    content = f"BT /{font.name} 12 Tf 72 720 Td ({escaped_text}) Tj ET"
    stream = StreamObject()
    stream._data = content.encode("utf-8")
    page[NameObject("/Contents")] = writer._add_object(stream)

    result = BytesIO()
    writer.write(result)
    return result.getvalue()


def render_pdf(template_name: str, download_name: str, context: Dict[str, Any]) -> Any:
    """Render a Jinja template into PDF using available engines.

    Prefers WeasyPrint if installed (for better CSS support),
    otherwise falls back to pure-Python pypdf (text-only fallback).
    """
    html = render_template(template_name, **context)

    renderers = (_render_with_weasyprint, _render_with_pypdf)
    last_error: Exception | None = None
    for renderer in renderers:
        try:
            pdf_bytes = renderer(html)
            return send_file(BytesIO(pdf_bytes), download_name=download_name, as_attachment=True)
        except Exception as exc:  # pragma: no cover - optional deps
            last_error = exc
            continue
    raise PdfUnavailable(f"PDF generation failed: {last_error}")
