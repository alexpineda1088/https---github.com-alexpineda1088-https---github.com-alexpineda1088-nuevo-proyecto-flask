import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3307,  # tu puerto
            user='root',
            password='tu_contraseña',  # pon la correcta
            database='desarrollo_web'
        )
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
