# models/caja.py

from database.conexion import obtener_conexion

class Caja:
    def __init__(self, total):
        self.total = total

    # models/caja.py

    @classmethod
    def obtener_caja(cls):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT total FROM caja WHERE id = 1")
        resultado = cursor.fetchone()
        conexion.close()
        if resultado:
            # EL CAMBIO CLAVE: Forzamos float acá para que self.total sea compatible
            return cls(float(resultado[0])) 
        else:
            # Si no hay nada, arrancamos en 0.0 (que es float)
            return cls(0.0)

    # models/caja.py

    def actualizar_total(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Forzamos que sea float por las dudas
        monto_limpio = float(self.total)
        
        # Intentamos actualizar
        cursor.execute("UPDATE caja SET total = %s WHERE id = 1", (monto_limpio,))
        
        # Si no existía el registro 1 (porque borraste la tabla), lo creamos
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO caja (id, total) VALUES (1, %s)", (monto_limpio,))
            
        conexion.commit()
        conexion.close()

    def sumar(self, monto):
        self.total += monto
        self.actualizar_total()

    def restar(self, monto):
        self.total -= monto
        self.actualizar_total()

    def modificar_manual(self, nuevo_total):
        self.total = nuevo_total
        self.actualizar_total()
