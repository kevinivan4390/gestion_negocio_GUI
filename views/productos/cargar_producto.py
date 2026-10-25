# views/productos/cargar_producto.py

import tkinter as tk
from tkinter import messagebox
from models.producto import Producto
from utils.validaciones import validar_producto
from database.db_caja import restar_a_caja
from datetime import datetime
from tkcalendar import DateEntry
from decimal import Decimal


class CargarProductoView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Cargar Nuevo Producto")
        
        # === CONFIGURACIÓN DE POSICIÓN Y FOCO ===
        # 1. Definimos el tamaño deseado
        ancho_ventana = 500
        alto_ventana = 700
        
        # 2. Calculamos la posición para que quede en el centro de la pantalla
        x_screen = (self.winfo_screenwidth() // 2) - (ancho_ventana // 2)
        y_screen = (self.winfo_screenheight() // 2) - (alto_ventana // 2)
        
        # 3. Aplicamos el tamaño y la posición calculada
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x_screen}+{y_screen}")
        
        # 4. Forzamos que la ventana aparezca arriba de la principal (evita que se pierda atrás)
        self.attributes("-topmost", True)
        
        # 5. Le damos el foco del teclado automáticamente
        self.focus_force()
        # =========================================

        self.master = master
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Cargar Producto", font=("Arial", 18, "bold")).pack(pady=10)

        self.variedad_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.marca_var = tk.StringVar()
        self.tamanio_var = tk.StringVar()
        self.sabor_var = tk.StringVar()
        self.preciocompra_var = tk.DoubleVar()
        self.precioventa_var = tk.DoubleVar()
        self.stock_var = tk.IntVar()

        campos = [
            ("Variedad", self.variedad_var),
            ("Nombre", self.nombre_var),
            ("Marca", self.marca_var),
            ("Tamaño", self.tamanio_var),
            ("Sabor", self.sabor_var),
            ("Precio de compra", self.preciocompra_var),
            ("Precio de venta", self.precioventa_var),
            ("Stock", self.stock_var),
        ]

        for texto, variable in campos:
            tk.Label(self, text=texto + ":").pack()
            tk.Entry(self, textvariable=variable).pack()

        tk.Label(self, text="Fecha de vencimiento:").pack()
        self.date_entry = DateEntry(self, date_pattern="dd/MM/yyyy", mindate=datetime.now())
        self.date_entry.pack()

        self.boton_guardar = tk.Button(self, text="Guardar Producto", command=self.guardar_producto)
        self.boton_guardar.pack(pady=20)

    def guardar_producto(self):
        """Guarda un nuevo producto en la base de datos y descuenta el monto de la caja"""
        variedad = self.variedad_var.get()
        nombre = self.nombre_var.get()
        marca = self.marca_var.get()
        tamanio = self.tamanio_var.get()
        sabor = self.sabor_var.get()
        precio_compra = self.preciocompra_var.get()
        precio_venta = self.precioventa_var.get()
        stock = self.stock_var.get()
        vencimiento = self.date_entry.get_date()

        # Validar datos del producto
        valido, mensaje = validar_producto(nombre, marca, precio_compra, precio_venta, stock)
        if not valido:
            messagebox.showerror("Error de Validación", mensaje, parent=self)
            return

        # Confirmar carga del producto
        confirmacion = messagebox.askyesno(
            "Confirmar Carga",
            f"Nombre: {nombre}\nMarca: {marca}\nPrecio Compra: ${precio_compra:.2f}\n"
            f"Precio Venta: ${precio_venta:.2f}\nStock: {stock}\n¿Desea guardar el producto?",
            parent=self
        )
        if not confirmacion:
            return

        try:
            # 1. Crear el objeto producto
            nuevo_producto = Producto(
                variedad=variedad,
                nombre=nombre,
                marca=marca,
                tamanio=tamanio,
                sabor=sabor,
                preciocompra=precio_compra,
                precioventa=precio_venta,
                stock=stock,
                vencimiento=vencimiento
            )

            # 2. Guardar en base de datos
            nuevo_producto.guardar()

            # 3. Descontar de la caja
            monto_compra = float(precio_compra) * float(stock)
            restar_a_caja(monto_compra)

            # 4. Mostrar mensaje de éxito ANTES de destruir ventana
            messagebox.showinfo(
                "Producto Guardado",
                f"El producto fue cargado exitosamente.\nSe descontaron ${monto_compra:.2f} de la caja.",
                parent=self
            )

            # Le pedimos a la ventana de atrás (el catálogo) que se refresque sola
            # para ver el nuevo producto sin tener que cerrar y abrir el programa.
            if hasattr(self.master, "cargar_productos"):
                self.master.cargar_productos()
            
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar el producto:\n{str(e)}", parent=self)
            self.boton_guardar.config(state="normal")

