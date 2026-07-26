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
| CTA Generar PDF | `#2563eb` |
| Preview documento | Hoja A4 HTML con CSS de plantilla (Shadow DOM) |

## Composición

| Zona | Contenido |
|------|-----------|
| Cabecera | Marca **MD-PDF** + tagline |
| Toolbar | Abrir .md + Abrir PDF + Plantilla · Limpiar + **Descargar .md** + **Generar PDF** |
| Avisos | URLs remotas; import PDF con pérdida |
| Workspace | Dos paneles (altura limitada + scroll propio) |
| Footer | Estado del backend |

## Modos de layout

### Modo Markdown (`Abrir .md` / pegar / limpiar)

| Izquierda | Derecha |
|-----------|---------|
| Panel **Markdown** con toggle **Editar / Ver** | **Vista PDF** = hoja HTML actual (plantilla), no PDF binario embebido |

- **Editar:** textarea legible (contraste alto)
- **Ver:** mismo HTML de preview en el panel izquierdo

### Modo PDF (`Abrir PDF`)

| Izquierda | Derecha |
|-----------|---------|
| Visor del **PDF original** (`iframe` + blob local) | Panel **Markdown** con **Editar / Ver** |

El PDF se mantiene en memoria del navegador (`URL.createObjectURL`); no se sube a cloud.

## Comportamientos

1. Subir / soltar `.md` → modo Markdown → preview con debounce (~400 ms)
2. **Abrir PDF** / soltar `.pdf` → modo PDF + `POST /api/import-pdf` → Markdown a la derecha (automático)
3. **Descargar .md** → guarda el Markdown del editor (útil tras importar un PDF)
4. Drop de archivos **sin overlay** visual
5. Contador palabras / caracteres / líneas
6. Generar PDF → descarga (copia en `output/` solo si `SAVE_TO_OUTPUT=1`)
7. Health en el footer

Detalle import: [12-PDF-TO-MD](./12-PDF-TO-MD.md).

## Atajos

| Atajo | Acción |
|-------|--------|
| `Ctrl+Enter` / `Cmd+Enter` | Generar PDF |
| `Ctrl+O` / `Cmd+O` | Abrir archivo `.md` |

## Preview

- `#preview-host` (derecha, modo MD) y `#md-view-host` (modo Ver) con **Shadow DOM**
- CSS de `/theme/themes/<id>.css` + `/api/highlight.css`
- La “Vista PDF” del panel derecho es la **hoja HTML** (no un PDF Playwright embebido)

## Criterio de hecho

- Paneles compactos con scroll independiente
- Toggle Editar/Ver con editor contrastado
- Modo PDF: PDF izquierda / Markdown derecha
- Modo MD: Markdown izquierda / Vista PDF (HTML) derecha
- Sin overlay de drag-and-drop
- Sin petición ruidosa a favicon (data URI; 204 de respaldo)
- Sin CDN; aviso de URLs remotas

## Fuera de alcance

- Monaco / CodeMirror
- Fuentes web por CDN
- Embeber PDF generado por Playwright en el panel (la descarga sigue siendo el PDF real)
- OCR / auth / multiusuario
