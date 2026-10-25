# views/productos/modificar_producto.py

import tkinter as tk
from tkinter import messagebox
from models.producto import Producto
from datetime import datetime
from tkcalendar import DateEntry

class ModificarProductoView(tk.Toplevel):
    def __init__(self, master, datos_producto):
        super().__init__(master)
        self.title(f"Modificar Producto ID {datos_producto[0]}")
        self.master = master

        # === CONFIGURACIÓN DE POSICIÓN, FOCO Y BLOQUEO ===
        ancho_v = 500
        alto_v = 700
        
        # Calculamos el centro de tu pantalla
        x = (self.winfo_screenwidth() // 2) - (ancho_v // 2)
        y = (self.winfo_screenheight() // 2) - (alto_v // 2)
        self.geometry(f"{ancho_v}x{alto_v}+{x}+{y}")
        
        # Esto hace que la ventana flote siempre arriba de la principal
        self.attributes("-topmost", True)
        
        # IMPORTANTE: Bloquea cualquier clic fuera de esta ventana hasta que se cierre
        self.grab_set() 
        
        # El cursor ya aparece listo para escribir
        self.focus_force()
        # ================================================

        # Cargamos los datos en el objeto Producto (limpiando los símbolos de pesos)
        self.producto = Producto(
            id=datos_producto[0],
            variedad=datos_producto[1],
            nombre=datos_producto[2],
            marca=datos_producto[3],
            tamanio=datos_producto[4],
            sabor=datos_producto[5],
            preciocompra=float(str(datos_producto[6]).replace("$", "")),
            precioventa=float(str(datos_producto[7]).replace("$", "")),
            stock=int(datos_producto[8]),
            vencimiento=datos_producto[9]
        )

        self.create_widgets()

    def create_widgets(self):
        """Armado de la interfaz con los datos actuales del producto"""
        tk.Label(self, text="Modificar Producto", font=("Arial", 18, "bold")).pack(pady=10)

        # Variables para los campos de texto
        self.variedad_var = tk.StringVar(value=self.producto.variedad)
        self.nombre_var = tk.StringVar(value=self.producto.nombre)
        self.marca_var = tk.StringVar(value=self.producto.marca)
        self.tamanio_var = tk.StringVar(value=self.producto.tamanio)
        self.sabor_var = tk.StringVar(value=self.producto.sabor)
        self.preciocompra_var = tk.DoubleVar(value=self.producto.preciocompra)
        self.precioventa_var = tk.DoubleVar(value=self.producto.precioventa)
        self.stock_var = tk.IntVar(value=self.producto.stock)

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

        # Generamos los labels y entries automáticamente
        for texto, variable in campos:
            tk.Label(self, text=texto + ":").pack()
            tk.Entry(self, textvariable=variable, width=40).pack(pady=2)

        # Calendario para la fecha de vencimiento
        tk.Label(self, text="Fecha de vencimiento:").pack(pady=(10, 0))
        try:
            fecha_vencimiento = datetime.strptime(str(self.producto.vencimiento), "%Y-%m-%d")
        except Exception:
            fecha_vencimiento = datetime.now()

        self.date_entry = DateEntry(self, date_pattern="dd/MM/yyyy", mindate=datetime.now())
        self.date_entry.set_date(fecha_vencimiento)
        self.date_entry.pack(pady=5)

        # Botón principal de guardado
        boton_guardar = tk.Button(self, text="Guardar Cambios", command=self.guardar_cambios, 
                                  bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10)
        boton_guardar.pack(pady=30)

    def guardar_cambios(self):
        """Lógica para validar, confirmar y guardar en la base de datos"""
        try:
            # Tomamos los datos de la interfaz
            self.producto.variedad = self.variedad_var.get()
            self.producto.nombre = self.nombre_var.get()
            self.producto.marca = self.marca_var.get()
            self.producto.tamanio = self.tamanio_var.get()
            self.producto.sabor = self.sabor_var.get()
            self.producto.preciocompra = float(self.preciocompra_var.get())
            self.producto.precioventa = float(self.precioventa_var.get())
            self.producto.stock = int(self.stock_var.get())
            self.producto.vencimiento = self.date_entry.get_date()

            # --- CONFIRMACIÓN ADELANTE Y AL MEDIO ---
            confirmacion = messagebox.askyesno(
                "Confirmar Modificación",
                f"¿Desea guardar los cambios del producto '{self.producto.nombre}'?",
                parent=self # Esto lo clava al centro de esta ventana
            )
            
            if confirmacion:
                # Guardamos en la DB
                self.producto.guardar()
                
                messagebox.showinfo("Éxito", "Los datos fueron modificados exitosamente.", parent=self)
                
                # --- CIERRE EN CADENA ---
                self.grab_release() # Liberamos el mouse/teclado
                
                if self.master:
                    self.master.deiconify() # Hacemos aparecer el catálogo de nuevo
                    if hasattr(self.master, "ver_todos_productos"):
                        self.master.ver_todos_productos() # Actualizamos la tabla para ver los cambios
                
                self.destroy() # Cerramos esta ventana

        except ValueError as e:
            messagebox.showerror("Error de Validación", f"Revisá los números ingresados: {str(e)}", parent=self)
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Algo salió mal: {str(e)}", parent=self)

    # Si el usuario cierra la ventana con la "X" de arriba, también liberamos el bloqueo
    def destroy(self):
        self.grab_release()
        super().destroy()