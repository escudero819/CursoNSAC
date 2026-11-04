# Diccionario de sintaxis rápida - `SQLAlchemy` + `sqlite3`

## Instalación
```bash
pip install sqlalchemy
```

## SQLite puro (`sqlite3` - incluido en Python)

```python
import sqlite3

# Conectar (crea el archivo si no existe)
conexion = sqlite3.connect("datos.db")
cursor = conexion.cursor()

# Crear tabla
cursor.execute("CREATE TABLE IF NOT EXISTS asteroides (id INTEGER PRIMARY KEY, nombre TEXT, diametro REAL)")

# Insertar con parámetros seguros (?)
cursor.execute("INSERT INTO asteroides (nombre, diametro) VALUES (?, ?)", ("Marte", 0.15))
conexion.commit()

# Insertar varios
cursor.executemany("INSERT INTO asteroides VALUES (?, ?, ?)", lista_datos)
conexion.commit()

# Consultar
cursor.execute("SELECT * FROM asteroides WHERE peligrosos = 1")
filas = cursor.fetchall()   # Todas
fila = cursor.fetchone()    # Solo la primera

# Cerrar
conexion.close()
```

## SQLAlchemy ORM

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# Engine y sesión
engine = create_engine("sqlite:///datos.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Definir modelo
class Asteroide(Base):
    __tablename__ = "asteroides"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    diametro_km = Column(Float, nullable=False)
    peligroso = Column(Boolean, default=False)

# Crear tablas
Base.metadata.create_all(engine)

# Insertar
session = Session()
obj = Asteroide(nombre="Marte", diametro_km=0.15, peligroso=False)
session.add(obj)
session.commit()

# Consultar
todos = session.query(Asteroide).all()
filtrados = session.query(Asteroide).filter(Asteroide.peligroso == True).all()
uno = session.query(Asteroide).filter(Asteroide.id == 1).first()

# Actualizar
uno.diametro_km = 0.18
session.commit()

# Eliminar
session.delete(uno)
session.commit()
session.close()
```

## Tipos de columna comunes

| Tipo SQLAlchemy | Uso |
|-----------------|-----|
| `Integer` | IDs, conteos |
| `String(n)` | Nombres, texto corto |
| `Text` | Texto largo |
| `Float` | Decimales |
| `Boolean` | Sí/No |
| `Date` | Fecha |
| `DateTime` | Fecha y hora |

## Relaciones entre tablas

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Asteroide(Base):
    __tablename__ = "asteroides"
    id = Column(Integer, primary_key=True)
    acercamientos = relationship("Acercamiento", back_populates="asteroide")

class Acercamiento(Base):
    __tablename__ = "acercamientos"
    id = Column(Integer, primary_key=True)
    asteroide_id = Column(Integer, ForeignKey("asteroides.id"))
    asteroide = relationship("Asteroide", back_populates="acercamientos")
```

## Manejo de transacciones

```python
try:
    session.add(obj)
    session.commit()
except Exception as e:
    session.rollback()  # Deshace cambios si algo falla
    raise e
finally:
    session.close()
```

---

> **Tip:** Siempre haz `session.commit()` después de INSERT/UPDATE/DELETE, o los cambios se perderán al cerrar.