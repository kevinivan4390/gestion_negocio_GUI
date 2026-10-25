import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",                # Usuario de MySQL
        password="4390",        # Poné tu contraseña de MySQL (puede ser vacío si no tiene)
        database="negocio"          # Nombre de la base de datos
    )
