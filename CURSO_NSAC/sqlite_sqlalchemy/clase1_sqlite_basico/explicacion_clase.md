# Clase 1 - SQLite básico (`sqlite3`)

## 1. Explicación del ejemplo

SQLite es una base de datos ligera que guarda todo en un solo archivo. No necesita servidor ni instalación, viene incluida con Python (`sqlite3`).

Este archivo contiene seis ejemplos que cubren el ciclo completo de vida de los datos (CRUD):

1. **Crear conexión:** `sqlite3.connect()` abre o crea el archivo `.db`.
2. **Crear tabla:** `CREATE TABLE` con tipos de datos y restricciones (`NOT NULL`, `PRIMARY KEY`, `DEFAULT`).
3. **Insertar uno:** `INSERT` con parámetros seguros `?`.
4. **Insertar varios:** `executemany()` para cargar múltiples registros eficientemente.
5. **Consultar:** `SELECT` con filtro opcional (`WHERE peligroso = 1`).
6. **Actualizar y eliminar:** `UPDATE` y `DELETE` con condición `WHERE`.

---

## 2. Explicación de la clase / conceptos clave

### ¿Por qué parámetros `?` y no concatenar strings?

**Nunca hagas esto (inyección SQL):**
```python
# PELIGROSO: un usuario podría inyectar SQL malicioso
cursor.execute(f"SELECT * FROM asteroides WHERE nombre = '{nombre_usuario}'")
```

**Haz esto (seguro):**
```python
cursor.execute("SELECT * FROM asteroides WHERE nombre = ?", (nombre_usuario,))
```

SQLite reemplaza el `?` por el valor de forma segura, escapando caracteres especiales automáticamente.

### Tipos de datos en SQLite

| Tipo SQLite | Uso típico | Ejemplo |
|-------------|------------|---------|
| `INTEGER` | Números enteros | IDs, conteos, booleano (0/1) |
| `REAL` | Números decimales | Diámetro, velocidad, distancia |
| `TEXT` | Texto | Nombres, fechas, descripciones |
| `BLOB` | Datos binarios | Imágenes, archivos |

### Sentencias SQL principales

| Sentencia | Propósito | Ejemplo simplificado |
|-----------|-----------|----------------------|
| `CREATE TABLE` | Crear tabla | `CREATE TABLE asteroides (id INTEGER PRIMARY KEY, nombre TEXT)` |
| `INSERT` | Agregar registro | `INSERT INTO asteroides (nombre) VALUES (?)` |
| `SELECT` | Leer registros | `SELECT * FROM asteroides WHERE peligroso = 1` |
| `UPDATE` | Modificar registro | `UPDATE asteroides SET diametro_km = 0.2 WHERE id = 1` |
| `DELETE` | Eliminar registro | `DELETE FROM asteroides WHERE id = 1` |

### Confirmar cambios (`commit`)

En SQLite, los cambios de `INSERT`, `UPDATE` y `DELETE` no se guardan hasta que llames a `conexion.commit()`. Si olvidas el `commit`, los datos se perderán al cerrar la conexión.

---

## 3. Diccionario de sintaxis global - `sqlite3`

```python
import sqlite3

# Conectar (crea el archivo si no existe)
conexion = sqlite3.connect("datos.db")

# Crear cursor para ejecutar SQL
cursor = conexion.cursor()

# Ejecutar SQL con parámetros seguros
cursor.execute("CREATE TABLE IF NOT EXISTS tabla (col1 TEXT, col2 INTEGER)")
cursor.execute("INSERT INTO tabla VALUES (?, ?)", ("valor1", 123))
cursor.executemany("INSERT INTO tabla VALUES (?, ?)", [("a", 1), ("b", 2)])

# Confirmar cambios
conexion.commit()

# Consultar
cursor.execute("SELECT * FROM tabla")
filas = cursor.fetchall()      # Todas las filas
fila = cursor.fetchone()       # Solo la primera

# Cerrar
conexion.close()
```

---

## 4. Flujo de trabajo lógico (razonamiento de un data scientist)

1. **Diseñar el esquema:** ¿Qué tablas necesitas? ¿Qué columnas y tipos?
2. **Conectar:** `sqlite3.connect()`.
3. **Crear estructura:** `CREATE TABLE IF NOT EXISTS`.
4. **Cargar datos:** `INSERT` o `executemany()` con parámetros `?`.
5. **Consultar:** `SELECT` con filtros según lo que necesites analizar.
6. **Actualizar/eliminar:** Solo si es necesario (en hackathon, suele ser más común solo insertar y consultar).
7. **Guardar y cerrar:** `commit()` y `close()`.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `OperationalError: table asteroides already exists` | Intentaste crear una tabla que ya existe | Usar `CREATE TABLE IF NOT EXISTS` |
| `ProgrammingError` | Número incorrecto de parámetros `?` | Verificar que la tupla tenga tantos elementos como `?` |
| `IntegrityError` | Violaste una restricción (ej. NOT NULL, UNIQUE) | Revisar que no faltan valores obligatorios |
| Cambios no guardados | Olvidaste `conexion.commit()` | Llamar a `commit()` después de INSERT/UPDATE/DELETE |

---

## 6. Adaptación a la competencia NSAC

En la hackathon usa SQLite para:

- Guardar los datos de la NASA que ya consultaste (evita llamar otra vez a la API).
- Almacenar registros personalizados que tu equipo genere (usuarios, reportes, alertas).
- Compartir el archivo `.db` con el equipo para que todos trabajen con los mismos datos.

Siguiente paso sugerido: `clase2_orm_sqlalchemy` para aprender a usar SQLAlchemy ORM, que te permite trabajar con tablas como clases de Python en lugar de escribir SQL a mano.