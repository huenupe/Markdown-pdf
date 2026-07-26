# 10 — Extras P1 (Fase 5)

Extras de alto valor local elegidos del [08-ROADMAP](./08-ROADMAP.md).

## Alcance de esta fase

| # | Extra | Resumen |
|---|-------|---------|
| 1 | Highlight de código | Pygments + extensión `codehilite` |
| 2 | Frontmatter YAML | `title`, `author`, `date` → cabecera del documento |
| 3 | Copia en `output/` | Cada PDF generado se guarda también en disco |
| 4 | Plantillas CSS | `informe` (default), `notas`, `tecnico` |

## Dependencias (`.venv`)

```text
Pygments
python-frontmatter
```

Instalar: `pip install -r requirements.txt` (con venv activo).

## 1. Highlight

- Extensión Markdown: `codehilite` (+ `fenced_code`)
- Estilos: CSS generado por Pygments (`HtmlFormatter`, clase `.highlight`), inyectado en la plantilla del documento junto al tema
- Aplica a preview y PDF

## 2. Frontmatter

Ejemplo al inicio del `.md`:

```yaml
---
title: Informe mensual
author: Nombre
date: 2026-07-24
---
```

- Se parsea con `python-frontmatter`
- El cuerpo (sin YAML) se convierte a HTML
- Si hay meta, se antepone:

```html
<header class="doc-meta">
  <h1 class="doc-title">…</h1>
  <p class="doc-byline">autor · fecha</p>
</header>
```

- Si hay `title` en frontmatter, no hace falta repetir `# Título` (opcional del usuario)
- Preview API puede devolver `meta` además de `html`

## 3. Guardar en `output/` (opt-in)

- Por defecto **no** se escribe en disco (solo descarga en el navegador)
- Con `SAVE_TO_OUTPUT=1`: tras generar, escribir `output/<nombre>.pdf`
- La carpeta está en `.gitignore`; no subir PDF con datos personales

## 4. Plantillas

Archivos en `shared/themes/`:

| id | Archivo | Uso |
|----|---------|-----|
| `informe` | `informe.css` | Documento formal (default; evoluciona el tema Fase 4) |
| `notas` | `notas.css` | Más aire, tono informal |
| `tecnico` | `tecnico.css` | Densidad tipográfica, énfasis en código |

API:

- Body opcional `theme`: `"informe" | "notas" | "tecnico"` (default `informe`)
- `GET /api/themes` → lista de temas
- CSS estático: `/theme/themes/<id>.css`

`shared/pdf-theme.css` se mantiene como alias/copia de `informe` para compatibilidad del preview antiguo.

## API — cambios

### `POST /api/preview`

```json
{ "markdown": "...", "theme": "informe" }
```

```json
{
  "html": "...",
  "meta": { "title": "...", "author": "...", "date": "..." },
  "theme": "informe"
}
```

### `POST /api/convert` / `convert-file`

Mismos campos + `theme` (convert-file: form field `theme` opcional).

### `GET /api/themes`

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

## Frontend

- Selector de plantilla en la toolbar
- Enviar `theme` en preview/convert
- Cargar CSS del tema elegido para el iframe
- Atajos existentes se mantienen (`Ctrl+Enter`, `Ctrl+O`)

## Criterio de hecho

- [x] Bloque ` ```python ` se ve resaltado en preview y PDF
- [x] Frontmatter genera cabecera con título/autor/fecha
- [x] Guardado en `output/` solo si `SAVE_TO_OUTPUT=1`
- [x] Cambiar plantilla cambia tipografía/colores del preview y del PDF
- [x] Docs y checklist actualizados

## Fuera de alcance (esta fase)

- P2/P3 del roadmap (TOC, math, CLI, etc.) salvo atajos ya hechos en Fase 3
