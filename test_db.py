from Conexion.conexion import get_connection


print("Iniciando prueba de conexión…")

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("Conexión exitosa! Tablas encontradas:")
    for table in tables:
        print(table[0])
except Exception as e:
    print("Error al conectar:", e)
finally:
    if conn:
        conn.close()
