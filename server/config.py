"""Configuración local del servidor."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLIENT_DIR = ROOT / "client"
SHARED_DIR = ROOT / "shared"
THEMES_DIR = SHARED_DIR / "themes"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
OUTPUT_DIR = ROOT / "output"
PDF_THEME_CSS = SHARED_DIR / "pdf-theme.css"

MAX_UPLOAD_BYTES = 2 * 1024 * 1024  # 2 MB (Markdown)
MAX_PDF_IMPORT_BYTES = 15 * 1024 * 1024  # 15 MB (PDF → Markdown)
PDF_TIMEOUT_MS = 30_000
ALLOWED_EXTENSIONS = {".md", ".markdown", ".txt"}
ALLOWED_PDF_EXTENSIONS = {".pdf"}

# Por defecto NO guarda PDF en disco (solo descarga). Opt-in: SAVE_TO_OUTPUT=1
SAVE_TO_OUTPUT = os.getenv("SAVE_TO_OUTPUT", "").strip().lower() in {
    "1",
    "true",
    "yes",
    "on",
}

DEFAULT_THEME = "informe"
THEMES = {
    "informe": "Informe",
    "notas": "Notas",
    "tecnico": "Técnico",
}


def normalize_theme(theme: str | None) -> str:
    if theme and theme in THEMES:
        return theme
    return DEFAULT_THEME
