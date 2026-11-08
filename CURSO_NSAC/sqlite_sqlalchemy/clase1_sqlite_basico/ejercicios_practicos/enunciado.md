# Ejercicios Prácticos - Clase 1: SQLite básico con `sqlite3`

## Objetivo
Dominar el ciclo completo de vida de los datos en SQLite (CRUD): crear tablas, insertar registros de forma segura, consultar con filtros, actualizar y eliminar, sin romper la integridad de la base de datos.

## Qué hay que hacer

1. **Crear conexión y tabla:** Conecta a una base de datos SQLite (crea el archivo si no existe). Crea una tabla llamada `mision_espacial` con las siguientes columnas: id (entero, clave primaria, autoincremental), nombre_asteroide (texto, no nulo), diametro_km (decimal, no nulo), peligroso (entero, 0 o 1), fecha_acercamiento (texto), fecha_registro (texto con valor por defecto de la fecha actual).

2. **Insertar un registro seguro:** Inserta un asteroide usando parámetros seguros con `?` (nunca concatenar strings en el SQL). Verifica que se haya insertado consultando el `lastrowid` del cursor.

3. **Insertar varios registros de una vez:** Prepara una lista de al menos 5 asteroides con sus datos y usa `executemany()` para insertarlos todos en una sola operación. Confirma los cambios con `commit()`.

4. **Consultar todos los registros:** Ejecuta un `SELECT * FROM mision_espacial` e imprime cada fila con un formato legible (por ejemplo: "ID 1 - Nombre: X, Diámetro: Y km, Peligroso: Sí/No").

5. **Consultar con filtro WHERE:** Consulta solo los asteroides potencialmente peligrosos (`peligroso = 1`) y muestra sus nombres y fechas de acercamiento. También consulta los asteroides con diámetro mayor a un valor que tú elijas.

6. **Actualizar un registro:** Elige un ID existente y actualiza su diámetro usando `UPDATE ... WHERE id = ?`. Confirma con `commit()` y luego consulta ese registro para verificar que el cambio se aplicó.

7. **Eliminar un registro:** Elige un ID que quieras eliminar y ejecuta `DELETE FROM mision_espacial WHERE id = ?`. Confirma con `commit()` y verifica que el registro ya no aparece al listar todos.

8. **Manejo de errores:** Envuelve al menos una de las operaciones (insertar, actualizar o eliminar) en un bloque `try/except` que capture `sqlite3.Error` y muestre un mensaje amigable si algo falla (por ejemplo, intentar insertar en una columna que no permite nulos sin proporcionar el valor).

## Resultado esperado

- Un archivo `.db` de SQLite creado con la tabla `mision_espacial`.
- Al menos 6 registros insertados (1 individual + 5 con executemany).
- Salida en consola de todos los registros con formato legible.
- Salida en consola del filtro de peligrosos y del filtro por diámetro.
- Al menos un registro actualizado correctamente (verificado tras la actualización).
- Al menos un registro eliminado correctamente (verificado tras la eliminación).
- Un bloque `try/except` que capture y maneje un error de base de datos sin cerrar el programa.
- La conexión se cierra correctamente al final con `close()`.

## Pistas

- Siempre usa `conexion.commit()` después de INSERT, UPDATE o DELETE, o los cambios se perderán.
- Usa `?` como marcador de posición para parámetros y pasa una tupla con los valores: `cursor.execute("INSERT ... VALUES (?, ?)", (valor1, valor2))`.
- `cursor.fetchall()` devuelve todas las filas como lista de tuplas.
- `cursor.lastrowid` te da el ID asignado automáticamente al último insert.

## Dificultad

Principiante

---