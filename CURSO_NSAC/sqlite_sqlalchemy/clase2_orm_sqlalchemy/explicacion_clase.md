# Clase 2 - SQLAlchemy ORM

## 1. Explicación del ejemplo

En la clase anterior usamos SQL puro con `sqlite3`. En esta clase usamos **SQLAlchemy ORM** (Object Relational Mapper), que te permite trabajar con la base de datos usando **clases y objetos de Python** en lugar de escribir sentencias SQL a mano.

El archivo contiene cinco ejemplos:

1. **Crear tablas:** `Base.metadata.create_all()` crea las tablas desde los modelos.
2. **Insertar con ORM:** Creas objetos Python (`Asteroide(...)`, `Acercamiento(...)`) y los guardas con `session.add()` / `session.add_all()`.
3. **Consultar con filtros:** `session.query(Modelo).filter(...).all()` equivale a un `SELECT ... WHERE`.
4. **Actualizar y eliminar:** Modificas atributos del objeto o usas `session.delete()`, luego `session.commit()`.
5. **JOIN con relaciones:** Accedes a datos relacionados mediante `relationship()` (ej. `asteroide.acercamientos`).

---

## 2. Explicación de la clase / conceptos clave

### Engine, Session y Base

| Componente | Propósito |
|------------|-----------|
| `create_engine(...)` | Conexión a la base de datos |
| `declarative_base()` | Clase base para definir modelos |
| `sessionmaker(bind=engine)` | Fábrica de sesiones para transacciones |
| `Session()` | Una sesión de trabajo (como una transacción) |

### Definir un modelo

```python
from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Asteroide(Base):
    __tablename__ = "asteroides"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    diametro_km = Column(Float, nullable=False)
    peligroso = Column(Boolean, default=False)
    fecha_acercamiento = Column(Date, nullable=False)
```

### Tipos de columna comunes

| Tipo SQLAlchemy | Equivalente Python | Uso |
|-----------------|--------------------|-----|
| `Integer` | `int` | IDs, conteos |
| `String(n)` | `str` | Nombres, texto corto |
| `Text` | `str` | Texto largo |
| `Float` | `float` | Decimales (diámetro, distancia) |
| `Boolean` | `bool` | Sí/No (peligroso) |
| `Date` | `datetime.date` | Fechas |
| `DateTime` | `datetime.datetime` | Fecha y hora |

### Consultas ORM vs SQL puro

| SQL puro | SQLAlchemy ORM |
|----------|----------------|
| `SELECT * FROM asteroides` | `session.query(Asteroide).all()` |
| `SELECT * FROM asteroides WHERE peligroso = 1` | `session.query(Asteroide).filter(Asteroide.peligroso == True).all()` |
| `SELECT * FROM asteroides WHERE diametro > 0.2` | `session.query(Asteroide).filter(Asteroide.diametro_km > 0.2).all()` |
| `SELECT * FROM asteroides WHERE id = 1` | `session.query(Asteroide).filter(Asteroide.id == 1).first()` |

### Relaciones entre tablas

```python
# En Asteroide:
acercamientos = relationship("Acercamiento", back_populates="asteroide")

# En Acercamiento:
asteroide_id = Column(Integer, ForeignKey("asteroides.id"))
asteroide = relationship("Asteroide", back_populates="acercamientos")
```

Esto te permite hacer `asteroide.acercamientos` y obtener automáticamente todos los acercamientos relacionados, sin escribir un `JOIN` manual.

---

## 3. Diccionario de sintaxis global - SQLAlchemy ORM

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///datos.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Definir modelo
class MiTabla(Base):
    __tablename__ = "mi_tabla"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

# Crear tablas
Base.metadata.create_all(engine)

# Insertar
session = Session()
obj = MiTabla(nombre="Ejemplo")
session.add(obj)
session.commit()

# Consultar
todos = session.query(MiTabla).all()
filtrados = session.query(MiTabla).filter(MiTabla.nombre == "Ejemplo").all()
uno = session.query(MiTabla).filter(MiTabla.id == 1).first()

# Actualizar
uno.nombre = "Nuevo nombre"
session.commit()

# Eliminar
session.delete(uno)
session.commit()

session.close()
```

---

## 4. Flujo de trabajo lógico

1. **Definir modelos:** Clases que representan tus tablas.
2. **Crear tablas:** `Base.metadata.create_all(engine)`.
3. **Abrir sesión:** `session = Session()`.
4. **Operar:** Insertar, consultar, filtrar, actualizar, eliminar con objetos Python.
5. **Confirmar:** `session.commit()` para guardar cambios.
6. **Deshacer si falla:** `session.rollback()` en caso de error.
7. **Cerrar:** `session.close()`.

> **Tip de la hackathon:** Si algo falla en medio de una transacción, llama a `session.rollback()` para dejar la base de datos en un estado consistente.

---

## 5. Posibles errores y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `OperationalError: no such table` | Intentaste consultar una tabla que no existe | Ejecutar `Base.metadata.create_all(engine)` primero |
| `IntegrityError` | Violaste una restricción (NOT NULL, UNIQUE, FK) | Revisar que todos los campos obligatorios tengan valor |
| `InvalidRequestError` | Sesión cerrada o objeto detached | Abrir una nueva sesión o hacer `session.expire_all()` |
| Cambios no guardados | Olvidaste `session.commit()` | Siempre hacer `commit()` tras INSERT/UPDATE/DELETE |

---

## 6. Adaptación a la competencia NSAC

SQLAlchemy ORM es ideal para la hackathon porque:

- Escribes menos código (no escribes SQL a mano).
- El código es más legible y fácil de mantener.
- Puedes cambiar de SQLite a PostgreSQL más tarde solo cambiando el `create_engine`.

Siguiente paso sugerido: `clase3_integracion_api_bd` para aprender a combinar la API de la NASA + pandas + SQLAlchemy en un flujo completo.