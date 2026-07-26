# 08 — Roadmap

## Fases

| Fase | Nombre | Entregable | Depende de |
|------|--------|------------|------------|
| 0 | Documentación | `README` + `docs/*` | — |
| 1 | Scaffold | `client/`, `server/`, `.venv`, `requirements.txt` | Docs 01–03 |
| 2 | Backend PDF | Endpoints health/preview/convert | Docs 04, 06, 07 |
| 3 | Frontend flujo | Upload → preview → descarga | Docs 05, 04 |
| 4 | Calidad | CSS PDF, fixtures, numeración | Docs 07, 06 |
| 5 | Extras | Ítems backlog priorizados | Roadmap |
| 6 | Cierre | README verificado, checklist OK | 03, 09 |

## MVP (debe quedar listo al cerrar Fase 4)

- [x] App local con deps en `.venv`
- [x] Subir `.md` y pegar texto
- [x] Preview HTML
- [x] Descargar PDF A4 vía Playwright
- [x] CSS documento básico
- [x] Páginas numeradas
- [x] Docs alineadas con el código

## Backlog (post-MVP)

### P1 — Alto valor local

1. [x] Highlight de código en PDF/preview
2. [x] Frontmatter YAML (`title`, `author`, `date`)
3. [x] Guardar copia en `output/` (opt-in `SAVE_TO_OUTPUT`)
4. [x] 2–3 plantillas CSS (Informe / Notas / Técnico)

Detalle: [10-EXTRAS-P1](./10-EXTRAS-P1.md)

### P2 — Productividad

5. [x] Atajos de teclado (`Ctrl+Enter`, etc.) — hecho en Fase 3
6. [x] Contador de palabras / caracteres / líneas (UI)
7. [x] **Importar PDF → Markdown** (local, con pérdida) — ver [12-PDF-TO-MD](./12-PDF-TO-MD.md)
8. [x] **Generar Markdown** (descarga `.md`; solo visible tras Abrir PDF)
9. Exportar también a HTML
10. Tabla de contenidos automática

### P3 — Más adelante

10. Historial reciente (localStorage)
11. Soporte de imágenes relativas con carpeta base
12. Math / Mermaid
13. OCR para PDFs escaneados
14. Script CLI `python -m server.cli` (md↔pdf)

## Ideas descartadas o aplazadas

| Idea | Motivo |
|------|--------|
| Auth / multiusuario | Fuera de visión local |
| Deploy cloud | Fuera de alcance v1 |
| Editor WYSIWYG | Complejidad alta; textarea basta |
| Node / npm en v1 | Un solo entorno: Python + `.venv` |

## Cómo agregar una idea nueva

1. Escribirla aquí en el backlog con prioridad
2. Si se va a implementar, crear o ampliar el doc técnico
3. Agregar ítems en [09-CHECKLIST](./09-CHECKLIST.md)
4. Recién entonces código

## Estado actual

- **Fases 0–6:** completadas
- **Producto local:** usable vía README (`python run.py` → `:8765`)
- **MD ↔ PDF:** CTAs **Abrir Markdown / Abrir PDF / Generar Markdown / Generar PDF**, modos de layout, Editar/Ver ([05-FRONTEND](./05-FRONTEND.md), [12-PDF-TO-MD](./12-PDF-TO-MD.md))
- **Backlog abierto:** resto P2/P3 (export HTML, TOC, OCR, CLI, etc.)
