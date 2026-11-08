# Ejercicios Prácticos - Clase 3: CRUD con SQLite y FastAPI

## Objetivo
Conectar FastAPI con una base de datos SQLite local mediante SQLAlchemy, implementar operaciones CRUD persistentes y manejar sesiones de base de datos por petición usando dependency injection.

## Qué hay que hacer

1. **Configurar la base de datos:** Crea un engine de SQLAlchemy para SQLite con `check_same_thread=False`, una fábrica de sesiones (`sessionmaker`) y una clase base declarativa. Define un modelo SQLAlchemy (por ejemplo, `TareaDB` o `EventoDB`) con al menos 5 columnas: id, nombre, descripción, estado (booleano o texto), fecha_creación.

2. **Crear las tablas:** Ejecuta `Base.metadata.create_all(bind=engine)` al iniciar la aplicación para crear la tabla en el archivo `.db`.

3. **Definir modelos Pydantic:** Crea tres modelos: uno base con los campos de entrada, uno para crear (hereda del base) y uno para respuesta que incluya el `id` y tenga `from_attributes = True`.

4. **Dependency injection de la sesión:** Escribe una función `get_db()` que cree una sesión, la `yield` y la cierre en un bloque `finally`. Úsala como dependencia (`Depends(get_db)`) en cada endpoint que acceda a la base de datos.

5. **Endpoint POST (Crear):** Crea un endpoint que reciba los datos de entrada, los guarde en la base de datos con `db.add()`, `db.commit()` y `db.refresh()`, y devuelva el objeto creado con su ID asignado.

6. **Endpoint GET listar (Read all):** Crea un endpoint que devuelva todos los registros de la tabla. Agrega un parámetro de consulta opcional para filtrar por estado (por ejemplo, solo tareas completadas o pendientes).

7. **Endpoint GET por ID (Read one):** Crea un endpoint que reciba un ID en la ruta, busque el registro en la base de datos y lo devuelva. Si no existe, lanza `HTTPException` 404.

8. **Endpoint PUT (Update):** Crea un endpoint que reciba un ID y los datos actualizados, busque el registro, modifique sus campos, confirme con `commit()` y devuelva el objeto actualizado. Si no existe, lanza `HTTPException` 404.

9. **Endpoint DELETE:** Crea un endpoint que reciba un ID, busque el registro, lo elimine con `db.delete()`, confirme con `commit()` y devuelva un mensaje de confirmación. Si no existe, lanza `HTTPException` 404.

10. **Probar en /docs:** Levanta el servidor y prueba cada endpoint desde la documentación interactiva de FastAPI (`/docs`). Verifica que los datos se persistan en el archivo `.db` incluso después de reiniciar el servidor.

## Resultado esperado

- Un archivo `.db` de SQLite creado con la tabla definida.
- Cinco endpoints CRUD funcionando: crear, listar (con filtro opcional), obtener por ID, actualizar y eliminar.
- Cada endpoint que accede a la base de datos usa `Depends(get_db)` para gestionar la sesión.
- Los datos se guardan y persisten en el archivo `.db` entre reinicios del servidor.
- Los registros no encontrados devuelven error 404.
- La documentación `/docs` permite probar cada endpoint con ejemplos reales.

## Pistas

- `connect_args={"check_same_thread": False}` es necesario para que SQLite funcione con FastAPI en hilos múltiples.
- `db.refresh(obj)` después de `commit()` carga el ID autogenerado en el objeto.
- `from_attributes = True` en el Config de Pydantic permite leer datos directamente de objetos SQLAlchemy.
- `query.filter(Modelo.campo == valor).first()` devuelve `None` si no se encuentra nada.

## Dificultad

Intermedio

---