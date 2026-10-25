# views/main_menu.py

import tkinter as tk
from views.productos.catalogo_productos import CatalogoProductosView
from views.clientes.catalogo_clientes import CatalogoClientesView
from views.empleados.catalogo_empleados import CatalogoEmpleadosView
from views.proveedores.catalogo_proveedores import CatalogoProveedoresView
from views.caja.detalle_caja import DetalleCajaView
from views.ventas.realizar_venta import RealizarVentaView
from views.ventas.historial_ventas import HistorialVentasView

class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Sistema de Gestión Comercial")
        self.master.geometry("600x700")
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        frame_menu = tk.Frame(self)
        frame_menu.pack(pady=50)

        boton_productos = tk.Button(frame_menu, text="Productos", width=20, height=2, font=("Arial", 14), command=self.abrir_catalogo_productos)
        boton_productos.pack(pady=10)

        boton_clientes = tk.Button(frame_menu, text="Clientes", width=20, height=2, font=("Arial", 14), command=self.abrir_clientes)
        boton_clientes.pack(pady=10)

        boton_empleados = tk.Button(frame_menu, text="Empleados", width=20, height=2, font=("Arial", 14), command=self.abrir_empleados)
        boton_empleados.pack(pady=10)

        boton_proveedores = tk.Button(frame_menu, text="Proveedores", width=20, height=2, font=("Arial", 14), command=self.abrir_proveedores)
        boton_proveedores.pack(pady=10)

        boton_caja = tk.Button(frame_menu, text="Caja", width=20, height=2, font=("Arial", 14), command=self.abrir_caja)
        boton_caja.pack(pady=10)

        boton_realizar_venta = tk.Button(frame_menu, text="Realizar Venta", width=20, height=2, font=("Arial", 14), command=self.abrir_realizar_venta)
        boton_realizar_venta.pack(pady=10)

        boton_historial_ventas = tk.Button(frame_menu, text="Historial de Ventas", width=20, height=2, font=("Arial", 14), command=self.abrir_historial_ventas)
        boton_historial_ventas.pack(pady=10)

    def abrir_catalogo_productos(self):
        CatalogoProductosView(self.master)

    def abrir_clientes(self):
        CatalogoClientesView(self.master)

    def abrir_empleados(self):
        CatalogoEmpleadosView(self.master)

    def abrir_proveedores(self):
        CatalogoProveedoresView(self.master)

    def abrir_caja(self):
        DetalleCajaView(self.master)

    def abrir_realizar_venta(self):
        RealizarVentaView(self.master)

    def abrir_historial_ventas(self):
        HistorialVentasView(self.master)
