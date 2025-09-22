import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="desarrollo_web"
    )
    print("¡Conexión exitosa a desarrollo_web!")
    conn.close()
except mysql.connector.Error as err:
    print(f"Error al conectar: {err}")
