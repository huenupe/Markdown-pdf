# 00 — Visión

## Problema

Convertir notas o documentos entre Markdown y PDF suele implicar herramientas sueltas, calidad inconsistente o servicios online. Se necesita un flujo simple en la propia máquina.

## Solución

Una app web local con:

1. **Entrada:** **Abrir Markdown** (o pegar texto), o **Abrir PDF** (texto → Markdown editable)
2. **Preview:** HTML renderizado (modo MD) o PDF original + Markdown (modo PDF)
3. **Salida según origen:**
   - Tras Abrir Markdown → **Generar PDF**
   - Tras Abrir PDF → **Generar Markdown**

La conversión a PDF usa **backend local** (Python + Playwright). La importación PDF → Markdown usa extracción local (PyMuPDF) y es **con pérdida**. Las librerías viven en un **`.venv`**.

## Usuario

- Uso personal / local
- Una sola persona en la máquina
- Sin cuentas ni colaboración

## Restricciones

| Restricción | Detalle |
|-------------|---------|
| Solo local | Escucha en `127.0.0.1`; no está pensado para exponer a internet |
| Sin auth | No hay login ni roles |
| Sin base de datos | No se persiste usuarios ni historial en DB (opcional: archivos en `output/`) |
| Sin cloud | No sube contenido a terceros |
| Deps en `.venv` | No instalar paquetes Python en el entorno global |
| UI offline | Sin CDN de tipografía (fuentes del sistema); ver [11-PRIVACIDAD](./11-PRIVACIDAD.md) |
| v1 enfocada | MVP usable antes que features avanzadas |

## Objetivos (estado actual)

- Flujo MD → preview → **Generar PDF**
- Flujo PDF → Markdown editable → **Generar Markdown**
- CTAs mutuamente excluyentes según el origen del archivo
- PDF A4 legible (títulos, listas, código, tablas básicas)
- Round-trip no idéntico (documentado en UI y [12-PDF-TO-MD](./12-PDF-TO-MD.md))
- Arranque: `.venv` → `pip install` → `python run.py` (puerto **8765**)

## Fuera de alcance

- Despliegue en Vercel/Railway/etc.
- Multiusuario o cola de trabajos
- Editor tipo Notion / WYSIWYG
- App de escritorio empaquetada (Electron)
- OCR para PDFs escaneados
- Sincronización con carpetas del sistema en tiempo real (watch mode)

## Éxito

Se considera exitoso si, siguiendo [03-SETUP](./03-SETUP.md):

1. Se genera un PDF correcto a partir de un `.md` de prueba, y
2. Se importa un PDF con texto y se descarga un `.md` usable con **Generar Markdown**,

en unos minutos en una máquina con Python instalado.
