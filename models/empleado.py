# models/empleado.py

from database.conexion import obtener_conexion

class Empleado:
    def __init__(self, id, nombre, apellido, dni, edad, cargo, salario):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.edad = edad
        self.cargo = cargo
        self.salario = salario

    def guardar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        if self.id is None:
            consulta = """
                INSERT INTO empleados (nombre, apellido, dni, edad, cargo, salario)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            valores = (self.nombre, self.apellido, self.dni, self.edad, self.cargo, self.salario)
            cursor.execute(consulta, valores)
            self.id = cursor.lastrowid
        else:
            consulta = """
                UPDATE empleados
                SET nombre=%s, apellido=%s, dni=%s, edad=%s, cargo=%s, salario=%s
                WHERE id=%s
            """
            valores = (self.nombre, self.apellido, self.dni, self.edad, self.cargo, self.salario, self.id)
            cursor.execute(consulta, valores)

        conexion.commit()
        cursor.close()
        conexion.close()

    def eliminar(self):
        if self.id is not None:
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM empleados WHERE id = %s", (self.id,))
            conexion.commit()
            cursor.close()
            conexion.close()
