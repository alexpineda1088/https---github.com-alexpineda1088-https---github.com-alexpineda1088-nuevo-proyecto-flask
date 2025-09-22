import sqlite3

# Conexión a la base de datos (se crea si no existe)
conn = sqlite3.connect('ventas.db')
cursor = conn.cursor()

# Crear tabla de ventas
cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    total REAL NOT NULL,
    fecha TEXT NOT NULL
)
""")

# Insertar datos de ejemplo
ventas = [
    ('Arroz 1kg', 3, 6.00, '2025-09-01'),
    ('Leche 1L', 2, 3.40, '2025-09-02'),
    ('Pan', 5, 5.00, '2025-09-03'),
    ('Huevos', 1, 2.50, '2025-09-04')
]

cursor.executemany("INSERT INTO ventas (producto, cantidad, total, fecha) VALUES (?, ?, ?, ?)", ventas)

# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("✅ Base de datos creada con éxito.")