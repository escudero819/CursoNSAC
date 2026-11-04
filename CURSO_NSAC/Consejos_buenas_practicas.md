# Consejos y buenas prácticas para la Hackathon NSAC

Este archivo resume los consejos clave, errores comunes y estrategias para rendir al máximo durante la competencia usando las herramientas de este curso.

---

## 1. Antes de la hackathon (preparación)

| Consejo | Por qué |
|---------|---------|
| Instala todas las librerías antes | `pip install requests pandas sqlalchemy fastapi uvicorn` | No pierdas tiempo descargando durante la competencia |
| Consigue tu API key de la NASA | https://api.nasa.gov | La `DEMO_KEY` tiene límites muy bajos |
| Prueba tu conexión a internet | La NASA API puede estar lenta o caída | Ten un plan B con datos locales |
| Crea una plantilla de proyecto | Copia esta carpeta `CURSO_NSAC` como base | No empieces desde cero |
| Revisa el Diccionario de sintaxis | Ten a mano los comandos más usados | Ahorra tiempo buscando en Google |

---

## 2. Durante la hackathon (flujo de trabajo recomendado)

```
Paso 1: Definir el problema y los datos que necesitas
Paso 2: Consultar la API de la NASA con requests (+ timeout)
Paso 3: Validar la respuesta (status_code == 200)
Paso 4: Transformar con pandas (json_normalize, filtrar, agrupar)
Paso 5: Guardar en SQLite con SQLAlchemy (evita llamar otra vez a la API)
Paso 6: Exponer endpoints con FastAPI para el equipo
Paso 7: Documentar en /docs para que todos sepan usar tu API
```

---

## 3. Buenas prácticas de código

### requests
- ✅ Siempre usa `timeout=10` (o similar) en cada petición.
- ✅ Usa `try/except` para capturar errores de red.
- ✅ Usa `response.raise_for_status()` para detectar errores HTTP.
- ✅ Usa `requests.Session()` si haces muchas peticiones al mismo servidor.
- ✅ Guarda tu API key en una variable de entorno, no en el código.
- ❌ Nunca concatenes URLs con datos de usuario sin validar.

### pandas
- ✅ Usa `pd.json_normalize()` para JSON anidados de la NASA.
- ✅ Usa `.copy()` al crear subconjuntos (`df[condicion].copy()`).
- ✅ Revisa valores nulos con `df.isnull().sum()` antes de operar.
- ✅ Guarda resultados intermedios en CSV o SQLite para no reprocesar.
- ❌ No intentes hacer todo en una sola línea; separa en pasos claros.

### SQLite / SQLAlchemy
- ✅ Siempre usa parámetros seguros `?` (sqlite3) o modelos ORM (SQLAlchemy).
- ✅ Llama a `conexion.commit()` o `session.commit()` tras INSERT/UPDATE/DELETE.
- ✅ Usa `CREATE TABLE IF NOT EXISTS` para no fallar si la tabla ya existe.
- ✅ Verifica duplicados antes de insertar (`if not session.query(...).first():`).
- ❌ No escribas SQL concatenando strings (riesgo de inyección SQL).

### FastAPI
- ✅ Usa Pydantic (`BaseModel`) para validar entrada y salida.
- ✅ Usa `response_model` para documentar las respuestas automáticamente.
- ✅ Usa `Depends(get_db)` para manejar sesiones de base de datos por petición.
- ✅ Usa `HTTPException` para devolver errores claros (404, 422, 503).
- ✅ Prueba tus endpoints en `http://127.0.0.1:8000/docs`.
- ❌ No olvides `check_same_thread=False` en el engine de SQLite con FastAPI.

---

## 4. Posibles errores en la competencia y cómo adaptarse

| Situación | Qué hacer |
|-----------|-----------|
| La API de la NASA no responde | Usa `try/except` y datos guardados en SQLite local |
| Límite de peticiones (429) | Espera, usa tu propia API key, o consulta desde SQLite local |
| JSON anidado muy complejo | Usa `pd.json_normalize()` con `sep="_"` |
| Datos con valores nulos | `df.fillna(0)` o `df.dropna()` según corresponda |
| Puerto 8000 ocupado | Cambia puerto: `uvicorn app:app --port 8001` |
| No se guardan cambios en BD | Olvidaste `session.commit()` o `conexion.commit()` |
| Error de validación 422 | Revisa que el JSON enviado coincida con tu modelo Pydantic |
| Necesitas compartir datos con el equipo | Comparte el archivo `.db` de SQLite o levanta tu FastAPI |

---

## 5. Razonamiento lógico de un licenciado en Ciencias de Datos

Frente a un problema nuevo durante la hackathon, sigue este orden mental:

1. **¿Qué datos necesito?** Definir las variables clave (fecha, ubicación, tipo de evento, etc.).
2. **¿De dónde vienen?** API de la NASA, CSV local, entrada del usuario.
3. **¿Cómo los consigo?** `requests.get()` con validación y timeout.
4. **¿Cómo los limpio?** `pandas`: quitar nulos, normalizar JSON, filtrar.
5. **¿Dónde los guardo?** SQLite para persistencia y reuso.
6. **¿Cómo los entrego al equipo?** FastAPI con endpoints documentados.
7. **¿Qué puede salir mal?** Anticipar errores de red, límites de API, datos faltantes.

---

## 6. Checklist rápido antes de presentar

- [ ] Todas las librerías instaladas (`requests`, `pandas`, `sqlalchemy`, `fastapi`, `uvicorn`)
- [ ] API key de la NASA configurada
- [ ] Endpoints probados en `/docs`
- [ ] Datos guardados en SQLite local (no depender solo de internet)
- [ ] Manejo de errores implementado (`try/except`, `HTTPException`)
- [ ] README o documentación breve para el equipo
- [ ] Código limpio y con comentarios breves

---

> **Recuerda:** En una hackathon, lo importante es que funcione y se pueda demostrar. Un código simple que funciona vale más que un código complejo que no termina. Usa este curso como referencia rápida y ¡mucho éxito en la NSAC!