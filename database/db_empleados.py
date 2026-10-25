# database/db_empleados.py

from database.conexion import obtener_conexion
from models.empleado import Empleado

def obtener_todos_empleados():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, apellido, dni, edad, cargo, salario FROM empleados")
    resultados = cursor.fetchall()
    empleados = [Empleado(*fila) for fila in resultados]
    conexion.close()
    return empleados

def buscar_empleados(filtro):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = """
        SELECT id, nombre, apellido, dni, edad, cargo, salario
        FROM empleados
        WHERE nombre LIKE %s OR apellido LIKE %s OR CAST(id AS CHAR) LIKE %s OR CAST(dni AS CHAR) LIKE %s
    """
    valores = (f"%{filtro}%", f"%{filtro}%", f"%{filtro}%", f"%{filtro}%")
    cursor.execute(consulta, valores)
    resultados = cursor.fetchall()
    empleados = [Empleado(*fila) for fila in resultados]
    conexion.close()
    return empleados
