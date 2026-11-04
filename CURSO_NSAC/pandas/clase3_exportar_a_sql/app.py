"""
Clase 3 - Exportar DataFrames de pandas a SQL (SQLite)

Objetivo:
- Guardar un DataFrame de pandas en una tabla de SQLite.
- Leer una tabla de SQLite y convertirla en DataFrame.
- Anexar datos a una tabla existente (if_exists="append").
- Reemplazar una tabla existente (if_exists="replace").
- Usar pandas con SQLAlchemy como motor de conexión.

Requisitos:
- pip install pandas sqlalchemy
"""

import pandas as pd
from sqlalchemy import create_engine


def crear_dataframe_ejemplo():
    """
    Crea un DataFrame de ejemplo con datos tipo NASA (asteroides).
    """
    datos = [
        {"nombre": "(2026 AB1)", "diametro_km": 0.15, "peligroso": False, "fecha": "2026-11-01"},
        {"nombre": "(2026 CD2)", "diametro_km": 0.42, "peligroso": True, "fecha": "2026-11-01"},
        {"nombre": "(2026 EF3)", "diametro_km": 0.08, "peligroso": False, "fecha": "2026-11-02"},
        {"nombre": "(2026 GH4)", "diametro_km": 1.20, "peligroso": True, "fecha": "2026-11-03"},
    ]
    return pd.DataFrame(datos)


def exportar_dataframe_a_sqlite(df, nombre_db="recursos/datos_nasa.db", nombre_tabla="asteroides"):
    """
    Ejemplo 1: Guardar un DataFrame en SQLite usando to_sql.
    """
    print("=" * 70)
    print("EJEMPLO 1: Exportar DataFrame a SQLite con to_sql")
    print("=" * 70)

    # create_engine crea la conexión a la base de datos SQLite
    # Si el archivo no existe, SQLite lo crea automáticamente
    engine = create_engine(f"sqlite:///{nombre_db}")

    try:
        # to_sql escribe el DataFrame en una tabla SQL
        # if_exists="replace": borra la tabla si existe y la crea de nuevo
        # if_exists="append": agrega filas a la tabla existente
        # if_exists="fall": lanza error si la tabla ya existe (por defecto)
        df.to_sql(
            name=nombre_tabla,
            con=engine,
            if_exists="replace",  # Cambia a "append" para no borrar datos previos
            index=False           # No escribir el índice del DataFrame como columna
        )
        print(f"✓ DataFrame exportado a tabla '{nombre_tabla}' en '{nombre_db}'")
        print(f"  Filas exportadas: {len(df)}")

    except Exception as e:
        print(f"✗ Error al exportar a SQLite: {e}")

    return engine


def leer_sqlite_a_dataframe(nombre_db="recursos/datos_nasa.db", nombre_tabla="asteroides"):
    """
    Ejemplo 2: Leer una tabla de SQLite y convertirla en DataFrame.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Leer tabla de SQLite a DataFrame")
    print("=" * 70)

    engine = create_engine(f"sqlite:///{nombre_db}")

    try:
        # read_sql leera toda la tabla
        df_leido = pd.read_sql_table(nombre_tabla, con=engine)
        print("✓ Tabla leída exitosamente:")
        print(df_leido.to_string(index=False))

        # También se puede leer con una consulta SQL personalizada
        consulta = "SELECT nombre, diametro_km FROM asteroides WHERE peligroso = 1"
        df_filtrado = pd.read_sql(consulta, con=engine)
        print("\n--- Consulta personalizada (solo peligrosos) ---")
        print(df_filtrado.to_string(index=False))

        return df_leido

    except Exception as e:
        print(f"✗ Error al leer desde SQLite: {e}")
        return None


def anexar_datos_nuevos(df_nuevos, nombre_db="recursos/datos_nasa.db", nombre_tabla="asteroides"):
    """
    Ejemplo 3: Anexar nuevos registros a una tabla existente sin borrar los anteriores.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Anexar datos nuevos (if_exists='append')")
    print("=" * 70)

    engine = create_engine(f"sqlite:///{nombre_db}")

    try:
        df_nuevos.to_sql(
            name=nombre_tabla,
            con=engine,
            if_exists="append",  # Agrega sin borrar lo existente
            index=False
        )
        print(f"✓ {len(df_nuevos)} registro(s) anexado(s) a '{nombre_tabla}'")

        # Verificamos el total
        total = pd.read_sql_table(nombre_tabla, con=engine)
        print(f"  Total de filas ahora: {len(total)}")

    except Exception as e:
        print(f"✗ Error al anexar datos: {e}")


if __name__ == "__main__":
    # Creamos el DataFrame de ejemplo
    df = crear_dataframe_ejemplo()
    print("DataFrame original:")
    print(df.to_string(index=False))

    # 1. Exportar a SQLite (reemplaza si existe)
    engine = exportar_dataframe_a_sqlite(df)

    # 2. Leer desde SQLite
    leer_sqlite_a_dataframe()

    # 3. Anexar datos nuevos
    df_nuevos = pd.DataFrame([
        {"nombre": "(2026 IJ5)", "diametro_km": 0.55, "peligroso": False, "fecha": "2026-11-04"}
    ])
    anexar_datos_nuevos(df_nuevos)

    print("\n✓ Clase 3 completada. Los datos persisten en el archivo SQLite.")