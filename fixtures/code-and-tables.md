# Código y tablas

Fixture para bloques de código y tablas GFM.

## Bloque de código

```python
def saludar(nombre: str) -> str:
    """Devuelve un saludo."""
    return f"Hola, {nombre}"

if __name__ == "__main__":
    print(saludar("MD-PDF"))
```

Código inline: `print("ok")`.

## Tabla

| Lenguaje | Uso en el proyecto | Notas        |
|----------|--------------------|--------------|
| Python   | Backend FastAPI    | `.venv`      |
| Markdown | Entrada            | fixtures     |
| CSS      | Tema del PDF       | `shared/`    |
| JS       | UI local           | `client/`    |

## Otra tabla corta

| A | B | C |
|---|---|---|
| 1 | 2 | 3 |
| 4 | 5 | 6 |

Los bloques `pre` y las tablas deben evitar cortes feos de página cuando quepan enteros.
