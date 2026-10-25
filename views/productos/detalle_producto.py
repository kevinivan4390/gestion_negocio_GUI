# views/productos/detalle_producto.py

import tkinter as tk
from tkinter import messagebox
from models.producto import Producto
from views.productos.modificar_producto import ModificarProductoView
from datetime import datetime, timedelta
from PIL import Image, ImageTk

class DetalleProductoView(tk.Toplevel):
    def __init__(self, master, datos_producto):
        super().__init__(master)
        self.title(f"Detalle Producto ID {datos_producto[0]}")
        
        # === 1. CAMBIO: CENTRAR VENTANA Y AGREGAR FOCO ===
        ancho_v = 700
        alto_v = 750
        x = (self.winfo_screenwidth() // 2) - (ancho_v // 2)
        y = (self.winfo_screenheight() // 2) - (alto_v // 2)
        self.geometry(f"{ancho_v}x{alto_v}+{x}+{y}")
        
        self.attributes("-topmost", True) # Asegura que aparezca adelante
        self.focus_force() # Toma el foco del teclado
        # ================================================

        self.master = master

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
        # === Cargar íconos ===
        self.edit_icon = ImageTk.PhotoImage(Image.open("resources/icons/edit_icon.png").resize((24, 24)))
        self.delete_icon = ImageTk.PhotoImage(Image.open("resources/icons/delete_icon.png").resize((24, 24)))
        
        # (El icono de volver ya no se usa, lo podés borrar si querés)

        # === Título ===
        tk.Label(self, text="Detalle del Producto", font=("Arial", 22, "bold")).pack(pady=20)

        # === Mostrar atributos ===
        atributos = [
            ("Variedad", self.producto.variedad),
            ("Nombre", self.producto.nombre),
            ("Marca", self.producto.marca),
            ("Tamaño", self.producto.tamanio),
            ("Sabor", self.producto.sabor),
            ("Precio Compra", f"${self.producto.preciocompra:.2f}"),
            ("Precio Venta", f"${self.producto.precioventa:.2f}"),
            ("Stock", self.producto.stock),
            ("Fecha de Vencimiento", self.producto.vencimiento)
        ]

        for label, valor in atributos:
            tk.Label(self, text=f"{label}: {valor}", font=("Arial", 13)).pack(pady=3)

        self.mostrar_advertencias()

        # === Frame para botones ===
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=30)

        # Botón Modificar
        self.boton_modificar = tk.Button(frame_botones, text=" Modificar Producto", image=self.edit_icon, compound="left", font=("Arial", 14),
                                         bg="lightgrey", command=self.modificar_producto)
        self.boton_modificar.grid(row=0, column=0, padx=15, pady=10, ipadx=30, ipady=15)

        # Botón Eliminar
        self.boton_eliminar = tk.Button(frame_botones, text=" Eliminar Producto", image=self.delete_icon, compound="left", font=("Arial", 14),
                                        bg="lightgrey", command=self.eliminar_producto)
        self.boton_eliminar.grid(row=0, column=1, padx=15, pady=10, ipadx=30, ipady=15)

        # === 2. CAMBIO: ELIMINAR BOTÓN VOLVER ===
        # Simplemente borré el bloque del boton_volver que estaba acá.
        # Para salir, el usuario usa la X o elige una acción.

        # Activar Hover
        self.agregar_hover(self.boton_modificar)
        self.agregar_hover(self.boton_eliminar)

    def mostrar_advertencias(self):
        if self.producto.stock <= 5:
            tk.Label(self, text="⚠️ ¡Stock Crítico!", fg="red", font=("Arial", 14, "bold")).pack(pady=10)

        try:
            fecha_venc = datetime.strptime(str(self.producto.vencimiento), "%Y-%m-%d")
            hoy = datetime.now()
            if fecha_venc - hoy <= timedelta(days=60):
                tk.Label(self, text="⚠️ ¡Producto Próximo a Vencer!", fg="orange", font=("Arial", 14, "bold")).pack(pady=10)
        except Exception:
            pass

    def agregar_hover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg="lightblue"))
        boton.bind("<Leave>", lambda e: boton.config(bg="lightgrey"))

    def modificar_producto(self):
        # === 3. CAMBIO: CERRAR DETALLE AL MODIFICAR ===
        # Importante: Le pasamos 'self.master' (el Catálogo) a la ventana de modificación
        # para que la Modificación sea hija del Catálogo y no de esta ventana que vamos a destruir.
        ModificarProductoView(self.master, [
            self.producto.id,
            self.producto.variedad,
            self.producto.nombre,
            self.producto.marca,
            self.producto.tamanio,
            self.producto.sabor,
            self.producto.preciocompra,
            self.producto.precioventa,
            self.producto.stock,
            self.producto.vencimiento
        ])
        
        self.destroy() # <--- Línea agregada: cierra el detalle al abrir modificar.

    def eliminar_producto(self):
        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que desea eliminar '{self.producto.nombre}'?", parent=self)
        if confirmar:
            self.producto.eliminar()
            messagebox.showinfo("Producto Eliminado", "Producto eliminado correctamente.", parent=self)
            
            # Al eliminar, despertamos el catálogo antes de cerrar
            if self.master:
                self.master.deiconify()
                self.master.ver_todos_productos()
            
            self.destroy()