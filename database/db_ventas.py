# database/db_ventas.py

from database.conexion import obtener_conexion

def guardar_venta(venta):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    # Insertar la venta
    consulta = """
        INSERT INTO ventas (fecha, cliente, detalle, total_bruto, descuento_aplicado, total_final)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        venta.fecha,
        venta.cliente,
        venta.generar_detalle(),
        venta.total_bruto,
        venta.descuento_aplicado,
        venta.total_final
    )
    cursor.execute(consulta, valores)
    conexion.commit()
    cursor.close()
    conexion.close()
