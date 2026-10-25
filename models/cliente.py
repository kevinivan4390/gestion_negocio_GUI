# models/cliente.py

from database.conexion import obtener_conexion

class Cliente:
    def __init__(self, id, nombre, apellido, telefono, dni, direccion, mail):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.dni = dni
        self.direccion = direccion
        self.mail = mail

    def guardar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        if self.id is None:
            consulta = """
                INSERT INTO clientes (nombre, apellido, telefono, dni, direccion, mail)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (self.nombre, self.apellido, self.telefono, self.dni, self.direccion, self.mail)
            cursor.execute(consulta, valores)
            self.id = cursor.lastrowid
        else:
            consulta = """
                UPDATE clientes
                SET nombre=%s, apellido=%s, telefono=%s, dni=%s, direccion=%s, mail=%s
                WHERE id=%s
            """
            valores = (self.nombre, self.apellido, self.telefono, self.dni, self.direccion, self.mail, self.id)
            cursor.execute(consulta, valores)

        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self):
        if self.id is not None:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = %s", (self.id,))
            conexion.commit()
            cursor.close()
            conexion.close()
