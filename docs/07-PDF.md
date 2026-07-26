# 07 — PDF

## Objetivo

Generar un PDF **A4** legible y predecible a partir del HTML producido por `markdown`, usando **Playwright** (Chromium).

## Pipeline

1. Recibir Markdown
2. Convertir a fragmento HTML ([06-MARKDOWN](./06-MARKDOWN.md))
3. Envolver en plantilla HTML completa:
   - `<!DOCTYPE html>`, charset UTF-8
   - Inyectar o linkear `shared/pdf-theme.css`
   - `<main class="document">…fragmento…</main>`
4. Playwright **sync** (en un hilo vía `asyncio.to_thread`, compatible con Windows):
   - lanzar browser (reutilizar instancia con lock)
   - `page.set_content(full_html, wait_until="networkidle")`
   - `page.pdf(**opciones)`
5. Devolver `bytes` al cliente (descarga en el navegador). Copia en `output/` **solo** si `SAVE_TO_OUTPUT=1`

## Opciones Playwright previstas

```python
{
    "format": "A4",
    "print_background": True,
    "margin": {
        "top": "20mm",
        "right": "18mm",
        "bottom": "20mm",
        "left": "18mm",
    },
    "display_header_footer": True,
    "header_template": "<div></div>",
    "footer_template": """
      <div style="font-size:9px;width:100%;text-align:center;color:#666;">
        <span class="pageNumber"></span> / <span class="totalPages"></span>
      </div>
    """,
}
```

Ajustar márgenes si header/footer comen espacio.

## CSS del documento (`shared/pdf-theme.css`)

Debe cubrir al menos:

- Tipografía de cuerpo legible
- Jerarquía `h1`–`h3`
- `pre` / `code` con fondo suave
- Tablas con bordes simples
- Imágenes `max-width: 100%`
- `page-break-inside: avoid` en `pre`, `table`, `blockquote` cuando ayude

El preview del frontend debería cargar el mismo CSS para acercar WYSIWYG.

## Archivos que toca

| Archivo | Rol |
|---------|-----|
| `server/services/pdf_service.py` | Playwright, `pdf()`, ciclo de vida |
| `server/services/markdown_service.py` | HTML fragment |
| `server/templates/document.html` | Envoltorio |
| `shared/pdf-theme.css` | Estilos de impresión |
| `output/` | Copias opcionales solo con `SAVE_TO_OUTPUT=1` |

## Rendimiento local

- Reutilizar un browser Playwright entre requests (singleton) en dev
- Cerrar browser en shutdown de la app
- Timeout por conversión (p. ej. 30 s)

## Errores típicos a manejar

| Error | Respuesta |
|-------|-----------|
| Chromium no instalado | 500 + mensaje (`playwright install chromium`) |
| HTML vacío | 400 |
| Timeout | 500 |

## Criterio de hecho

- PDF A4 abre en lectores comunes
- Texto seleccionable (no solo imagen)
- Numeración de páginas visible
- Fixtures de [06-MARKDOWN](./06-MARKDOWN.md) se ven correctos

## Verificar fixtures (Fase 4)

Con el servidor corriendo:

```powershell
.\scripts\render_fixtures.ps1
```

Salida en `output/simple.pdf`, `output/code-and-tables.pdf`, `output/with-images.pdf`.

## Sentido inverso (PDF → Markdown)

Este documento cubre solo **MD → PDF**. Para importar un PDF al editor, ver [12-PDF-TO-MD](./12-PDF-TO-MD.md).

## Fuera de alcance (v1)

- PDF/A archival
- Firmas digitales
- Marca de agua compleja
- Múltiples temas de marca (solo 1 tema; más en roadmap)
- OCR / recuperación perfecta del Markdown original
