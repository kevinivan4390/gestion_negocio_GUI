# models/producto.py

from database.conexion import obtener_conexion

class Producto:
    def __init__(self, id=None, variedad="", nombre="", marca="", tamanio="", sabor="", preciocompra=0.0, precioventa=0.0, stock=0, vencimiento=None):
        self.id = id
        self.variedad = variedad
        self.nombre = nombre
        self.marca = marca
        self.tamanio = tamanio
        self.sabor = sabor
        self.preciocompra = preciocompra
        self.precioventa = precioventa
        self.stock = stock
        self.vencimiento = vencimiento

    def guardar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        if self.id is None:
            consulta = """
                INSERT INTO productos (variedad, nombre, marca, tamanio, sabor, preciocompra, precioventa, stock, vencimiento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (self.variedad, self.nombre, self.marca, self.tamanio, self.sabor, self.preciocompra, self.precioventa, self.stock, self.vencimiento)
            cursor.execute(consulta, valores)
            self.id = cursor.lastrowid
        else:
            consulta = """
                UPDATE productos
                SET variedad=%s, nombre=%s, marca=%s, tamanio=%s, sabor=%s,
                    preciocompra=%s, precioventa=%s, stock=%s, vencimiento=%s
                WHERE id=%s
            """
            valores = (self.variedad, self.nombre, self.marca, self.tamanio, self.sabor, self.preciocompra, self.precioventa, self.stock, self.vencimiento, self.id)
            cursor.execute(consulta, valores)
        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self):
        if self.id is not None:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM productos WHERE id=%s", (self.id,))
            conexion.commit()
            cursor.close()
            conexion.close()

    def calcular_margen(self):
        return self.precioventa - self.preciocompra

    def __str__(self):
        return f"{self.nombre} - {self.marca} - ${self.precioventa}"
