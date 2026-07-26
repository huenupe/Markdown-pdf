# 11 — Privacidad (uso local / offline)

## Objetivo

Minimizar salida de datos a internet al usar MD-PDF. El diseño es **local**: Markdown y PDF no se envían a un servicio cloud de la app.

## Qué queda en tu máquina

- Servidor en `127.0.0.1` (no expuesto a la red por defecto)
- Conversión MD→PDF con Playwright/Chromium local
- Importación PDF→Markdown con PyMuPDF local (sin APIs cloud de documentos)
- Dependencias en `.venv` (sin telemetría de “subir el documento” en el código de la app)
- Por defecto **no** se guardan PDF en `output/` (solo descarga). Opt-in: `SAVE_TO_OUTPUT=1`

## Qué puede salir a internet

| Situación | ¿Filtra el texto del Markdown? | Notas |
|-----------|--------------------------------|-------|
| Imágenes/recursos `http(s)://` en el `.md` | Indirecto | Al generar el PDF, Chromium **descarga** esa URL |
| `pip install` / `playwright install` | No | Solo al instalar paquetes/navegador |
| Importar PDF | No | El binario se procesa en tu máquina |
| Extensiones del navegador | Depende de la extensión | Fuera del control de MD-PDF |

## Medidas aplicadas en la UI

- Aspecto de producto web (SaaS); **datos y cómputo siguen en local**
- **Sin Google Fonts** ni otros CDN de tipografía: fuentes del sistema
- **Sin favicon remoto** ni archivo favicon: icono vacío en data URI (no pide `/favicon.ico` a la red)
- **Aviso** si el Markdown contiene URLs remotas (`http://` / `https://`) en imágenes o enlaces que puedan disparar red al exportar
- **Aviso** tras importar PDF: conversión con pérdida (no es OCR cloud)
- Preview del documento en Shadow DOM local; el PDF importado se ve con blob `blob:` en el navegador (no se reenvía a terceros)
- Sin ejecutar scripts del HTML del documento

## Recomendaciones de uso

1. Preferir imágenes embebidas (data URI) o, cuando exista soporte, archivos locales
2. Evitar `![](https://…)` si el documento es sensible
3. No exponer el servidor a `0.0.0.0` ni a internet
4. Para depurar la consola del navegador, usar ventana sin extensiones (muchas alertas vienen de `contentscript.js` ajenos)
5. Solo abrir PDFs de confianza (parsers locales; app pensada para localhost)

## Docs relacionados

- [00-VISION](./00-VISION.md) — restricciones locales
- [05-FRONTEND](./05-FRONTEND.md) — UI
- [06-MARKDOWN](./06-MARKDOWN.md) — imágenes y límites
- [12-PDF-TO-MD](./12-PDF-TO-MD.md) — importación PDF
