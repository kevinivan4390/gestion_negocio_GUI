# models/proveedor.py

from database.conexion import obtener_conexion

class Proveedor:
    def __init__(self, id, nombre, telefono, direccion, mail):
        self.id = id
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.mail = mail

    def guardar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        if self.id is None:
            consulta = """
                INSERT INTO proveedores (nombre, telefono, direccion, mail)
                VALUES (%s, %s, %s, %s)
            """
            valores = (self.nombre, self.telefono, self.direccion, self.mail)
            cursor.execute(consulta, valores)
            self.id = cursor.lastrowid
        else:
            consulta = """
                UPDATE proveedores
                SET nombre=%s, telefono=%s, direccion=%s, mail=%s
                WHERE id=%s
            """
            valores = (self.nombre, self.telefono, self.direccion, self.mail, self.id)
            cursor.execute(consulta, valores)

        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self):
        if self.id is not None:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM proveedores WHERE id = %s", (self.id,))
            conexion.commit()
            cursor.close()
            conexion.close()
