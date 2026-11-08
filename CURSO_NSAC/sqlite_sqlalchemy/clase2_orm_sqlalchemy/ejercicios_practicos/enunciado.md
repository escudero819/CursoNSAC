# Ejercicios Prácticos - Clase 2: SQLAlchemy ORM

## Objetivo
Trabajar con la base de datos usando clases y objetos de Python en lugar de escribir SQL a mano, definiendo modelos, creando sesiones, insertando, consultando con filtros, actualizando, eliminando y relacionando tablas.

## Qué hay que hacer

1. **Definir dos modelos relacionados:** Crea una clase `Planeta` (id, nombre, tipo, diametro_km, distancia_sol_km, es_habitable) y una clase `Luna` (id, nombre, planeta_id como clave foránea, diametro_km, distancia_planeta_km). Establece una relación `relationship()` entre ellos para que un planeta pueda tener varias lunas y cada luna sepa a qué planeta pertenece.

2. **Crear las tablas:** Usa `Base.metadata.create_all(engine)` para crear ambas tablas en la base de datos SQLite.

3. **Insertar planetas y lunas con objetos:** Crea al menos 3 instancias de `Planeta` y, para al menos uno de ellos, crea 2 o 3 instancias de `Luna` asociadas (asigna el planeta directamente en la relación o usa el `planeta_id`). Agrégalos a la sesión con `add_all()` y confirma con `commit()`.

4. **Consultar todos los planetas:** Recupera todos los planetas con `session.query(Planeta).all()` e imprímelos.

5. **Consultar con filtros:** Obtén solo los planetas marcados como habitables (`es_habitable == True`). También obtén los planetas con diámetro mayor a un valor que elijas. Imprime los resultados.

6. **Obtener un objeto por ID y actualizarlo:** Busca un planeta por su ID con `.first()`, modifica uno de sus atributos (por ejemplo, el diámetro), y guarda los cambios con `commit()`.

7. **Eliminar un registro:** Busca un planeta o luna por ID y elimínalo con `session.delete()`, luego confirma con `commit()`.

8. **Acceder a relaciones:** Para cada planeta consultado, imprime sus lunas relacionadas accediendo al atributo de relación (por ejemplo, `planeta.lunas`). Verifica que se recuperen automáticamente sin escribir un JOIN manual.

9. **Manejo de transacciones:** Envuelve al menos una operación de escritura (insertar, actualizar o eliminar) en un bloque `try/except` que llame a `session.rollback()` si algo falla, dejando la base de datos en un estado consistente.

## Resultado esperado

- Dos tablas creadas en SQLite: `planetas` y `lunas`.
- Al menos 3 planetas y 4 lunas insertadas usando objetos Python.
- Al menos una luna asociada correctamente a un planeta mediante la relación ORM.
- Salida en consola de todos los planetas y de los filtrados (habitables y por diámetro).
- Al menos un planeta actualizado y verificado tras el cambio.
- Al menos un registro eliminado y verificado.
- Al menos un ejemplo de acceso a datos relacionados (`planeta.lunas`) funcionando sin SQL manual.
- Un bloque `try/except` con `session.rollback()` demostrado o comentado en el código.

## Pistas

- La clave foránea se define con `ForeignKey("planetas.id")`.
- La relación se define con `relationship("Luna", back_populates="planeta")` en Planeta y `relationship("Planeta", back_populates="lunas")` en Luna.
- `session.query(Modelo).filter(Modelo.campo == valor).all()` es equivalente a `SELECT * FROM modelo WHERE campo = valor`.
- `session.refresh(obj)` recarga el objeto desde la base de datos después de un commit (útil para obtener IDs autogenerados).

## Dificultad

Intermedio

---