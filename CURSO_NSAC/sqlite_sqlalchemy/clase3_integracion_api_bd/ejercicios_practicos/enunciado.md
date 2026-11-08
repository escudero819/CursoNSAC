# Ejercicios Prácticos - Clase 3: Integración API de la NASA + pandas + SQLAlchemy

## Objetivo
Ejecutar un flujo ETL completo (Extraer, Transformar, Cargar) que consume datos de la API de la NASA, los transforma con pandas y los guarda en SQLite evitando duplicados, para luego consultarlos localmente.

## Qué hay que hacer

1. **Extraer datos de la NASA:** Consulta un endpoint de la NASA (puede ser NeoWs para asteroides o EONET para eventos naturales) con `requests`, usando tu API key y un rango de fechas. Maneja posibles errores de red con `try/except`.

2. **Transformar con pandas:** Recibe el JSON de la respuesta y conviértelo en un DataFrame plano. Si el JSON está anidado, usa `pd.json_normalize()` o navega manualmente hasta la lista de objetos. Selecciona solo las columnas que te interesen (nombre, fecha, diámetro, peligroso, distancia, velocidad, etc.).

3. **Limpiar los datos:** Revisa valores nulos con `isnull().sum()` y decida cómo manejarlos (rellenar con `fillna()` o eliminar con `dropna()`). Convierte las fechas al formato adecuado si es necesario.

4. **Cargar a SQLite evitando duplicados:** Con SQLAlchemy, define un modelo que coincida con las columnas de tu DataFrame. Antes de insertar cada registro, verifica si ya existe en la base de datos (por ejemplo, por nombre + fecha). Inserta solo los nuevos y cuenta cuántos se agregaron y cuántos se omitieron por ser duplicados.

5. **Consultar los datos guardados:** Lee la tabla completa de vuelta a un DataFrame con `pd.read_sql_table()` o consulta con SQLAlchemy. Imprime cuántos registros hay en total y muestra algunos ejemplos.

6. **Consulta filtrada desde la BD:** Desde SQLite, obtén solo los registros potencialmente peligrosos o solo los de una fecha específica. Muestra el resultado en consola.

7. **Ejecutar el flujo dos veces:** Ejecuta todo el script dos veces con el mismo rango de fechas. La segunda vez no debería insertar registros nuevos (todos deberían ser detectados como duplicados y omitidos).

## Resultado esperado

- Un script que complete todo el flujo ETL sin intervención manual.
- Al menos una consulta exitosa a la API de la NASA con datos recibidos.
- Un DataFrame limpio y plano listo para guardar.
- Un archivo `.db` de SQLite con la tabla poblada con datos de la NASA.
- Salida en consola que indique cuántos registros se insertaron y cuántos se omitieron por duplicados.
- Al menos una consulta filtrada desde SQLite (por ejemplo, solo peligrosos).
- Al ejecutar el script dos veces, la segunda inserción deje 0 registros nuevos.

## Pistas

- Para evitar duplicados, consulta la base de datos antes de cada `session.add()`.
- Usa `datetime.strptime(fecha_str, "%Y-%m-%d").date()` para convertir strings de fecha a objetos `date` de Python.
- `session.query(Modelo).filter(Modelo.campo == valor).first()` devuelve `None` si no existe, lo cual es útil para verificar duplicados.
- `Base.metadata.create_all(engine)` crea las tablas si no existen.

## Dificultad

Avanzado

---