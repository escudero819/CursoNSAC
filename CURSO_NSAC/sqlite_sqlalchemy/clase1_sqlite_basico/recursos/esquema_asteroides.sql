-- Esquema de la tabla asteroides (SQLite)
CREATE TABLE IF NOT EXISTS asteroides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    diametro_km REAL NOT NULL,
    peligroso INTEGER DEFAULT 0,
    fecha_acercamiento TEXT NOT NULL,
    fecha_registro TEXT DEFAULT (date('now'))
);

-- Ejemplo de consulta de asteroides peligrosos
SELECT nombre, diametro_km, fecha_acercamiento
FROM asteroides
WHERE peligroso = 1
ORDER BY diametro_km DESC;

-- Ejemplo de conteo por fecha
SELECT fecha_acercamiento, COUNT(*) as total
FROM asteroides
GROUP BY fecha_acercamiento;