# 01 — Stack

## Resumen

| Capa | Tecnología | Rol |
|------|------------|-----|
| Runtime | Python 3.12+ | Servidor y herramientas |
| Aislamiento | `.venv` en la raíz del repo | Todas las librerías Python (nunca globales) |
| Backend | FastAPI + Uvicorn | API HTTP local + servir UI estática |
| Frontend | HTML / CSS / JS (vanilla) en `client/` | Abrir MD/PDF, Editar/Ver, preview, CTAs |
| Markdown → HTML | `markdown` (extensiones) | Parseo de Markdown |
| HTML → PDF | Playwright sync (Chromium) | `page.pdf()` en hilo; estable en Windows |
| PDF → Markdown | PyMuPDF + pymupdf4llm | Extracción local (con pérdida); ver [12-PDF-TO-MD](./12-PDF-TO-MD.md) |
| Upload | FastAPI `UploadFile` | Recepción de `.md` y `.pdf` |
| Estilos PDF | CSS en `shared/themes/` | Tipografía e impresión |

## Por qué esta elección

- **`.venv`:** dependencias aisladas del sistema; fácil de borrar y recrear.
- **Backend + Playwright:** calidad de PDF consistente (Chromium).
- **Frontend estático:** sin Node/npm; un solo entorno Python.
- **FastAPI:** API clara, docs en `/docs`, ideal para local.
- **PyMuPDF:** import PDF local sin APIs cloud.
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
| `jinja2` | Plantilla HTML del documento |
| `Pygments` | Resaltado de código |
| `python-frontmatter` | YAML frontmatter |
| `pymupdf` | Abrir PDF |
| `pymupdf4llm` | PDF → Markdown |
| `tabulate` | Dependencia de pymupdf4llm |

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

`playwright install chromium` descarga el navegador (~150–300 MB la primera vez).

## Versiones

- Python: 3.12+
- Rangos en `requirements.txt`; el lock exacto vive dentro de `.venv`
- Arranque recomendado: `python run.py` → `http://127.0.0.1:8765`

## Lo que no usamos

| Tecnología | Motivo |
|------------|--------|
| Node.js / npm / Vite / React | Evitar segundo gestor; UI vanilla basta |
| Instalar con `pip` global | Obligatorio usar `.venv` |
| Docker | Innecesario para uso personal local |
| WeasyPrint / Pandoc | Playwright + PyMuPDF cubren MD↔PDF |
| Base de datos | No hay persistencia de usuarios |
| Auth / JWT | App local de un solo usuario |
| Favicon en disco / CDN | Ver [11-PRIVACIDAD](./11-PRIVACIDAD.md) |

## Relación con otros docs

- Scaffold e instalación: [03-SETUP](./03-SETUP.md)
- Carpetas: [02-ARQUITECTURA](./02-ARQUITECTURA.md)
- Extras P1 (histórico Fase 5): [10-EXTRAS-P1](./10-EXTRAS-P1.md)
- PDF de salida: [07-PDF](./07-PDF.md)
- Import PDF: [12-PDF-TO-MD](./12-PDF-TO-MD.md)
- UI: [05-FRONTEND](./05-FRONTEND.md)
