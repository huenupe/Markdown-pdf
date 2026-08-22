# 04 — API

Base URL local: `http://127.0.0.1:8765` (default de `python run.py`)

Todas las rutas bajo `/api`. Content-Type JSON salvo uploads multipart y respuestas PDF.

## Endpoints

### `GET /api/health`

Comprueba que el servidor esté vivo (y, si es viable, el estado de Playwright).

**Response 200**

```json
{
  "ok": true,
  "service": "md-pdf",
  "playwright": "ready"
}
```

`playwright` puede ser `"ready"` | `"error"` (con `message` opcional si falla Chromium).

---

### `GET /api/themes`

Lista plantillas CSS disponibles.

```json
{
  "themes": [
    { "id": "informe", "label": "Informe" },
    { "id": "notas", "label": "Notas" },
    { "id": "tecnico", "label": "Técnico" }
  ],
  "default": "informe"
}
```

### `GET /api/highlight.css`

Hoja de estilos Pygments para bloques resaltados (preview).

---

### `POST /api/preview`

Convierte Markdown a HTML para el panel de vista previa (incluye frontmatter y highlight).

**Request**

```json
{
  "markdown": "---\ntitle: Demo\n---\n\n# Título\n\nHola mundo",
  "theme": "informe"
}
```

**Response 200**

```json
{
  "html": "<header class=\"doc-meta\">...</header>...",
  "meta": { "title": "Demo" },
  "theme": "informe"
}
```

**Errores**

| Código | Cuando |
|--------|--------|
| 400 | Falta `markdown` o no es string |
| 413 | Cuerpo demasiado grande |
| 500 | Error de parseo inesperado |

---

### `POST /api/convert`

Genera un PDF a partir de Markdown en el body.

**Request**

```json
{
  "markdown": "# Título\n\nContenido",
  "filename": "notas.md",
  "theme": "informe"
}
```

- `markdown` (requerido): string
- `filename` (opcional): nombre sugerido; se usa para el `Content-Disposition` (`.pdf`). Puede incluir Unicode/emojis: el header usa `filename` ASCII de respaldo y `filename*` UTF-8 (RFC 6266).
- `theme` (opcional): `informe` | `notas` | `tecnico`

**Response 200**

- `Content-Type: application/pdf`
- `Content-Disposition: attachment; filename="notas.pdf"` (si hay emojis: también `filename*=UTF-8''…`)
- Body: binario PDF
- `X-Saved-Path` (solo si `SAVE_TO_OUTPUT=1`): ruta en `output/`

**Errores**

| Código | Cuando |
|--------|--------|
| 400 | Markdown inválido / vacío |
| 500 | Fallo de Playwright o generación |

---

### `POST /api/convert-file`

Igual que convert, pero el origen es un archivo subido.

**Request:** `multipart/form-data`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `file` | File | Archivo `.md` / texto |
| `theme` | string | Opcional; plantilla CSS |

**Response 200:** PDF binario (nombre derivado del archivo original).

**Errores:** 400 si no hay archivo o extensión no permitida; 413 si excede tamaño; 500 si falla la generación.

---

### `POST /api/import-pdf`

Convierte un PDF (texto seleccionable) a Markdown. Ver [12-PDF-TO-MD](./12-PDF-TO-MD.md).

**Request:** `multipart/form-data`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `file` | File | Archivo `.pdf` (máx. 15 MB) |

**Response 200**

```json
{
  "markdown": "# Título\n\nContenido…",
  "filename": "documento.md",
  "meta": { "pages": 2, "source": "documento.pdf" },
  "warnings": [
    "Conversión con pérdida: revisá títulos, tablas e imágenes."
  ]
}
```

**Errores**

| Código | Cuando |
|--------|--------|
| 400 | Falta archivo, no es `.pdf`, o vacío |
| 413 | Supera 15 MB |
| 422 | Sin texto extraíble (posible escaneado; OCR no soportado) |
| 500 | Fallo del extractor |

---

## Pipeline compartido (servicios)

```
markdown (string)
  → services/markdown_service.py  → html_fragment
  → templates/document.html + shared/pdf-theme.css → full_html
  → services/pdf_service.py (Playwright) → bytes PDF
```

Import (sentido inverso, aparte):

```
PDF bytes → services/pdf_import_service.py → markdown (string)
```

Preview usa solo hasta `html_fragment` (el frontend puede envolver con el mismo CSS para fidelidad visual).

## Límites

| Límite | Valor |
|--------|-------|
| Tamaño máximo Markdown (body/upload `.md`) | 2 MB |
| Tamaño máximo PDF import | 15 MB |
| Extensiones Markdown | `.md`, `.markdown`, `.txt` |
| Extensión import | `.pdf` |
| Timeout generación PDF | p. ej. 30 s |

## Dependencias que toca

- FastAPI (rutas)
- `python-multipart` (convert-file, import-pdf)
- `markdown` (preview + convert)
- Playwright (convert / convert-file)
- `pymupdf` + `pymupdf4llm` (import-pdf)

## Criterio de hecho

- Health responde
- Preview devuelve HTML válido para un MD de prueba
- Convert / convert-file devuelven un PDF abrible
- Import-pdf devuelve Markdown usable para un PDF con texto
- Errores 400/422/500 con mensaje JSON claro

## Fuera de alcance (v1 / esta API)

- Autenticación
- Cola de trabajos / webhooks
- Versionado de API (`/v1`)
- Almacenamiento permanente indexado
- OCR de PDFs escaneados
