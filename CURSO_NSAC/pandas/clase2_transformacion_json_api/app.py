"""
Clase 2 - Transformación de JSON de APIs con pandas

Objetivo:
- Aplanar JSON anidados (muy común en respuestas de la NASA).
- Usar json_normalize para convertir JSON jerárquico a DataFrame plano.
- Filtrar, agrupar y agregar datos.
- Combinar DataFrames (merge, concat).
- Exportar a CSV y Excel.

Requisitos:
- pip install pandas
"""

import pandas as pd
import json


def json_anidado_a_dataframe():
    """
    Ejemplo 1: Aplanar un JSON anidado (tipo respuesta de NASA NeoWs).
    json_normalize convierte estructuras jerárquicas en columnas planas.
    """
    print("=" * 70)
    print("EJEMPLO 1: Aplanar JSON anidado con json_normalize")
    print("=" * 70)

    # Simulamos una respuesta simplificada de NASA NeoWs
    json_nasa = {
        "element_count": 3,
        "near_earth_objects": {
            "2026-11-01": [
                {
                    "name": "(2026 AB1)",
                    "absolute_magnitude_h": 22.5,
                    "estimated_diameter": {
                        "kilometers": {
                            "estimated_diameter_min": 0.10,
                            "estimated_diameter_max": 0.22
                        }
                    },
                    "is_potentially_hazardous_asteroid": False,
                    "close_approach_data": [
                        {
                            "close_approach_date": "2026-11-01",
                            "relative_velocity": {"kilometers_per_hour": 28450},
                            "miss_distance": {"kilometers": 15000000}
                        }
                    ]
                },
                {
                    "name": "(2026 CD2)",
                    "absolute_magnitude_h": 19.8,
                    "estimated_diameter": {
                        "kilometers": {
                            "estimated_diameter_min": 0.30,
                            "estimated_diameter_max": 0.55
                        }
                    },
                    "is_potentially_hazardous_asteroid": True,
                    "close_approach_data": [
                        {
                            "close_approach_date": "2026-11-01",
                            "relative_velocity": {"kilometers_per_hour": 15200},
                            "miss_distance": {"kilometers": 32000000}
                        }
                    ]
                }
            ]
        }
    }

    # Extraemos la lista de asteroides por fecha
    asteroides_por_fecha = json_nasa["near_earth_objects"]
    lista_asteroides = []
    for fecha, asteroides in asteroides_por_fecha.items():
        for ast in asteroides:
            ast["fecha_consulta"] = fecha  # Agregamos la fecha como columna
            lista_asteroides.append(ast)

    # json_normalize aplana los diccionarios anidados en columnas separadas
    df = pd.json_normalize(lista_asteroides, sep="_")

    print("\n--- DataFrame aplanado ---")
    print(df.to_string(index=False))

    print("\nColumnas resultantes:")
    for col in df.columns:
        print(f"  - {col}")


