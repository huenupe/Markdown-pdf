"""PDF → Markdown (local, con pérdida). Ver docs/12-PDF-TO-MD.md."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf
import pymupdf4llm

LOSSY_WARNING = (
    "Conversión con pérdida: revisá títulos, tablas e imágenes. "
    "No recupera el Markdown original ni el layout exacto."
)


class PdfImportError(Exception):
    """Error de importación controlado."""

    def __init__(self, message: str, *, code: str = "error") -> None:
        super().__init__(message)
        self.code = code


@dataclass
class PdfImportResult:
    markdown: str
    filename: str
    pages: int
    source: str
    warnings: list[str] = field(default_factory=list)


def _suggested_md_name(source_name: str | None) -> str:
    if not source_name or not source_name.strip():
        return "documento.md"
    base = Path(source_name.strip()).stem or "documento"
    return f"{base}.md"


def _has_extractable_text(doc: pymupdf.Document) -> bool:
    for page in doc:
        text = page.get_text("text") or ""
        if text.strip():
            return True
    return False


def _normalize_markdown(md: str) -> str:
    text = md.replace("\r\n", "\n").replace("\r", "\n").strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def pdf_bytes_to_markdown(data: bytes, source_name: str | None = None) -> PdfImportResult:
    if not data:
        raise PdfImportError("El archivo PDF está vacío.", code="empty")

    source = Path(source_name or "documento.pdf").name
    if not source.lower().endswith(".pdf"):
        source = f"{Path(source).stem or 'documento'}.pdf"

    try:
        doc = pymupdf.open(stream=data, filetype="pdf")
    except Exception as exc:  # noqa: BLE001
        raise PdfImportError(
            f"No se pudo abrir el PDF: {exc}",
            code="invalid",
        ) from exc

    try:
        if doc.page_count < 1:
            raise PdfImportError("El PDF no tiene páginas.", code="empty")

        if not _has_extractable_text(doc):
            raise PdfImportError(
                "El PDF no tiene texto extraíble (posible escaneado). "
                "OCR no está soportado aún.",
                code="no_text",
            )

        raw_md = pymupdf4llm.to_markdown(doc)
        markdown = _normalize_markdown(raw_md or "")
        if not markdown:
            raise PdfImportError(
                "No se pudo obtener Markdown del PDF.",
                code="no_text",
            )

        return PdfImportResult(
            markdown=markdown,
            filename=_suggested_md_name(source_name),
            pages=doc.page_count,
            source=source,
            warnings=[LOSSY_WARNING],
        )
    finally:
        doc.close()
