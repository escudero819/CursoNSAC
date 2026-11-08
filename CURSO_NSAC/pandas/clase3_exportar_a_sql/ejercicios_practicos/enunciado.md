# Ejercicios Prácticos - Clase 3: Exportar DataFrames de `pandas` a SQL (SQLite)

## Objetivo
Persistir datos de pandas en una base de datos SQLite local, leerlos de vuelta, y gestionar la adición de nuevos registros sin duplicar información existente.

## Qué hay que hacer

1. **Crear un DataFrame de datos espaciales:** Construye un DataFrame con al menos 8 registros de asteroides o eventos espaciales (nombre, diámetro, potencialmente peligroso, fecha de acercamiento). Asegúrate de que los tipos de datos sean adecuados (texto, decimal, booleano, fecha).

2. **Exportar a SQLite (reemplazar):** Conecta a una base de datos SQLite usando SQLAlchemy (`create_engine`) y guarda el DataFrame en una tabla llamada `eventos_espaciales` usando `df.to_sql()` con `if_exists="replace"`. Verifica que la tabla se creó y que contiene los datos.

3. **Leer la tabla de vuelta a pandas:** Usa `pd.read_sql_table()` para leer la tabla completa y convertirla nuevamente en un DataFrame. Imprime el resultado para confirmar que los datos se leyeron correctamente.

4. **Consulta SQL personalizada:** Usa `pd.read_sql()` con una consulta SQL personalizada para obtener solo los registros potencialmente peligrosos, o solo aquellos con diámetro mayor a un valor específico. Muestra el resultado.

5. **Anexar nuevos registros sin duplicar:** Crea un segundo DataFrame con 3 registros nuevos (algunos pueden repetir nombre o fecha con los existentes). Intenta agregarlos a la misma tabla con `if_exists="append"`. Luego lee la tabla completa y verifica que ahora tiene más filas que antes.

6. **Evitar duplicados al insertar:** Antes de insertar los 3 registros nuevos, verifica uno por uno si ya existe un registro con el mismo nombre y fecha en la base de datos. Solo inserta los que no existan. Cuenta cuántos se insertaron realmente y cuántos se omitieron por ser duplicados.

## Resultado esperado

- Un archivo `.db` de SQLite creado en tu carpeta con la tabla `eventos_espaciales`.
- El DataFrame original exportado y luego leído de vuelta sin pérdida de datos.
- Al menos una consulta SQL personalizada que filtre registros (por ejemplo, solo peligrosos).
- La tabla contenga los registros originales más los nuevos anexados (al menos 11 filas totales si empezaste con 8 y agregaste 3).
- Al ejecutar el proceso de evitar duplicados, se muestre por consola cuántos registros se insertaron y cuántos se omitieron por ya existir.
- No se lancen errores de clave duplicada ni de estructura de tabla al hacer el append.

## Pistas

- `create_engine("sqlite:///nombre.db")` crea o abre la base de datos.
- `df.to_sql("nombre_tabla", con=engine, if_exists="replace", index=False)` guarda el DataFrame.
- `pd.read_sql_table("nombre_tabla", con=engine)` lee toda la tabla.
- `pd.read_sql("SELECT * FROM tabla WHERE condicion", con=engine)` ejecuta consultas personalizadas.
- Para verificar existencia antes de insertar, puedes consultar la tabla con `read_sql_table` y filtrar en pandas, o ejecutar una consulta SQL `SELECT COUNT(*)`.

## Dificultad

Intermedio

---