# Conexion/conexion.py
import mysql.connector

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Cambia si tienes contraseña
            database='desarrollo_web'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None