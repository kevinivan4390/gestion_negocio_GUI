# utils/historial_pdf_generator.py

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

def generar_historial_pdf(ventas):
    carpeta = "resources/reportes/"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{carpeta}HistorialVentas_{timestamp}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, height - 50, "Historial de Ventas")

    c.setFont("Helvetica-Bold", 10)
    headers = ["ID Venta", "Fecha", "Cliente", "Total Final"]
    x_positions = [50, 120, 250, 500]

    y = height - 80

    for idx, header in enumerate(headers):
        c.drawString(x_positions[idx], y, header)

    c.setFont("Helvetica", 10)
    y -= 20

    for venta in ventas:
        id_venta, fecha, cliente, total = venta
        c.drawString(x_positions[0], y, str(id_venta))
        c.drawString(x_positions[1], y, str(fecha))
        c.drawString(x_positions[2], y, str(cliente))
        c.drawString(x_positions[3], y, str(total))
        y -= 20

        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = height - 50

    c.save()
    return filename
