# Clase 3 - Exportar DataFrames de `pandas` a SQL (SQLite)

## 1. Explicación del ejemplo

En la hackathon necesitarás guardar los datos que obtienes de la API de la NASA para no tener que consultarlos una y otra vez (ahorra tiempo y evita alcanzar el límite de peticiones).

Esta clase enseña a mover datos entre **pandas** y **SQLite** usando SQLAlchemy como motor de conexión:

1. **Exportar a SQLite:** `df.to_sql()` guarda un DataFrame en una tabla de base de datos.
2. **Leer desde SQLite:** `pd.read_sql_table()` y `pd.read_sql()` convierten una tabla o consulta SQL en DataFrame.
3. **Anexar datos:** `if_exists="append"` agrega nuevos registros sin borrar los existentes.

---

## 2. Explicación de la clase / conceptos clave

### `create_engine` de SQLAlchemy

SQLAlchemy es la librería que conecta Python con bases de datos. Para SQLite solo necesitas la ruta del archivo:

```python
from sqlalchemy import create_engine
engine = create_engine("sqlite:///datos.db")
```

El triple slash `///` indica una ruta relativa al archivo local.

### `df.to_sql()`

| Parámetro | Valor | Significado |
|-----------|-------|-------------|
| `name` | `"tabla"` | Nombre de la tabla en la BD |
| `con` | `engine` | Conexión a la base de datos |
| `if_exists` | `"replace"` | Borra la tabla y la crea de nuevo |
| `if_exists` | `"append"` | Agrega filas a la tabla existente |
| `if_exists` | `"fail"` | Lanza error si la tabla ya existe (por defecto) |
| `index` | `False` | No escribe el índice de pandas como columna |

### Leer desde SQLite

```python
# Leer toda la tabla
df = pd.read_sql_table("asteroides", con=engine)

# Leer con consulta SQL personalizada
df = pd.read_sql("SELECT * FROM asteroides WHERE peligroso = 1", con=engine)
```

---

## 3. Diccionario de sintaxis global - pandas + SQL (SQLite)

```python
import pandas as pd
from sqlalchemy import create_engine

# Conexión a SQLite
engine = create_engine("sqlite:///datos.db")

# Exportar DataFrame a SQL
df.to_sql("nombre_tabla", con=engine, if_exists="replace", index=False)
df.to_sql("nombre_tabla", con=engine, if_exists="append", index=False)

# Leer tabla completa
df = pd.read_sql_table("nombre_tabla", con=engine)

# Leer con consulta SQL
df = pd.read_sql("SELECT * FROM tabla WHERE columna = valor", con=engine)

# Cerrar conexión (opcional, SQLite lo maneja solo)
engine.dispose()
```

---

## 4. Flujo de trabajo lógico

1. **Obtener datos:** `requests` → JSON → `pandas` DataFrame.
2. **Transformar:** `pd.json_normalize()`, filtros, agrupaciones.
3. **Persistir:** `df.to_sql()` guarda en SQLite para reutilizar.
4. **Consultar después:** `pd.read_sql()` recupera los datos sin llamar de nuevo a la API.
5. **Anexar nuevos datos:** Cuando llegan más datos de la API, `if_exists="append"`.

> **¿Por qué guardar en SQLite?** En una hackathon, la API puede caer o tener rate limit. Tener los datos en SQLite te permite seguir trabajando sin depender de internet.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `OperationalError: unable to open database file` | Ruta incorrecta o sin permisos | Verificar la carpeta `recursos/` existe y tiene permisos de escritura |
| `ValueError` | Las columnas del DataFrame no coinciden con la tabla existente al hacer append | Asegurar que los nombres de columna coincidan exactamente |
| `ImportError: No module named 'sqlalchemy'` | SQLAlchemy no instalado | `pip install sqlalchemy` |
| Tabla duplicada | `if_exists="replace"` borra datos previos sin querer | Usar `if_exists="append"` si quieres conservar datos existentes |

---

## 6. Adaptación a la competencia NSAC

Flujo recomendado para la hackathon:

1. Consultar la API de la NASA con `requests`.
2. Normalizar con `pd.json_normalize()`.
3. Guardar en SQLite con `df.to_sql(if_exists="append")`.
4. Cuando necesites los datos, leer con `pd.read_sql_table()` en lugar de llamar otra vez a la API.
5. Usar FastAPI (próxima sección) para exponer esos datos guardados al resto del equipo.

Siguiente paso sugerido: `sqlite_sqlalchemy/clase1_sqlite_basico` para aprender SQL puro y SQLAlchemy ORM en profundidad.