# database/db_clientes.py

from database.conexion import obtener_conexion
from models.cliente import Cliente

def obtener_todos_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, apellido, telefono, dni, direccion, mail FROM clientes")
    resultados = cursor.fetchall()
    clientes = [Cliente(*fila) for fila in resultados]
    conexion.close()
    return clientes

def buscar_clientes(filtro):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = """
        SELECT id, nombre, apellido, telefono, dni, direccion, mail
        FROM clientes
        WHERE nombre LIKE %s OR apellido LIKE %s OR CAST(id AS CHAR) LIKE %s OR CAST(dni AS CHAR) LIKE %s
    """
    valores = (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%", f"%{filtro}%")
    cursor.execute(consulta, valores)
    resultados = cursor.fetchall()
    clientes = [Cliente(*fila) for fila in resultados]
    conexion.close()
    return clientes
