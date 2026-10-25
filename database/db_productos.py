# database/db_productos.py

from database.conexion import obtener_conexion
from models.producto import Producto
from database.conexion import obtener_conexion

def obtener_todos_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, variedad, nombre, marca, tamanio, sabor, preciocompra, precioventa, stock, vencimiento FROM productos")
    resultados = cursor.fetchall()
    conexion.close()

    productos = [Producto(*fila) for fila in resultados]
    return productos

def buscar_productos(filtro):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    query = """
        SELECT id, variedad, nombre, marca, tamanio, sabor, preciocompra, precioventa, stock, vencimiento
        FROM productos
        WHERE nombre LIKE %s OR marca LIKE %s OR variedad LIKE %s
    """
    like_filtro = f"%{filtro}%"
    cursor.execute(query, (like_filtro, like_filtro, like_filtro))
    resultados = cursor.fetchall()
    conexion.close()

    productos = [Producto(*fila) for fila in resultados]
    return productos


def actualizar_stock(id_producto, nuevo_stock):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    consulta = "UPDATE productos SET stock = %s WHERE id = %s"
    valores = (nuevo_stock, id_producto)
    cursor.execute(consulta, valores)
    conexion.commit()
    cursor.close()
    conexion.close()

