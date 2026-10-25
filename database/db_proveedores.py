# database/db_proveedores.py

from database.conexion import obtener_conexion
from models.proveedor import Proveedor

def obtener_todos_proveedores():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, telefono, direccion, mail FROM proveedores")
    resultados = cursor.fetchall()
    proveedores = [Proveedor(*fila) for fila in resultados]
    conexion.close()
    return proveedores

def buscar_proveedores(filtro):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = """
        SELECT id, nombre, telefono, direccion, mail
        FROM proveedores
        WHERE nombre LIKE %s OR CAST(id AS CHAR) LIKE %s
    """
    valores = (f"%{filtro}%", f"%{filtro}%")
    cursor.execute(consulta, valores)
    resultados = cursor.fetchall()
    proveedores = [Proveedor(*fila) for fila in resultados]
    conexion.close()
    return proveedores
