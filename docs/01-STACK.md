# 01 — Stack

## Resumen

| Capa | Tecnología | Rol |
|------|------------|-----|
| Runtime | Python 3.12+ | Servidor y herramientas |
| Aislamiento | `.venv` en la raíz del repo | Todas las librerías Python (nunca globales) |
| Backend | FastAPI + Uvicorn | API HTTP local + servir UI estática |
| Frontend | HTML / CSS / JS (vanilla) en `client/` | Upload, editor, preview, descarga |
| Markdown → HTML | `markdown` (extensiones) | Parseo de Markdown |
| HTML → PDF | Playwright sync (Chromium) | `page.pdf()` en hilo; estable en Windows |
| PDF → Markdown | PyMuPDF + pymupdf4llm | Extracción local (con pérdida); ver [12-PDF-TO-MD](./12-PDF-TO-MD.md) |
| Upload | FastAPI `UploadFile` | Recepción de `.md` y `.pdf` |
| Estilos PDF | CSS propio (`shared/pdf-theme.css`) | Tipografía e impresión |

## Por qué esta elección

- **`.venv`:** dependencias aisladas del sistema; fácil de borrar y recrear.
- **Backend + Playwright:** calidad de PDF consistente (Chromium), equivalente a Puppeteer.
- **Frontend estático:** sin Node/npm; un solo entorno Python.
- **FastAPI:** API clara, docs automáticas en `/docs`, ideal para local.
- **Sin DB / sin Docker en v1:** menos fricción para uso personal.

## Dependencias (`requirements.txt`)

Todas se instalan **solo** dentro de `.venv`:

| Paquete | Uso |
|---------|-----|
| `fastapi` | API |
| `uvicorn[standard]` | Servidor ASGI |
| `python-multipart` | Upload de archivos |
| `markdown` | Markdown → HTML |
| `playwright` | HTML → PDF (Chromium) |
| `jinja2` | Plantilla HTML del documento (opcional pero útil) |

### Extras P1 (Fase 5; ver [10-EXTRAS-P1](./10-EXTRAS-P1.md))

- `python-frontmatter` — YAML frontmatter
- `Pygments` — resaltado de código

### Import PDF (P2; ver [12-PDF-TO-MD](./12-PDF-TO-MD.md))

- `pymupdf` — abrir PDF
- `pymupdf4llm` — PDF → Markdown

## Instalación de deps (siempre con venv activo)

```bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

`playwright install chromium` descarga el navegador (~150–300 MB la primera vez). Queda gestionado por Playwright, no como paquete pip suelto en el sistema.

## Versiones

- Python: 3.12+ (probado en el entorno del proyecto)
- Tras scaffold Fase 1 (ejemplo): FastAPI `0.140.0`, Playwright `1.61.0`, Markdown `3.10.2`
- Rangos en `requirements.txt`; el lock exacto vive dentro de `.venv`

## Lo que no usamos (v1)

| Tecnología | Motivo |
|------------|--------|
| Node.js / npm / Vite / React | Evitar segundo gestor; UI vanilla basta |
| Instalar con `pip` global | Obligatorio usar `.venv` |
| Docker | Innecesario para uso personal local |
| WeasyPrint / Pandoc | Playwright cubre el caso con CSS familiar |
| Base de datos | No hay persistencia de usuarios |
| Auth / JWT | App local de un solo usuario |

## Relación con otras fases

- Scaffold e instalación: [03-SETUP](./03-SETUP.md)
- Carpetas: [02-ARQUITECTURA](./02-ARQUITECTURA.md)
- Detalle PDF: [07-PDF](./07-PDF.md)
