import sqlite3

# Conectarse a la base de datos (se creará si no existe)
conn = sqlite3.connect('ventas.db')
cursor = conn.cursor()

# Crear tabla productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL
)
""")

# Crear tabla ventas
cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    total REAL NOT NULL,
    fecha TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("Tablas 'productos' y 'ventas' creadas correctamente.")
