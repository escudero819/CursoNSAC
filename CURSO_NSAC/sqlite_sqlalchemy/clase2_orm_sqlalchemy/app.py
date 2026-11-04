"""
Clase 2 - SQLAlchemy ORM (Modelos y consultas orientadas a objetos)

Objetivo:
- Entender la diferencia entre SQL puro y ORM.
- Definir modelos de base de datos como clases de Python.
- Crear sesión y engine con SQLAlchemy.
- Insertar, consultar, filtrar y actualizar usando el ORM.
- Relacionar tablas (ForeignKey y relationship).

Requisitos:
- pip install sqlalchemy
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import date


# --- Configuración del engine y sesión ---
RUTA_BD = "sqlite:///recursos/datos_orm.db"
engine = create_engine(RUTA_BD, echo=False)  # echo=True muestra el SQL generado
Session = sessionmaker(bind=engine)
Base = declarative_base()


# --- Definición de modelos (tablas como clases Python) ---

class Asteroide(Base):
    """
    Modelo que representa la tabla 'asteroides'.
    Cada instancia de esta clase es una fila de la tabla.
    """
    __tablename__ = "asteroides"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    diametro_km = Column(Float, nullable=False)
    peligroso = Column(Boolean, default=False)
    fecha_acercamiento = Column(Date, nullable=False)

    # Relación: un asteroide puede tener varios acercamientos
    acercamientos = relationship("Acercamiento", back_populates="asteroide")

    def __repr__(self):
        return f"<Asteroide(nombre={self.nombre}, peligroso={self.peligroso})>"


class Acercamiento(Base):
    """
    Modelo que representa la tabla 'acercamientos'.
    Tiene una clave foránea hacia asteroides.
    """
    __tablename__ = "acercamientos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    asteroide_id = Column(Integer, ForeignKey("asteroides.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    distancia_km = Column(Float, nullable=False)
    velocidad_km_s = Column(Float, nullable=False)

    # Relación inversa
    asteroide = relationship("Asteroide", back_populates="acercamientos")

    def __repr__(self):
        return f"<Acercamiento(fecha={self.fecha}, distancia={self.distancia_km} km)>"


def crear_tablas():
    """
    Crea todas las tablas definidas en los modelos.
    """
    print("=" * 70)
    print("EJEMPLO 1: Crear tablas con SQLAlchemy ORM")
    print("=" * 70)

    Base.metadata.create_all(engine)
    print("Tablas creadas: asteroides, acercamientos")


def insertar_con_orm():
    """
    Ejemplo 2: Insertar registros usando objetos Python (ORM).
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 2: Insertar con ORM (session.add / add_all)")
    print("=" * 70)

    session = Session()
    try:
        # Creamos objetos Python
        ast1 = Asteroide(
            nombre="(2026 AB1)",
            diametro_km=0.15,
            peligroso=False,
            fecha_acercamiento=date(2026, 11, 1)
        )
        ast2 = Asteroide(
            nombre="(2026 CD2)",
            diametro_km=0.42,
            peligroso=True,
            fecha_acercamiento=date(2026, 11, 1)
        )

        # Creamos un acercamiento relacionado
        acerc1 = Acercamiento(
            fecha=date(2026, 11, 1),
            distancia_km=15000000,
            velocidad_km_s=28.4,
            asteroide=ast1  # Asignamos la relación directamente
        )

        # Agregamos a la sesion y confirmamos
        session.add_all([ast1, ast2, acerc1])
        session.commit()

        print(f"Insertados: {ast1}, {ast2}, {acerc1}")
        print(f"ID asignado automaticamente a ast1: {ast1.id}")

    except Exception as e:
        session.rollback()
        print(f"Error al insertar: {e}")
    finally:
        session.close()


def consultar_con_orm():
    """
    Ejemplo 3: Consultar con filtros usando el ORM.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 3: Consultar con ORM (query / filter / all)")
    print("=" * 70)

    session = Session()
    try:
        # Consultar todos los asteroides
        todos = session.query(Asteroide).all()
        print(f"\n--- Todos los asteroides ({len(todos)}) ---")
        for a in todos:
            print(f"  {a}")

        # Filtrar solo peligrosos (equivalente a WHERE peligroso = 1)
        peligrosos = session.query(Asteroide).filter(Asteroide.peligroso == True).all()
        print(f"\n--- Asteroides peligrosos ({len(peligrosos)}) ---")
        for a in peligrosos:
            print(f"  {a.nombre} | Ø {a.diametro_km} km")

        # Filtrar por diametro mayor a 0.2
        grandes = session.query(Asteroide).filter(Asteroide.diametro_km > 0.2).all()
        print(f"\n--- Asteroides con diametro > 0.2 km ({len(grandes)}) ---")
        for a in grandes:
            print(f"  {a.nombre} | Ø {a.diametro_km} km")

        # Obtener solo uno por ID
        uno = session.query(Asteroide).filter(Asteroide.id == 1).first()
        if uno:
            print(f"\n--- Asteroide ID 1 ---\n  {uno}")

    except Exception as e:
        print(f"Error al consultar: {e}")
    finally:
        session.close()


def actualizar_y_eliminar_con_orm():
    """
    Ejemplo 4: Actualizar y eliminar registros con ORM.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 4: Actualizar y eliminar con ORM")
    print("=" * 70)

    session = Session()
    try:
        # Actualizar: obtenemos el objeto, modificamos y commit
        ast = session.query(Asteroide).filter(Asteroide.id == 1).first()
        if ast:
            ast.diametro_km = 0.18
            session.commit()
            print(f"Actualizado: {ast.nombre} -> Ø {ast.diametro_km} km")

        # Eliminar: session.delete() y commit
        ast_eliminar = session.query(Asteroide).filter(Asteroide.id == 999).first()
        if ast_eliminar:
            session.delete(ast_eliminar)
            session.commit()
            print(f"Eliminado: {ast_eliminar.nombre}")
        else:
            print("  No existe asteroide con ID 999 (nada que eliminar).")

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


def consultar_con_join():
    """
    Ejemplo 5: Consulta con JOIN entre asteroides y acercamientos.
    """
    print("\n" + "=" * 70)
    print("EJEMPLO 5: Consulta con JOIN (relationship)")
    print("=" * 70)

    session = Session()
    try:
        # Consultamos asteroides y accedemos a sus acercamientos relacionados
        asteroides = session.query(Asteroide).all()
        for a in asteroides:
            print(f"\nAsteroide: {a.nombre} (Peligroso: {a.peligroso})")
            for acerc in a.acercamientos:
                print(f"  - Acercamiento {acerc.fecha}: {acerc.distancia_km:,} km, {acerc.velocidad_km_s} km/s")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    crear_tablas()
    insertar_con_orm()
    consultar_con_orm()
    actualizar_y_eliminar_con_orm()
    consultar_con_join()