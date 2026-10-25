# views/ventas/historial_ventas.py

import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from models.historial_ventas import HistorialVentasModel
from utils.historial_pdf_generator import generar_historial_pdf
from datetime import datetime
import re

class HistorialVentasView(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Historial de Ventas")
        self.master = master

        # === 1. CONFIGURACIÓN DE POSICIÓN, FOCO Y BLOQUEO ===
        ancho_v = 1200
        alto_v = 700
        x = (self.winfo_screenwidth() // 2) - (ancho_v // 2)
        y = (self.winfo_screenheight() // 2) - (alto_v // 2)
        self.geometry(f"{ancho_v}x{alto_v}+{x}+{y}")
        
        # Esto evita que la ventana se vaya atrás de la principal
        self.attributes("-topmost", True)
        # Bloquea el menú principal mientras ves el historial
        self.grab_set() 
        self.focus_force()
        # ===================================================

        self.create_widgets()
        self.ver_todas()

    def create_widgets(self):
        frame_filtros = tk.Frame(self)
        frame_filtros.pack(fill="x", pady=10)

        tk.Label(frame_filtros, text="Desde:").pack(side=tk.LEFT, padx=5)
        self.fecha_inicio = DateEntry(frame_filtros, date_pattern="yyyy-mm-dd")
        self.fecha_inicio.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_filtros, text="Hasta:").pack(side=tk.LEFT, padx=5)
        self.fecha_fin = DateEntry(frame_filtros, date_pattern="yyyy-mm-dd")
        self.fecha_fin.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_filtros, text="Cliente:").pack(side=tk.LEFT, padx=5)
        self.cliente_var = tk.StringVar()
        self.entry_cliente = tk.Entry(frame_filtros, textvariable=self.cliente_var)
        self.entry_cliente.pack(side=tk.LEFT, padx=5)

        boton_filtrar = tk.Button(frame_filtros, text="Filtrar", command=self.filtrar)
        boton_filtrar.pack(side=tk.LEFT, padx=10)

        boton_todos = tk.Button(frame_filtros, text="Mostrar Todos", command=self.ver_todas)
        boton_todos.pack(side=tk.LEFT, padx=10)

        boton_exportar = tk.Button(frame_filtros, text="Exportar a PDF", command=self.exportar_pdf)
        boton_exportar.pack(side=tk.RIGHT, padx=10)

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Fecha", "Cliente", "Total"), show="headings")
        self.tree.heading("ID", text="ID Venta")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Total", text="Total Final")

        self.tree.column("ID", anchor=tk.CENTER, width=80)
        self.tree.column("Fecha", anchor=tk.CENTER, width=200)
        self.tree.column("Cliente", anchor=tk.CENTER, width=300)
        self.tree.column("Total", anchor=tk.CENTER, width=120)

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Double-1>", self.ver_detalle_venta)

    def ver_todas(self):
        self.tree.delete(*self.tree.get_children())
        ventas = HistorialVentasModel.listar_todas()
        for v in ventas:
            self.tree.insert("", tk.END, values=(v['id'], v['fecha'].strftime("%d/%m/%Y %H:%M"), v['cliente'], f"${v['total_final']:.2f}"))

    def filtrar(self):
        fecha_inicio = self.fecha_inicio.get_date()
        fecha_fin = self.fecha_fin.get_date()
        cliente = self.cliente_var.get().strip()

        if cliente:
            ventas = HistorialVentasModel.listar_por_fecha_y_cliente(fecha_inicio, fecha_fin, cliente)
        else:
            ventas = HistorialVentasModel.listar_por_fecha(fecha_inicio, fecha_fin)

        self.tree.delete(*self.tree.get_children())
        for v in ventas:
            self.tree.insert("", tk.END, values=(v['id'], v['fecha'].strftime("%d/%m/%Y %H:%M"), v['cliente'], f"${v['total_final']:.2f}"))

    def exportar_pdf(self):
        ventas = []
        for item in self.tree.get_children():
            ventas.append(self.tree.item(item)['values'])

        if not ventas:
            messagebox.showwarning("Sin datos", "No hay ventas para exportar.", parent=self)
            return

        generar_historial_pdf(ventas)
        messagebox.showinfo("Exportación Completa", "El historial fue exportado exitosamente.", parent=self)

    def ver_detalle_venta(self, event):
        seleccionado = self.tree.selection()
        if not seleccionado:
            return
        
        item = self.tree.item(seleccionado)
        valores = item['values'] 
        
        id_venta = valores[0]
        total_final = float(valores[3].replace('$', ''))
        
        detalle = HistorialVentasModel.obtener_detalle_venta(id_venta)
        
        precios = re.findall(r'=\s\$(\d+\.\d+)', detalle)
        total_bruto = sum(float(p) for p in precios)
        
        monto_descontado = total_bruto - total_final
        porcentaje = round((monto_descontado * 100) / total_bruto) if total_bruto > 0 else 0

        resumen = f"ID Venta: {id_venta}\n"
        resumen += f"Cliente: {valores[2]}\n"
        resumen += "-" * 35 + "\n"
        resumen += f"{detalle}\n"
        resumen += "-" * 35 + "\n"
        resumen += f"Total Bruto: ${total_bruto:.2f}\n"
        resumen += f"Descuento Aplicado: {porcentaje}% (-${monto_descontado:.2f})\n"
        resumen += f"TOTAL FINAL: ${total_final:.2f}"
        
        # === 2. CAMBIO CLAVE: Usamos parent=self para que no se pierda el foco ===
        messagebox.showinfo(f"Detalle Venta ID {id_venta}", resumen, parent=self)

    # Liberamos el bloqueo si se cierra la ventana
    def destroy(self):
        self.grab_release()
        super().destroy()