# 00 — Visión

## Problema

Convertir notas o documentos en Markdown a un PDF legible suele implicar herramientas sueltas, calidad inconsistente o servicios online. Se necesita un flujo simple en la propia máquina.

## Solución

Una app web local con:

1. **Entrada:** subir un `.md`, pegar Markdown, o **importar un PDF** (texto → Markdown editable)
2. **Preview:** ver el HTML renderizado antes de exportar
3. **Salida:** generar y descargar un PDF con estilo de documento

La conversión a PDF ocurre en un **backend local** (Python + Playwright). La importación PDF → Markdown usa extracción local (PyMuPDF) y es **con pérdida**. Las librerías viven en un **`.venv`**.

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

## Objetivos de la v1

- Flujo completo: archivo/texto → preview → PDF
- PDF A4 legible (títulos, listas, código, tablas básicas)
- Documentación que guíe cada implementación
- Arranque: crear `.venv` → `pip install` → `uvicorn`

## Objetivo post-v1 (Development)

- Importar PDF con texto → Markdown editable → (opcional) re-exportar PDF
- Dejar claro en UI/docs que el round-trip no es idéntico

## Fuera de alcance (v1)

- Despliegue en Vercel/Railway/etc.
- Multiusuario o cola de trabajos
- Editor tipo Notion / WYSIWYG
- App de escritorio empaquetada (Electron)
- Sincronización con carpetas del sistema en tiempo real (watch mode)

## Éxito

Se considera exitoso si, en una máquina con Python instalado, siguiendo [03-SETUP](./03-SETUP.md), se genera un PDF correcto a partir de un `.md` de prueba en menos de 10 minutos.
