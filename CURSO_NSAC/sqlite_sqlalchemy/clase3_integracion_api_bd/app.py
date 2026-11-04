"""
Clase 3 - Integracion: API de la NASA + pandas + SQLAlchemy

Objetivo:
- Combinar todo lo aprendido: consultar API de la NASA con requests,
  transformar con pandas y guardar en SQLite con SQLAlchemy.
- Implementar un flujo completo de extraccion, transformacion y carga (ETL).
- Evitar duplicados al guardar datos ya existentes.
- Manejar errores de red y de base de datos de forma integrada.

Requisitos:
- pip install requests pandas sqlalchemy
"""

import requests
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date, datetime, timedelta

# Configuracion
NASA_BASE_URL = "https://api.nasa.gov"
API_KEY = "DEMO_KEY"
RUTA_BD = "sqlite:///recursos/datos_integracion.db"

engine = create_engine(RUTA_BD)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Modelo para almacenar asteroides
class AsteroideNASA(Base):
    __tablename__ = "asteroides_nasa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    diametro_min_km = Column(Float)
    diametro_max_km = Column(Float)
    peligroso = Column(Boolean, default=False)
    fecha_acercamiento = Column(Date, nullable=False)
    velocidad_km_h = Column(Float)
    distancia_km = Column(Float)
    fecha_registro = Column(Date, default=date.today)


def consultar_nasa_neos(fecha_inicio, fecha_fin):
    """Paso 1 - Extraer: Consultar la API NeoWs de la NASA."""
    print("=" * 70)
    print("PASO 1: Consultar API de la NASA (NeoWs)")
    print("=" * 70)

    url = f"{NASA_BASE_URL}/neo/rest/v1/feed"
    params = {
        "api_key": API_KEY,
        "start_date": fecha_inicio,
        "end_date": fecha_fin
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        datos = response.json()
        print(f"API respondio con {datos.get('element_count', 0)} asteroide(s)")
        return datos
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
        return None


def transformar_datos(datos_json):
    """Paso 2 - Transformar: Aplanar JSON anidado con pandas y preparar para SQL."""
    print("\n" + "=" * 70)
    print("PASO 2: Transformar datos con pandas")
    print("=" * 70)

    if not datos_json:
        return pd.DataFrame()

    cercanias_por_fecha = datos_json.get("near_earth_objects", {})
    filas = []

    for fecha_str, asteroides in cercanias_por_fecha.items():
        for ast in asteroides:
            diametro = ast.get("estimated_diameter", {}).get("kilometers", {})
            filas.append({
                "nombre": ast.get("name", "Desconocido"),
                "diametro_min_km": diametro.get("estimated_diameter_min"),
                "diametro_max_km": diametro.get("estimated_diameter_max"),
                "peligroso": ast.get("is_potentially_hazardous_asteroid", False),
                "fecha_acercamiento": fecha_str,
                "velocidad_km_h": None,
                "distancia_km": None
            })
            acercamientos = ast.get("close_approach_data", [])
            if acercamientos:
                filas[-1]["velocidad_km_h"] = acercamientos[0].get("relative_velocity", {}).get("kilometers_per_hour")
                filas[-1]["distancia_km"] = acercamientos[0].get("miss_distance", {}).get("kilometers")

    df = pd.DataFrame(filas)
    print(f"DataFrame creado con {len(df)} fila(s) y {len(df.columns)} columna(s)")
    print(df.head().to_string(index=False))
    return df


def cargar_a_sqlite(df):
    """Paso 3 - Cargar: Guardar datos en SQLite evitando duplicados."""
    print("\n" + "=" * 70)
    print("PASO 3: Cargar datos a SQLite con SQLAlchemy")
    print("=" * 70)

    if df.empty:
        print("No hay datos para cargar.")
        return

    Base.metadata.create_all(engine)
    session = Session()

    try:
        insertados = 0
        duplicados_omitidos = 0

        for _, fila in df.iterrows():
            # Verificar si ya existe (por nombre + fecha) para evitar duplicados
            existe = session.query(AsteroideNASA).filter(
                AsteroideNASA.nombre == fila["nombre"],
                AsteroideNASA.fecha_acercamiento == fila["fecha_acercamiento"]
            ).first()

            if existe:
                duplicados_omitidos += 1
                continue

            nuevo = AsteroideNASA(
                nombre=fila["nombre"],
                diametro_min_km=fila["diametro_min_km"],
                diametro_max_km=fila["diametro_max_km"],
                peligroso=bool(fila["peligroso"]),
                fecha_acercamiento=datetime.strptime(fila["fecha_acercamiento"], "%Y-%m-%d").date(),
                velocidad_km_h=fila["velocidad_km_h"],
                distancia_km=fila["distancia_km"]
            )
            session.add(nuevo)
            insertados += 1

        session.commit()
        print(f"Insertados: {insertados} registro(s)")
        print(f"Duplicados omitidos: {duplicados_omitidos} registro(s)")

    except Exception as e:
        session.rollback()
        print(f"Error al cargar a SQLite: {e}")
    finally:
        session.close()


def consultar_datos_guardados():
    """Bonus: Consultar los datos guardados en SQLite."""
    print("\n" + "=" * 70)
    print("BONUS: Consultar datos guardados en SQLite")
    print("=" * 70)

    session = Session()
    try:
        todos = session.query(AsteroideNASA).all()
        print(f"Total en BD: {len(todos)} registro(s)")
        for a in todos[:5]:
            print(f"  {a.nombre} | {a.fecha_acercamiento} | Peligroso: {a.peligroso} | Ø {a.diametro_max_km} km")

        peligrosos = session.query(AsteroideNASA).filter(AsteroideNASA.peligroso == True).all()
        print(f"\nPotencialmente peligrosos: {len(peligrosos)}")

    except Exception as e:
        print(f"Error al consultar: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    # Definir rango de fechas (ultimos 7 dias)
    hoy = date.today()
    hace_siete_dias = hoy - timedelta(days=7)

    print(f"Consultando datos del {hace_siete_dias} al {hoy}...")

    # Paso 1: Extraer de la API
    datos_json = consultar_nasa_neos(str(hace_siete_dias), str(hoy))

    # Paso 2: Transformar con pandas
    df = transformar_datos(datos_json)

    # Paso 3: Cargar a SQLite
    cargar_a_sqlite(df)

    # Bonus: Consultar lo guardado
    consultar_datos_guardados()

    print("\nFlujo ETL completo finalizado.")