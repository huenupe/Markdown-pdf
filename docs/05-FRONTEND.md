# 05 — Frontend

## Objetivo UX

Interfaz con **aspecto de producto web (SaaS)** y ejecución **100% local**: Markdown ↔ PDF (preview HTML de documento + import PDF), sin cuentas ni cloud.

## Stack UI

- HTML / CSS / JS vanilla en `client/`
- Servido por FastAPI desde la raíz `/`
- Sin Node, npm, Vite ni React
- **Sin CDN externos** (tipografía `system-ui` / Segoe UI; ver [11-PRIVACIDAD](./11-PRIVACIDAD.md))
- **Sin favicon en disco:** `<link rel="icon" href="data:,">` para no pedir `/favicon.ico`; el backend responde `204` si algún cliente aún lo solicita

## Look visual

| Elemento | Dirección |
|----------|-----------|
| Fondo app | `#f8fafc` |
| Paneles | `#ffffff`, borde `#e2e8f0`, radio ~8px, sombra suave |
| Altura paneles | Fija (`~48vh` / máx. ~480px), scroll **interno** por cuadro |
| Texto editor | `#0f172a` (alto contraste en modo Editar) |
| CTA principal | `#2563eb` (**Generar PDF** o **Generar Markdown**, según modo) |
| Preview documento | Hoja A4 HTML con CSS de plantilla (Shadow DOM) |

## Composición

| Zona | Contenido |
|------|-----------|
| Cabecera | Marca **MD-PDF** + tagline |
| Toolbar | **Abrir Markdown** + **Abrir PDF** + Plantilla · Limpiar + CTA según modo |
| Avisos | URLs remotas; import PDF con pérdida |
| Workspace | Dos paneles (altura limitada + scroll propio) |
| Footer | Estado del backend |

## Botones de acción (mutuamente excluyentes)

| Origen | Modo | CTA visible |
|--------|------|-------------|
| **Abrir Markdown** / pegar / Limpiar | `md` | Solo **Generar PDF** |
| **Abrir PDF** | `pdf` | Solo **Generar Markdown** |

No se muestra **Generar Markdown** al abrir un `.md`, ni **Generar PDF** tras importar un PDF.

## Modos de layout

### Modo Markdown (`Abrir Markdown` / pegar / limpiar)

| Izquierda | Derecha |
|-----------|---------|
| Panel **Markdown** con toggle **Editar / Ver** | **Vista PDF** = hoja HTML actual (plantilla) |

### Modo PDF (`Abrir PDF`)

| Izquierda | Derecha |
|-----------|---------|
| Visor del **PDF original** (`iframe` + blob local) | Panel **Markdown** con **Editar / Ver** |

## Comportamientos

1. **Abrir Markdown** / soltar `.md` → modo MD → preview con debounce (~400 ms) → CTA **Generar PDF**
2. **Abrir PDF** / soltar `.pdf` → modo PDF + `POST /api/import-pdf` → CTA **Generar Markdown**
3. Drop **sin overlay** visual
4. Contador palabras / caracteres / líneas
5. Health en el footer

Detalle import: [12-PDF-TO-MD](./12-PDF-TO-MD.md).

## Atajos

| Atajo | Acción |
|-------|--------|
| `Ctrl+Enter` / `Cmd+Enter` | Generar PDF (solo en modo MD) |
| `Ctrl+O` / `Cmd+O` | Abrir Markdown |

## Preview

- `#preview-host` (derecha, modo MD) y `#md-view-host` (modo Ver) con **Shadow DOM**
- CSS de `/theme/themes/<id>.css` + `/api/highlight.css`

## Criterio de hecho

- Paneles compactos con scroll independiente
- Toggle Editar/Ver con editor contrastado
- CTA según modo (Generar PDF vs Generar Markdown)
- Sin overlay de drag-and-drop
- Sin petición ruidosa a favicon
- Sin CDN; aviso de URLs remotas

## Fuera de alcance

- Monaco / CodeMirror
- Fuentes web por CDN
- Embeber PDF generado por Playwright en el panel
- OCR / auth / multiusuario