def filtrar_y_agrupar(df):
    """
    Ejemplo 2: Filtrado, agrupación y agregación de datos.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Filtrado, agrupación y agregación")
    print("=" * 70)

    # Filtrar solo asteroides potencialmente peligrosos
    peligrosos = df[df["is_potentially_hazardous_asteroid"] == True]
    print("\n--- Asteroides potencialmente peligrosos ---")
    print(peligrosos[["name", "fecha_consulta", "estimated_diameter_kilometers_estimated_diameter_max"]].to_string(index=False))

    # Agrupar por fecha y contar cuántos asteroides hay cada día
    conteo_por_fecha = df.groupby("fecha_consulta").size().reset_index(name="cantidad_asteroides")
    print("\n--- Cantidad de asteroides por fecha ---")
    print(conteo_por_fecha)

    # Diámetro máximo promedio por fecha
    promedio_por_fecha = df.groupby("fecha_consulta")["estimated_diameter_kilometers_estimated_diameter_max"].mean().reset_index()
    print("\n--- Diámetro máximo promedio por fecha ---")
    print(promedio_por_fecha)


def combinar_dataframes():
    """
    Ejemplo 3: Combinar DataFrames con merge y concat.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Combinar DataFrames (merge y concat)")
    print("=" * 70)

    # DataFrame de asteroides
    df_asteroides = pd.DataFrame({
        "id_asteroide": [1, 2, 3],
        "nombre": ["(2026 AB1)", "(2026 CD2)", "(2026 EF3)"],
        "peligroso": [False, True, False]
    })

    # DataFrame de acercamientos (más datos por asteroide)
    df_acercamientos = pd.DataFrame({
        "id_asteroide": [1, 2, 3],
        "fecha": ["2026-11-01", "2026-11-01", "2026-11-02"],
        "distancia_km": [15000000, 32000000, 8000000]
    })

    # merge: unir por columna común (como JOIN en SQL)
    df_combinado = pd.merge(df_asteroides, df_acercamientos, on="id_asteroide", how="inner")
    print("\n--- DataFrames unidos con merge (inner join) ---")
    print(df_combinado.to_string(index=False))

    # concat: apilar DataFrames verticalmente
    df_extra = pd.DataFrame({
        "id_asteroide": [4],
        "nombre": ["(2026 GH4)"],
        "peligroso": [True]
    })
    df_apilado = pd.concat([df_asteroides, df_extra], ignore_index=True)
    print("\n--- DataFrames apilados con concat ---")
    print(df_apilado.to_string(index=False))


def exportar_datos(df):
    """
    Ejemplo 4: Exportar a CSV y Excel.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Exportar datos")
    print("=" * 70)

    # Exportar a CSV
    df.to_csv("recursos/asteroides_procesados.csv", index=False, encoding="utf-8")
    print("\n✓ Exportado a 'recursos/asteroides_procesados.csv'")

    # Exportar a Excel (requiere openpyxl: pip install openpyxl)
    try:
        df.to_excel("recursos/asteroides_procesados.xlsx", index=False)
        print("✓ Exportado a 'recursos/asteroides_procesados.xlsx'")
    except ImportError:
        print("✗ Para exportar a Excel, instala: pip install openpyxl")


if __name__ == "__main__":
    # Ejecutamos el ejemplo 1 y capturamos el DataFrame para usarlo en los siguientes
    json_anidado_a_dataframe()

    # Recreamos el DataFrame para los ejemplos 2, 3 y 4
    datos = [
        {
            "name": "(2026 AB1)",
            "absolute_magnitude_h": 22.5,
            "estimated_diameter_kilometers_estimated_diameter_min": 0.10,
            "estimated_diameter_kilometers_estimated_diameter_max": 0.22,
            "is_potentially_hazardous_asteroid": False,
            "fecha_consulta": "2026-11-01",
            "close_approach_data_close_approach_date": "2026-11-01",
            "close_approach_data_relative_velocity_kilometers_per_hour": 28450,
            "close_approach_data_miss_distance_kilometers": 15000000
        },
        {
            "name": "(2026 CD2)",
            "absolute_magnitude_h": 19.8,
            "estimated_diameter_kilometers_estimated_diameter_min": 0.30,
            "estimated_diameter_kilometers_estimated_diameter_max": 0.55,
            "is_potentially_hazardous_asteroid": True,
            "fecha_consulta": "2026-11-01",
            "close_approach_data_close_approach_date": "2026-11-01",
            "close_approach_data_relative_velocity_kilometers_per_hour": 15200,
            "close_approach_data_miss_distance_kilometers": 32000000
        },
        {
            "name": "(2026 EF3)",
            "absolute_magnitude_h": 21.0,
            "estimated_diameter_kilometers_estimated_diameter_min": 0.05,
            "estimated_diameter_kilometers_estimated_diameter_max": 0.12,
            "is_potentially_hazardous_asteroid": False,
            "fecha_consulta": "2026-11-02",
            "close_approach_data_close_approach_date": "2026-11-02",
            "close_approach_data_relative_velocity_kilometers_per_hour": 22100,
            "close_approach_data_miss_distance_kilometers": 8000000
        }
    ]
    df = pd.DataFrame(datos)

    filtrar_y_agrupar(df)
    combinar_dataframes()
    exportar_datos(df)