# 09 — Checklist

Usar este archivo para marcar progreso. Antes de cada bloque: leer los docs indicados.

## Fase 0 — Documentación

Docs a leer: ninguno (crearlos).

- [x] `README.md`
- [x] `docs/00-VISION.md`
- [x] `docs/01-STACK.md`
- [x] `docs/02-ARQUITECTURA.md`
- [x] `docs/03-SETUP.md`
- [x] `docs/04-API.md`
- [x] `docs/05-FRONTEND.md`
- [x] `docs/06-MARKDOWN.md`
- [x] `docs/07-PDF.md`
- [x] `docs/08-ROADMAP.md`
- [x] `docs/09-CHECKLIST.md`

**Salida:** plan y contratos claros sin código de app.

---

## Fase 1 — Scaffold

Docs: [01-STACK](./01-STACK.md), [02-ARQUITECTURA](./02-ARQUITECTURA.md), [03-SETUP](./03-SETUP.md)

- [x] Estructura `client/` + `server/` + `shared/`
- [x] `requirements.txt` + `.venv` creado
- [x] Dependencias instaladas **solo** en `.venv`
- [x] `.gitignore` (incluye `.venv/`, `output/`, etc.)
- [x] `GET /api/health` responde (histórico Fase 1: `:8000`; **hoy default `:8765`** vía `run.py`)
- [x] UI estática en la raíz (histórico `:8000`; **hoy** `http://127.0.0.1:8765`)
- [x] Script de arranque `scripts/dev.ps1` / `scripts/dev.sh`
- [x] Actualizar [03-SETUP](./03-SETUP.md) si los comandos reales difieren

**Salida:** venv + server + client placeholder corren en local.

---

## Fase 2 — Backend

Docs: [04-API](./04-API.md), [06-MARKDOWN](./06-MARKDOWN.md), [07-PDF](./07-PDF.md)

- [x] `POST /api/preview`
- [x] `POST /api/convert`
- [x] `POST /api/convert-file`
- [x] `markdown_service.py` + `pdf_service.py`
- [x] Plantilla HTML + `shared/pdf-theme.css` (mínimo)
- [x] `playwright install chromium` documentado/verificado
- [x] Prueba manual: PDF abrible

**Salida:** API genera preview HTML y PDF sin UI completa.

---

## Fase 3 — Frontend

Docs: [05-FRONTEND](./05-FRONTEND.md), [04-API](./04-API.md)

- [x] Dropzone / input `.md`
- [x] Textarea sincronizado
- [x] Preview con debounce → `/api/preview`
- [x] Botón Generar PDF → `/api/convert` → descarga
- [x] Estados loading / error
- [x] Atajos `Ctrl+Enter` (PDF) y `Ctrl+O` (abrir)
- [x] Tema del documento en preview (`/theme/pdf-theme.css`)

**Salida:** flujo completo en el navegador.

---

## Fase 4 — Calidad PDF

Docs: [07-PDF](./07-PDF.md), [06-MARKDOWN](./06-MARKDOWN.md)

- [x] CSS tipografía, código, tablas, imágenes
- [x] Márgenes A4 + `print_background`
- [x] Numeración de páginas
- [x] Fixtures `simple`, `code-and-tables`, `with-images`
- [x] Preview visualmente cercano al PDF (hoja A4; hoy **Shadow DOM**, no iframe `srcdoc`)
- [x] Script `scripts/render_fixtures.ps1`

**Salida:** fixtures OK.

---

## Fase 5 — Extras P1

Docs: [10-EXTRAS-P1](./10-EXTRAS-P1.md), [08-ROADMAP](./08-ROADMAP.md)

- [x] Highlight (Pygments + codehilite)
- [x] Frontmatter YAML
- [x] Copia en `output/` opt-in (`SAVE_TO_OUTPUT`)
- [x] Plantillas informe / notas / tecnico
- [x] UI selector de plantilla
- [x] `GET /api/themes` + `GET /api/highlight.css`

---

## Fase 6 — Cierre

Docs: [03-SETUP](./03-SETUP.md), este checklist, [README](../README.md)

- [x] README con instrucciones reales verificadas
- [x] Smoke test: health, UI, preview, convert, frontmatter (`scripts/smoke_test.py`)
- [x] Roadmap actualizado (MVP + fases 0–6)
- [x] Setup alineado con el estado final

**Salida:** proyecto usable siguiendo solo el README.

---

## Privacidad UI (post v1)

Docs: [11-PRIVACIDAD](./11-PRIVACIDAD.md), [05-FRONTEND](./05-FRONTEND.md)

- [x] Sin Google Fonts / CDN de tipografía
- [x] Aviso de URLs remotas en la UI
- [x] Preview con Shadow DOM (sin iframe `srcdoc`)
- [x] Docs de privacidad y Markdown actualizados

---

## P2 — Import PDF → Markdown (rama Development)

Docs: [12-PDF-TO-MD](./12-PDF-TO-MD.md), [04-API](./04-API.md), [05-FRONTEND](./05-FRONTEND.md)

- [x] `pymupdf` + `pymupdf4llm` en `requirements.txt` / `.venv`
- [x] `server/services/pdf_import_service.py`
- [x] `POST /api/import-pdf`
- [x] UI: Abrir PDF + aviso de pérdida + drop `.pdf`
- [x] Límite 15 MB PDF (separado del 2 MB Markdown)
- [x] Error 422 claro si no hay texto extraíble
- [x] Smoke: convert → import-pdf → markdown no vacío
- [x] Docs (00–12, README) alineados con CTAs y flujos actuales

---

## UX layout (Development)

Docs: [05-FRONTEND](./05-FRONTEND.md)

- [x] Paneles más bajos con scroll interno independiente
- [x] Toggle Editar / Ver (editor con contraste alto)
- [x] Modo MD: Markdown | Vista PDF (hoja HTML)
- [x] Modo PDF: PDF original | Markdown
- [x] Sin favicon en disco (`data:,` + `204` en `/favicon.ico`)
- [x] Sin overlay visual de drop (drop silencioso; Abrir Markdown / Abrir PDF)
- [x] **Generar Markdown** solo en modo PDF; **Generar PDF** solo en modo Markdown
- [x] Etiquetas: Abrir Markdown · Abrir PDF · Generar Markdown · Generar PDF

---

## Smoke test

Con el servidor en `http://127.0.0.1:8765`:

```powershell
.\.venv\Scripts\python.exe scripts\smoke_test.py
```

Resultado (2026-07-26): **OK** — health, assets, preview, convert, frontmatter, **import-pdf**.
