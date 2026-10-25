# models/venta.py

from datetime import datetime

class Venta:
    def __init__(self, cliente=None, descuento=0):
        self.fecha = datetime.now()
        self.cliente = cliente  # Puede ser None si no es registrado
        self.productos = []  # Lista de tuplas: (nombre, cantidad, precio_unitario, subtotal)
        self.total_bruto = 0
        self.descuento_aplicado = descuento  # Porcentaje (%)
        self.total_final = 0

    def agregar_producto(self, nombre, cantidad, precio_unitario):
        subtotal = cantidad * precio_unitario
        self.productos.append((nombre, cantidad, precio_unitario, subtotal))
        self.calcular_total()

    def calcular_total(self):
        self.total_bruto = sum(prod[3] for prod in self.productos)
        descuento_monto = (self.total_bruto * self.descuento_aplicado) / 100
        self.total_final = self.total_bruto - descuento_monto

    def aplicar_descuento(self, nuevo_descuento):
        self.descuento_aplicado = nuevo_descuento
        self.calcular_total()

    def generar_detalle(self):
        detalle = ""
        for nombre, cantidad, precio_unitario, subtotal in self.productos:
            detalle += f"{cantidad} x {nombre} @ ${precio_unitario:.2f} = ${subtotal:.2f}\n"
        return detalle

    def obtener_resumen(self):
        cliente_info = self.cliente if self.cliente else "Cliente no registrado"
        resumen = f"Fecha: {self.fecha.strftime('%d/%m/%Y %H:%M')}\n"
        resumen += f"Cliente: {cliente_info}\n"
        resumen += f"Detalle:\n{self.generar_detalle()}\n"
        resumen += f"Total bruto: ${self.total_bruto:.2f}\n"
        resumen += f"Descuento aplicado: {self.descuento_aplicado}%\n"
        resumen += f"Total final: ${self.total_final:.2f}\n"
        return resumen
