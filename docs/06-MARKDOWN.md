# 06 — Markdown

## Motor

- Librería: **`markdown`** (Python), instalada en `.venv`
- Frontmatter: **`python-frontmatter`** (`title`, `author`, `date`)
- Highlight: extensión `codehilite` + **Pygments**
- HTML de salida: fragmento; el envoltorio lo pone la plantilla del PDF

## Soporte v1

| Elemento | Ejemplo | Notas |
|----------|---------|-------|
| Encabezados | `#` … `######` | Estilos en CSS PDF |
| Párrafos | texto | |
| Énfasis | `*em*` `**strong**` | |
| Listas | `-` / `1.` | Anidadas básicas |
| Enlaces | `[texto](url)` | URL remota puede generar request al exportar |
| Imágenes | `![alt](url)` | Preferir **data URI**; `http(s)` descarga al PDF |
| Código inline / bloques | `` ` `` / ` ``` ` | Con highlight |
| Citas, HR, tablas | | Extensiones `tables`, etc. |
| Frontmatter YAML | `---` al inicio | Cabecera `.doc-meta` |

## Privacidad de recursos

Ver [11-PRIVACIDAD](./11-PRIVACIDAD.md).

- `![](https://…)` o enlaces `http(s)://` → Chromium puede salir a internet al generar el PDF
- La UI muestra un aviso si detecta `http://` / `https://` en el texto
- Recomendado: data URI (como `fixtures/with-images.md`)

## Sentido inverso (PDF → Markdown)

El Markdown también puede **producirse** al importar un PDF (extracción local, con pérdida). Ver [12-PDF-TO-MD](./12-PDF-TO-MD.md). Ese flujo no usa este motor `markdown` hasta que el usuario edita y vuelve a pedir preview/PDF.

## Limitaciones

| Tema | Comportamiento |
|------|----------------|
| HTML embebido en el MD | Evitado / sanitizado |
| Imágenes relativas (`./img.png`) | No soportadas aún (backlog P3) |
| Math / Mermaid | No en v1 |
| Round-trip MD→PDF→MD | No idéntico |

## Fixtures

| Archivo | Cubre |
|---------|--------|
| `simple.md` | Títulos, listas, enlace |
| `code-and-tables.md` | Código, tabla |
| `with-images.md` | Imagen data URI |
| `frontmatter-demo.md` | YAML + highlight |
