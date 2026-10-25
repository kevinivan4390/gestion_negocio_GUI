# models/historial_ventas.py

from database.conexion import obtener_conexion
from datetime import datetime

class HistorialVentasModel:
    @staticmethod
    def listar_todas():
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id, fecha, cliente, total_final FROM ventas ORDER BY fecha DESC")
        ventas = cursor.fetchall()
        conexion.close()
        return ventas

    @staticmethod
    def listar_por_fecha(fecha_inicio, fecha_fin):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        query = """
            SELECT id, fecha, cliente, total_final 
            FROM ventas
            WHERE fecha BETWEEN %s AND %s
            ORDER BY fecha DESC
        """
        cursor.execute(query, (fecha_inicio, fecha_fin))
        ventas = cursor.fetchall()
        conexion.close()
        return ventas

    @staticmethod
    def listar_por_cliente(nombre_cliente):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        query = """
            SELECT id, fecha, cliente, total_final
            FROM ventas
            WHERE cliente LIKE %s
            ORDER BY fecha DESC
        """
        cursor.execute(query, (f"%{nombre_cliente}%",))
        ventas = cursor.fetchall()
        conexion.close()
        return ventas

    @staticmethod
    def obtener_detalle_venta(id_venta):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        query = "SELECT detalle FROM ventas WHERE id = %s"
        cursor.execute(query, (id_venta,))
        detalle = cursor.fetchone()
        conexion.close()
        return detalle['detalle'] if detalle else "No disponible"

    @staticmethod
    def listar_por_fecha_y_cliente(fecha_inicio, fecha_fin, nombre_cliente):
        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)
        query = """
            SELECT id, fecha, cliente, total_final
            FROM ventas
            WHERE fecha BETWEEN %s AND %s
              AND cliente LIKE %s
            ORDER BY fecha DESC
        """
        cursor.execute(query, (fecha_inicio, fecha_fin, f"%{nombre_cliente}%"))
        ventas = cursor.fetchall()
        conexion.close()
        return ventas
