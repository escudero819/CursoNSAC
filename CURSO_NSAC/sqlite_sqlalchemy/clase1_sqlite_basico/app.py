"""
Clase 1 - SQLite básico (SQL puro con sqlite3)

Objetivo:
- Crear una base de datos SQLite desde Python.
- Crear tablas con tipos de datos y restricciones.
- Insertar, consultar, actualizar y eliminar registros (CRUD).
- Usar parámetros seguros para evitar inyección SQL.
- Manejar errores comunes de base de datos.

Requisitos:
- sqlite3 viene incluido con Python (no necesita instalación externa)
"""

import sqlite3
from datetime import date


RUTA_BD = "recursos/datos_nasa.db"


def crear_conexion():
    """
    Crea y devuelve una conexión a la base de datos SQLite.
    Si el archivo no existe, SQLite lo crea automáticamente.
    """
    try:
        conexion = sqlite3.connect(RUTA_BD)
        print(f"✓ Conexión establecida con '{RUTA_BD}'")
        return conexion
    except sqlite3.Error as e:
        print(f"✗ Error al conectar con la BD: {e}")
        return None


def crear_tabla(conexion):
    """
    Ejemplo 1: Crear una tabla para almacenar asteroides.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 1: Crear tabla en SQLite")
    print("=" * 70)

    sentencia_sql = """
    CREATE TABLE IF NOT EXISTS asteroides (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        diametro_km REAL NOT NULL,
        peligroso INTEGER DEFAULT 0,   -- 0 = False, 1 = True
        fecha_acercamiento TEXT NOT NULL,
        fecha_registro TEXT DEFAULT (date('now'))
    );
    """

    try:
        cursor = conexion.cursor()
        cursor.execute(sentencia_sql)
        conexion.commit()
        print("✓ Tabla 'asteroides' creada (o ya existía).")
    except sqlite3.Error as e:
        print(f"✗ Error al crear tabla: {e}")


def insertar_asteroide(conexion, nombre, diametro, peligroso, fecha):
    """
    Ejemplo 2: Insertar un registro usando parámetros seguros (?).
    NUNCA concatenar valores directamente en el SQL (riesgo de inyección SQL).
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Insertar registro (INSERT)")
    print("=" * 70)

    sentencia = """
    INSERT INTO asteroides (nombre, diametro_km, peligroso, fecha_acercamiento)
    VALUES (?, ?, ?, ?);
    """

    try:
        cursor = conexion.cursor()
        cursor.execute(sentencia, (nombre, diametro, int(peligroso), fecha))
        conexion.commit()
        print(f"✓ Asteroide '{nombre}' insertado con ID {cursor.lastrowid}.")
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"✗ Error al insertar: {e}")
        return None


def insertar_varios_asteroides(conexion, lista_asteroides):
    """
    Ejemplo 3: Insertar varios registros de una vez con executemany.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Insertar varios registros (executemany)")
    print("=" * 70)

    sentencia = """
    INSERT INTO asteroides (nombre, diametro_km, peligroso, fecha_acercamiento)
    VALUES (?, ?, ?, ?);
    """

    try:
        cursor = conexion.cursor()
        cursor.executemany(sentencia, lista_asteroides)
        conexion.commit()
        print(f"✓ {cursor.rowcount} asteroide(s) insertado(s).")
    except sqlite3.Error as e:
        print(f"✗ Error al insertar varios: {e}")


def consultar_asteroides(conexion, solo_peligrosos=False):
    """
    Ejemplo 4: Consultar registros (SELECT).
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Consultar registros (SELECT)")
    print("=" * 70)

    if solo_peligrosos:
        sentencia = "SELECT id, nombre, diametro_km, fecha_acercamiento FROM asteroides WHERE peligroso = 1;"
    else:
        sentencia = "SELECT id, nombre, diametro_km, peligroso, fecha_acercamiento FROM asteroides;"

    try:
        cursor = conexion.cursor()
        cursor.execute(sentencia)
        filas = cursor.fetchall()

        print(f"✓ Se encontraron {len(filas)} registro(s):")
        for fila in filas:
            print(f"  ID {fila[0]} | {fila[1]} | Ø {fila[2]} km | Peligroso: {'Sí' if fila[3] else 'No'} | {fila[4] if len(fila) > 4 else ''}")
        return filas
    except sqlite3.Error as e:
        print(f"✗ Error al consultar: {e}")
        return []


def actualizar_asteroide(conexion, id_asteroide, nuevo_diametro):
    """
    Ejemplo 5: Actualizar un registro (UPDATE).
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Actualizar registro (UPDATE)")
    print("=" * 70)

    sentencia = "UPDATE asteroides SET diametro_km = ? WHERE id = ?;"

    try:
        cursor = conexion.cursor()
        cursor.execute(sentencia, (nuevo_diametro, id_asteroide))
        conexion.commit()
        if cursor.rowcount > 0:
            print(f"✓ Asteroide ID {id_asteroide} actualizado. Diámetro: {nuevo_diametro} km.")
        else:
            print(f"✗ No se encontró ningún asteroide con ID {id_asteroide}.")
    except sqlite3.Error as e:
        print(f"✗ Error al actualizar: {e}")


def eliminar_asteroide(conexion, id_asteroide):
    """
    Ejemplo 6: Eliminar un registro (DELETE).
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 6: Eliminar registro (DELETE)")
    print("=" * 70)

    sentencia = "DELETE FROM asteroides WHERE id = ?;"

    try:
        cursor = conexion.cursor()
        cursor.execute(sentencia, (id_asteroide,))
        conexion.commit()
        if cursor.rowcount > 0:
            print(f"✓ Asteroide ID {id_asteroide} eliminado.")
        else:
            print(f"✗ No se encontró ningún asteroide con ID {id_asteroide}.")
    except sqlite3.Error as e:
        print(f"✗ Error al eliminar: {e}")


def cerrar_conexion(conexion):
    if conexion:
        conexion.close()
        print("\n✓ Conexión cerrada.")


if __name__ == "__main__":
    # 1. Conectar
    conexion = crear_conexion()
    if not conexion:
        exit()

    try:
        # 2. Crear tabla
        crear_tabla(conexion)

        # 3. Insertar uno por uno
        insertar_asteroide(conexion, "(2026 AB1)", 0.15, False, "2026-11-01")
        insertar_asteroide(conexion, "(2026 CD2)", 0.42, True, "2026-11-01")

        # 4. Insertar varios de una vez
        lista_nuevos = [
            ("(2026 EF3)", 0.08, False, "2026-11-02"),
            ("(2026 GH4)", 1.20, True, "2026-11-03"),
        ]
        insertar_varios_asteroides(conexion, lista_nuevos)

        # 5. Consultar todos
        consultar_asteroides(conexion)

        # 6. Consultar solo peligrosos
        print("\n--- Solo peligrosos ---")
        consultar_asteroides(conexion, solo_peligrosos=True)

        # 7. Actualizar
        actualizar_asteroide(conexion, id_asteroide=1, nuevo_diametro=0.18)

        # 8. Consultar para verificar
        consultar_asteroides(conexion)

        # 9. Eliminar uno (opcional, comentado para conservar datos de ejemplo)
        # eliminar_asteroide(conexion, id_asteroide=4)

    finally:
        cerrar_conexion(conexion)