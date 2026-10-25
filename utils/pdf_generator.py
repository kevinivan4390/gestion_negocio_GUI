# utils/pdf_generator.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def generar_factura_pdf(venta):
    carpeta = "resources/facturas/"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    filename = f"{carpeta}Factura_{venta.fecha.strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Factura de Venta")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Fecha: {venta.fecha.strftime('%d/%m/%Y %H:%M')}")
    c.drawString(50, height - 120, f"Cliente: {venta.cliente or 'No registrado'}")

    y = height - 160
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Detalle:")
    y -= 20

    c.setFont("Helvetica", 10)
    for nombre, cantidad, precio_unitario, subtotal in venta.productos:
        c.drawString(50, y, f"{cantidad} x {nombre} @ ${precio_unitario:.2f} = ${subtotal:.2f}")
        y -= 15
        if y < 100:
            c.showPage()
            y = height - 50

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, f"Total Bruto: ${venta.total_bruto:.2f}")
    y -= 20
    c.drawString(50, y, f"Descuento Aplicado: {venta.descuento_aplicado}%")
    y -= 20
    c.drawString(50, y, f"Total Final: ${venta.total_final:.2f}")

    c.save()
