"""
Clase 1 - Estructuras de datos con pandas

Objetivo:
- Entender las dos estructuras principales de pandas: Series y DataFrame.
- Crear DataFrames desde diccionarios, listas y JSON.
- Leer archivos CSV y JSON.
- Explorar datos básicos (head, info, describe, shape).
- Seleccionar filas y columnas.

Requisitos:
- pip install pandas
"""

import pandas as pd
import json


def crear_series_y_dataframe():
    """
    Ejemplo 1: Crear una Series y un DataFrame desde diccionarios y listas.
    """
    print("=" * 70)
    print("EJEMPLO 1: Series y DataFrame básicos")
    print("=" * 70)

    # --- Series: arreglo unidimensional con etiquetas (índice) ---
    temperaturas = pd.Series([22.5, 24.1, 19.8, 21.3, 23.7],
                             index=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
                             name="Temperatura (°C)")

    print("\n--- Series (temperaturas diarias) ---")
    print(temperaturas)
    print(f"\nTipo: {type(temperaturas)}")

    # --- DataFrame: tabla bidimensional (como Excel o SQL) ---
    datos_asteroides = {
        "nombre": ["(2026 AB1)", "(2026 CD2)", "(2026 EF3)"],
        "diametro_km": [0.15, 0.42, 0.08],
        "peligroso": [False, True, False],
        "fecha_acercamiento": ["2026-11-02", "2026-11-03", "2026-11-04"]
    }

    df = pd.DataFrame(datos_asteroides)

    print("\n--- DataFrame (asteroides cercanos) ---")
    print(df)
    print(f"\nDimensiones (filas, columnas): {df.shape}")
    print(f"Columnas: {list(df.columns)}")


def leer_json_y_csv():
    """
    Ejemplo 2: Leer datos desde archivos JSON y CSV.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Leer JSON y CSV")
    print("=" * 70)

    # Crear un archivo JSON de ejemplo (simulando respuesta de API)
    json_ejemplo = [
        {"id": 1, "nombre": "Marte", "tipo": "planeta", "distancia_sol": 227.9},
        {"id": 2, "nombre": "Fobos", "tipo": "luna", "distancia_sol": 227.9},
        {"id": 3, "nombre": "Deimos", "tipo": "luna", "distancia_sol": 227.9}
    ]
    with open("recursos/cuerpos_celestes.json", "w", encoding="utf-8") as f:
        json.dump(json_ejemplo, f, ensure_ascii=False, indent=2)

    # Leer JSON con pandas
    df_json = pd.read_json("recursos/cuerpos_celestes.json")
    print("\n--- DataFrame desde JSON ---")
    print(df_json)

    # Crear un CSV de ejemplo
    csv_contenido = """fecha,objeto,distancia_km,velocidad_km_s
2026-11-01,AST-001,150000,28.4
2026-11-02,AST-002,320000,15.2
2026-11-03,AST-001,145000,28.6
"""
    with open("recursos/asteroides.csv", "w", encoding="utf-8") as f:
        f.write(csv_contenido)

    # Leer CSV con pandas
    df_csv = pd.read_csv("recursos/asteroides.csv")
    print("\n--- DataFrame desde CSV ---")
    print(df_csv)


def explorar_datos(df):
    """
    Ejemplo 3: Exploración rápida de un DataFrame.
    Métodos clave para entender los datos en segundos.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Exploración de datos (head, info, describe)")
    print("=" * 70)

    print("\n--- Primeras 3 filas (head) ---")
    print(df.head(3))

    print("\n--- Información general (info) ---")
    df.info()

    print("\n--- Estadísticas descriptivas (describe) ---")
    print(df.describe(include="all"))

    print("\n--- Valores nulos por columna ---")
    print(df.isnull().sum())


def seleccionar_datos(df):
    """
    Ejemplo 4: Selección de filas y columnas.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Selección de datos")
    print("=" * 70)

    # Seleccionar una columna (devuelve Series)
    print("\n--- Columna 'nombre' ---")
    print(df["nombre"])

    # Seleccionar varias columnas (devuelve DataFrame)
    print("\n--- Columnas 'nombre' y 'peligroso' ---")
    print(df[["nombre", "peligroso"]])

    # Filtrar filas con condición (booleano)
    print("\n--- Asteroides peligrosos (peligroso == True) ---")
    peligrosos = df[df["peligroso"] == True]
    print(peligrosos)

    # Filtrar por condición numérica
    print("\n--- Diámetro mayor a 0.1 km ---")
    grandes = df[df["diametro_km"] > 0.1]
    print(grandes)

    # Acceder por posición (iloc) y por etiqueta (loc)
    print("\n--- Primera fila con iloc ---")
    print(df.iloc[0])

    print("\n--- Fila con índice 2 usando loc ---")
    print(df.loc[2])


if __name__ == "__main__":
    crear_series_y_dataframe()

    # Creamos un DataFrame de ejemplo para explorar y seleccionar
    datos_ejemplo = {
        "nombre": ["(2026 AB1)", "(2026 CD2)", "(2026 EF3)", "(2026 GH4)"],
        "diametro_km": [0.15, 0.42, 0.08, 1.2],
        "peligroso": [False, True, False, True],
        "fecha_acercamiento": ["2026-11-02", "2026-11-03", "2026-11-04", "2026-11-05"]
    }
    df_asteroides = pd.DataFrame(datos_ejemplo)

    leer_json_y_csv()
    explorar_datos(df_asteroides)
    seleccionar_datos(df_asteroides)