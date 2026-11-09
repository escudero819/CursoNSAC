from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine("sqlite:///recursos/database.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Planeta(Base):
    __tablename__ = "planetas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    diametro_km = Column(Float, nullable=False)
    distancia_sol_km = Column(Float, nullable=False)
    es_habitable = Column(Boolean, nullable=False)

    lunas = relationship("Luna", back_populates="planeta")

    def __repr__(self):
        return f"Planeta(nombre={self.nombre}, tipo={self.tipo}, es_habitable={self.es_habitable})"

class Luna(Base):
    __tablename__ = "lunas"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    planeta_id = Column(Integer, ForeignKey("planetas.id"))
    diametro_km = Column(Float, nullable=False)
    distancia_planeta_km = Column(Float, nullable=False)

    planeta = relationship("Planeta", back_populates="lunas")

    def __repr__(self):
        return f"Luna (nombre={self.nombre}, diametro_km={self.diametro_km}, distancia_planeta={self.distancia_planeta_km})"

def Crear_BD():
    # creamos las tablas en la BD
    Base.metadata.create_all(engine)

    datos_planetas = [
        Planeta(nombre="Jupiter", tipo="gaseoso", diametro_km=10000000, distancia_sol_km=7000, es_habitable=False),
        Planeta(nombre="Tierra", tipo="rocoso", diametro_km=5000, distancia_sol_km=400000, es_habitable=True),
        Planeta(nombre="Venus", tipo="rocoso", diametro_km=2500, distancia_sol_km=200000, es_habitable=False)
    ]

    datos_lunas = [
        Luna(nombre="Luna", planeta_id=2, diametro_km=250, distancia_planeta_km=10000),
        Luna(nombre="RX-GHRD", planeta_id=1, diametro_km=40, distancia_planeta_km=23498.4),
        Luna(nombre="MAJS-GG", planeta_id=2, diametro_km=50, distancia_planeta_km=9834),
        Luna(nombre="LEO-MEs", planeta_id=3, diametro_km=20, distancia_planeta_km=8282),
        Luna(nombre="KEI-hg", planeta_id=1, diametro_km=745, distancia_planeta_km=100),
        Luna(nombre="Luna-2", planeta_id=3, diametro_km=237, distancia_planeta_km=10),
        Luna(nombre="AJS-ehjg", planeta_id=1, diametro_km=9505, distancia_planeta_km=100),
    ]

    session = Session()
    try:
        session.add_all(datos_planetas)
        session.commit()
        session.add_all(datos_lunas)
        session.commit()
    except Exception as e:
        session.rollback()
        print("Problema al cargar la BD")
        raise e

def Consultar_Planetas():
    session = Session()
    planetas = session.query(Planeta).all()
    print(planetas)

def Filtrar():
    session = Session()
    habitables = session.query(Planeta).filter(Planeta.es_habitable == True).all()
    if habitables:
        print("Se encontro/aron", len(habitables), "planeta/s habitables")
        print(habitables)
    else:
        print("ningun planeta es habitable")
    grandes = session.query(Planeta).filter(Planeta.diametro_km >= 5000).all()
    if grandes:
        print("Se encontro/aron", len(grandes), "planeta/s grandes")
        print(grandes)
    else:
        print("ningun planeta es habitable")

def Modificar_diametro(id, valor):
    session = Session()
    planeta = session.query(Planeta).filter(Planeta.id == id).first()
    if planeta:
        try:
            atr_ant = planeta.diametro_km
            planeta.diametro_km = valor
            session.commit()
            print(f"se logro cambiar el valor del diametro de {atr_ant} a {valor}")
        except Exception as e:
            session.rollback()
            print(e)
    else:
        print("no existe dicho ID")

def Eliminar(id):
    session = Session()

    uno = session.query(Planeta).filter(Planeta.id == id).first()
    if uno:
        session.delete(uno)
        session.commit()
        print(uno, " eliminado")
    else:
        print("no existe ese id de planeta")

def Relaciones():
    #en el muestreo recorrer planeta.lunas
    session = Session()

    planetas = session.query(Planeta).all()
    for planeta in planetas:
        lunas = planeta.lunas
        print(f"en {planeta.nombre} hay {len(lunas)} lunas")
        print(lunas)
    

if __name__ == "__main__":
    Crear_BD() # <- Ya la creamos o borra la existente para probar
    Consultar_Planetas()
    Filtrar()
    Modificar_diametro(1, 679950)
    Relaciones()