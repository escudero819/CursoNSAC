# Comparación SQL puro vs SQLAlchemy ORM

| Tarea | SQL puro (sqlite3) | SQLAlchemy ORM |
|-------|-------------------|----------------|
| Crear tabla | `CREATE TABLE ...` | `class Modelo(Base): ...` + `create_all()` |
| Insertar | `INSERT INTO ... VALUES (?, ?)` | `session.add(Objeto(...))` + `commit()` |
| Consultar | `SELECT * FROM tabla WHERE ...` | `session.query(Modelo).filter(...).all()` |
| Actualizar | `UPDATE tabla SET ... WHERE ...` | `obj.atributo = valor` + `commit()` |
| Eliminar | `DELETE FROM tabla WHERE ...` | `session.delete(obj)` + `commit()` |
| Relaciones | `JOIN` manual | `relationship()` + `obj.relacionado` |

**Recomendación NSAC:** Usa SQLAlchemy ORM si prefieres trabajar con objetos Python. Usa SQL puro si necesitas consultas muy complejas o rendimiento extremo.