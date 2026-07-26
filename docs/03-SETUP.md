# 03 — Setup

## Requisitos del sistema

- **Python** 3.12+ (recomendado)
- Sistema operativo: Windows / macOS / Linux
- Espacio en disco: ~300 MB+ para Chromium de Playwright
- Red en la primera instalación (pip + `playwright install chromium`)

Comprobar:

```bash
python --version
```

## Entorno virtual (obligatorio)

Todas las librerías van en `.venv` en la raíz del repo. **No** usar `pip install` global.

```bash
cd MD-PDF
python -m venv .venv
```

Activar:

```powershell
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
```

```bash
# macOS / Linux
source .venv/bin/activate
```

Con el venv activo, el prompt suele mostrar `(.venv)`.

## Instalación de dependencias

```bash
pip install -r requirements.txt
playwright install chromium
```

Incluye PyMuPDF / pymupdf4llm para **importar PDF → Markdown** (ver [12-PDF-TO-MD](./12-PDF-TO-MD.md)). Chromium queda en el cache de Playwright (en Windows: `%LOCALAPPDATA%\ms-playwright`).

## Arranque

Con el venv activo, usar el launcher (recomendado):

```bash
python run.py
```

```powershell
.\scripts\dev.ps1
```

```bash
./scripts/dev.sh
```

- UI + API: `http://127.0.0.1:8765`
- Docs FastAPI: `http://127.0.0.1:8765/docs`

`run.py` por defecto:

- host `127.0.0.1`
- puerto `8765` (menos conflictos que 8000 en Windows)
- **sin** `--reload` (más estable con Playwright en Windows)

Opciones:

```bash
python run.py --port 9000
python run.py --reload
```

### Evitar este comando en Windows (histórico)

```bash
uvicorn server.main:app --reload --host 127.0.0.1 --port 8000
```

En Windows suele combinar:

1. `WinError 10013` si el puerto está reservado/bloqueado
2. `NotImplementedError` en Playwright con el event loop de `--reload`

El PDF usa Playwright **sync** en un hilo (`asyncio.to_thread`), que es compatible con Windows.

## Verificación

1. `GET http://127.0.0.1:8765/api/health` → `"ok": true` y `"playwright": "ready"`
2. Abrir la UI → toolbar (**Abrir Markdown** / **Abrir PDF**) + paneles + plantilla
3. **Abrir Markdown** con `fixtures/simple.md` → preview OK → solo CTA **Generar PDF** → descarga `.pdf`
4. **Abrir PDF** (un PDF con texto) → layout PDF \| Markdown → solo CTA **Generar Markdown** → descarga `.md`
5. `output/`: por defecto **no** se escribe nada; solo si `SAVE_TO_OUTPUT=1`
6. Smoke automatizado (servidor arriba):

```powershell
.\.venv\Scripts\python.exe scripts\smoke_test.py
```

```powershell
.\scripts\render_fixtures.ps1
```

Nota: el ejemplo histórico con puerto `8000` más abajo es solo para documentar problemas en Windows; el default actual es **8765**.

## Variables de entorno (opcionales)

| Variable | Default | Uso |
|----------|---------|-----|
| `PORT` | `8765` | Puerto de `run.py` / smoke tests |
| `HOST` | `127.0.0.1` | Host de `run.py` |
| `MD_PDF_BASE` | `http://127.0.0.1:$PORT` | Base URL para scripts de prueba |
| `SAVE_TO_OUTPUT` | off | Si `1`/`true`, guarda copia del PDF en `output/` |

## Troubleshooting

| Síntoma | Qué revisar |
|---------|-------------|
| `python` no encontrado | Instalar Python 3.12+ y marcar “Add to PATH” |
| ExecutionPolicy en PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Playwright no encuentra Chromium | `playwright install chromium` con venv activo |
| `WinError 10013` | Puerto bloqueado/reservado → `python run.py --port 9000` o revisar `netsh interface ipv4 show excludedportrange protocol=tcp` |
| `NotImplementedError` / Playwright al arrancar | Usar `python run.py` (sin `--reload`). Ya no debería ocurrir con Playwright sync |
| Puerto en uso | `python run.py --port <otro>` |
| Módulos no encontrados | Confirmar `(.venv)` activo y `pip install -r requirements.txt` |
| Preview sin colores de código | `GET /api/highlight.css` debe responder 200 |

## .gitignore

```
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
output/*
!output/.gitkeep
.env
*.log
.DS_Store
```

## Criterio de salida

Siguiendo este archivo (o el README), se arranca la app y se genera un PDF a partir de un fixture en menos de 10 minutos.
