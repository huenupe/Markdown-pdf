"""Rutas /api — preview, conversión a PDF e import PDF → Markdown."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
from pydantic import BaseModel, Field

from server.config import (
    ALLOWED_EXTENSIONS,
    ALLOWED_PDF_EXTENSIONS,
    DEFAULT_THEME,
    MAX_PDF_IMPORT_BYTES,
    MAX_UPLOAD_BYTES,
    SAVE_TO_OUTPUT,
    THEMES,
    normalize_theme,
)
from server.services.markdown_service import render_markdown
from server.services.pdf_import_service import PdfImportError, pdf_bytes_to_markdown
from server.services.pdf_service import highlight_css, pdf_service

router = APIRouter(prefix="/api")


class PreviewRequest(BaseModel):
    markdown: str = Field(..., min_length=0)
    theme: str | None = None


class ConvertRequest(BaseModel):
    markdown: str = Field(..., min_length=1)
    filename: str | None = None
    theme: str | None = None


def _ensure_size(text: str) -> None:
    if len(text.encode("utf-8")) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="El contenido supera el límite de 2 MB.")


def _pdf_filename(name: str | None) -> str:
    if not name or not name.strip():
        return "documento.pdf"
    base = Path(name.strip()).stem or "documento"
    return f"{base}.pdf"


async def _make_pdf(markdown: str, filename: str | None, theme: str | None) -> Response:
    text = markdown.strip()
    if not text:
        raise HTTPException(status_code=400, detail="El Markdown está vacío.")
    _ensure_size(markdown)
    theme_id = normalize_theme(theme)

    try:
        result = render_markdown(markdown)
        if not result.html.strip():
            raise HTTPException(status_code=400, detail="El Markdown no produjo contenido HTML.")
        pdf_bytes = await pdf_service.html_to_pdf(result.html, theme=theme_id)
    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"Error al generar PDF: {exc}") from exc

    out_name = _pdf_filename(filename)
    headers = {"Content-Disposition": f'attachment; filename="{out_name}"'}
    if SAVE_TO_OUTPUT:
        saved = pdf_service.save_to_output(pdf_bytes, out_name)
        headers["X-Saved-Path"] = str(saved.as_posix())

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers=headers,
    )


@router.get("/health")
async def health() -> dict:
    status = "ready" if pdf_service.ready else "error"
    payload: dict = {
        "ok": True,
        "service": "md-pdf",
        "phase": 6,
        "playwright": status,
    }
    if status != "ready":
        payload["message"] = (
            pdf_service.last_error
            or "Chromium no disponible. Con el .venv activo: playwright install chromium"
        )
    return payload


@router.get("/themes")
async def list_themes() -> dict:
    return {
        "themes": [{"id": k, "label": v} for k, v in THEMES.items()],
        "default": DEFAULT_THEME,
    }


@router.get("/highlight.css")
async def highlight_stylesheet() -> Response:
    return Response(content=highlight_css(), media_type="text/css")


@router.post("/preview")
async def preview(body: PreviewRequest) -> dict:
    if not isinstance(body.markdown, str):
        raise HTTPException(status_code=400, detail="El campo 'markdown' debe ser texto.")
    _ensure_size(body.markdown)
    theme_id = normalize_theme(body.theme)
    try:
        result = render_markdown(body.markdown)
    except Exception as exc:  # noqa: BLE001 — respuesta API controlada
        raise HTTPException(status_code=500, detail=f"Error al parsear Markdown: {exc}") from exc
    return {"html": result.html, "meta": result.meta, "theme": theme_id}


@router.post("/convert")
async def convert(body: ConvertRequest) -> Response:
    return await _make_pdf(body.markdown, body.filename, body.theme)


@router.post("/convert-file")
async def convert_file(
    file: UploadFile = File(...),
    theme: str = Form(DEFAULT_THEME),
) -> Response:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Falta el archivo.")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Extensión no permitida. Usá: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    raw = await file.read()
    if len(raw) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="El archivo supera el límite de 2 MB.")
    if not raw:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="El archivo debe estar en UTF-8.") from exc

    return await _make_pdf(text, file.filename, theme)


@router.post("/import-pdf")
async def import_pdf(file: UploadFile = File(...)) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Falta el archivo.")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_PDF_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Solo se aceptan archivos .pdf",
        )

    raw = await file.read()
    if len(raw) > MAX_PDF_IMPORT_BYTES:
        raise HTTPException(
            status_code=413,
            detail="El PDF supera el límite de 15 MB.",
        )
    if not raw:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")

    try:
        result = pdf_bytes_to_markdown(raw, file.filename)
    except PdfImportError as exc:
        status = 422 if exc.code == "no_text" else 400
        if exc.code not in {"no_text", "empty", "invalid"}:
            status = 500
        raise HTTPException(status_code=status, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail=f"Error al importar PDF: {exc}",
        ) from exc

    return {
        "markdown": result.markdown,
        "filename": result.filename,
        "meta": {"pages": result.pages, "source": result.source},
        "warnings": result.warnings,
    }
