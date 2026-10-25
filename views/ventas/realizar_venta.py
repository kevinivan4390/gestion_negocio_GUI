# views/ventas/realizar_venta.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from models.venta import Venta
from database.db_ventas import guardar_venta
from database.db_caja import sumar_a_caja
from database.db_clientes import buscar_clientes
from database.db_productos import buscar_productos, actualizar_stock
from utils.pdf_generator import generar_factura_pdf

class RealizarVentaView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Realizar Venta")
        self.geometry("1400x900")
        self.master = master
        self.venta = Venta()
        self.productos_encontrados = []
        self.clientes_encontrados = []
        
        self.create_widgets()
        
        # --- CONFIGURACIÓN INICIAL ---
        self.check_no_registrado.set(1)
        self.toggle_cliente()
        self.autocompletar_productos()

    def create_widgets(self):
        """Crea todos los widgets de la ventana de realizar venta"""

        # Cargar iconos
        self.shop_icon = ImageTk.PhotoImage(Image.open("resources/icons/shop_icon.png").resize((40, 40)))
        self.trash_icon = ImageTk.PhotoImage(Image.open("resources/icons/delete_icon.png").resize((32, 32)))

        # --- Frame de Cliente (ARRIBA) ---
        frame_cliente = tk.LabelFrame(self, text="Datos del Cliente", font=("Arial", 14))
        frame_cliente.pack(side=tk.TOP, pady=10, padx=10, fill="x")

        tk.Label(frame_cliente, text="Buscar Cliente:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.entry_cliente = tk.Entry(frame_cliente, font=("Arial", 12))
        self.entry_cliente.pack(side=tk.LEFT, padx=5)
        self.entry_cliente.bind("<KeyRelease>", self.autocompletar_clientes)

        frame_list_cli = tk.Frame(frame_cliente)
        frame_list_cli.pack(side=tk.LEFT, padx=5)
        
        scroll_cli = tk.Scrollbar(frame_list_cli, orient="vertical")
        self.listbox_clientes = tk.Listbox(frame_list_cli, height=4, font=("Arial", 12), width=35, yscrollcommand=scroll_cli.set)
        scroll_cli.config(command=self.listbox_clientes.yview)
        
        self.listbox_clientes.pack(side=tk.LEFT)
        scroll_cli.pack(side=tk.RIGHT, fill="y")
        
        self.listbox_clientes.bind("<Double-1>", self.seleccionar_cliente)
        self.listbox_clientes.bind("<Return>", self.seleccionar_cliente)

        self.check_no_registrado = tk.IntVar()
        tk.Checkbutton(frame_cliente, text="No es cliente registrado", variable=self.check_no_registrado, command=self.toggle_cliente).pack(side=tk.LEFT, padx=5)

        tk.Button(frame_cliente, text="Registrar Nuevo Cliente", command=self.registrar_nuevo_cliente).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_cliente, text="Desmarcar Cliente", command=self.desmarcar_cliente).pack(side=tk.LEFT, padx=5)

        # --- Frame de Productos (ARRIBA) ---
        frame_producto = tk.LabelFrame(self, text="Agregar Producto", font=("Arial", 14))
        frame_producto.pack(side=tk.TOP, pady=10, padx=10, fill="x")

        tk.Label(frame_producto, text="Buscar Producto:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.entry_producto = tk.Entry(frame_producto, font=("Arial", 12))
        self.entry_producto.pack(side=tk.LEFT, padx=5)
        self.entry_producto.bind("<KeyRelease>", self.autocompletar_productos)

        frame_list_prod = tk.Frame(frame_producto)
        frame_list_prod.pack(side=tk.LEFT, padx=5)

        scroll_prod = tk.Scrollbar(frame_list_prod, orient="vertical")
        self.listbox_productos = tk.Listbox(frame_list_prod, height=6, font=("Arial", 12), width=50, yscrollcommand=scroll_prod.set)
        scroll_prod.config(command=self.listbox_productos.yview)

        self.listbox_productos.pack(side=tk.LEFT)
        scroll_prod.pack(side=tk.RIGHT, fill="y")
        
        self.listbox_productos.bind("<Double-1>", self.seleccionar_producto)
        self.listbox_productos.bind("<Return>", self.seleccionar_producto)

        tk.Label(frame_producto, text="Cantidad:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.cantidad_var = tk.StringVar(value="1")
        self.entry_cantidad = tk.Entry(frame_producto, textvariable=self.cantidad_var, font=("Arial", 12), width=5)
        self.entry_cantidad.pack(side=tk.LEFT, padx=5)

        boton_agregar_carrito = tk.Button(
            frame_producto,
            text="Agregar\nal Carrito",
            image=self.shop_icon,
            compound="top",
            font=("Arial", 11, "bold"),
            bg="lightblue",
            command=self.agregar_producto
        )
        boton_agregar_carrito.pack(side=tk.LEFT, padx=20, pady=5)

        # --- Frame Botones Confirmar/Cancelar (ABAJO DE TODO) ---
        frame_botones = tk.Frame(self)
        frame_botones.pack(side=tk.BOTTOM, pady=20)

        tk.Button(frame_botones, text="Confirmar Venta", bg="lightgreen", font=("Arial", 14, "bold"), command=self.confirmar_venta).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)
        tk.Button(frame_botones, text="Cancelar Venta", bg="lightcoral", font=("Arial", 14), command=self.destroy).pack(side=tk.LEFT, padx=10, ipadx=10, ipady=5)

        # --- Frame Totales y Descuento (ABAJO) ---
        frame_total = tk.Frame(self)
        frame_total.pack(side=tk.BOTTOM, pady=10, fill="x")

        frame_totales_interno = tk.Frame(frame_total)
        frame_totales_interno.pack(anchor="center")

        tk.Label(frame_totales_interno, text="Descuento %:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.descuento_var = tk.IntVar(value=0)
        self.entry_descuento = tk.Entry(frame_totales_interno, textvariable=self.descuento_var, font=("Arial", 12), width=5)
        self.entry_descuento.pack(side=tk.LEFT, padx=5)

        # Botones de aplicar/quitar
        tk.Button(frame_totales_interno, text="Aplicar", bg="lightgreen", command=self.actualizar_descuento).pack(side=tk.LEFT, padx=2)
        tk.Button(frame_totales_interno, text="Quitar", bg="lightcoral", command=self.quitar_descuento).pack(side=tk.LEFT, padx=2)

        self.label_total = tk.Label(frame_totales_interno, text="Total: $0.00", font=("Arial", 20, "bold"), fg="green")
        self.label_total.pack(side=tk.LEFT, padx=30)

        # --- Frame del Carrito (CENTRO - OCUPANDO EL RESTO) ---
        frame_carrito = tk.LabelFrame(self, text="Carrito de Productos", font=("Arial", 14))
        frame_carrito.pack(side=tk.TOP, pady=10, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(frame_carrito, columns=("Nombre", "Marca", "Tamaño", "Sabor", "Cantidad", "Precio Unitario", "Subtotal"), show="headings", selectmode="browse")
        for col in ("Nombre", "Marca", "Tamaño", "Sabor", "Cantidad", "Precio Unitario", "Subtotal"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        
        self.tree.pack(side=tk.TOP, fill="both", expand=True)

        boton_eliminar = tk.Button(frame_carrito, text=" Eliminar del Carrito", image=self.trash_icon, compound="left", font=("Arial", 12), bg="tomato", command=self.eliminar_producto_carrito)
        boton_eliminar.pack(side="bottom", pady=10)

    def toggle_cliente(self):
        if self.check_no_registrado.get():
            self.entry_cliente.config(state="disabled")
            self.listbox_clientes.config(state="disabled")
            self.entry_descuento.config(state="disabled")
            self.listbox_clientes.delete(0, tk.END)
            self.quitar_descuento()
        else:
            self.entry_cliente.config(state="normal")
            self.listbox_clientes.config(state="normal")
            self.entry_descuento.config(state="normal")
            self.autocompletar_clientes()

    def desmarcar_cliente(self):
        self.entry_cliente.delete(0, tk.END)
        self.entry_cliente.configure(bg="white")
        self.autocompletar_clientes()

    def autocompletar_clientes(self, event=None):
        texto = self.entry_cliente.get().lower()
        self.listbox_clientes.delete(0, tk.END)
        self.clientes_encontrados = buscar_clientes(texto)
        self.clientes_encontrados.sort(key=lambda c: c.nombre.lower())
        
        for c in self.clientes_encontrados:
            self.listbox_clientes.insert(tk.END, f"{c.nombre} {c.apellido} - DNI: {c.dni}")

    def seleccionar_cliente(self, event=None):
        try:
            index = self.listbox_clientes.curselection()[0]
            cliente = self.clientes_encontrados[index]
            self.entry_cliente.delete(0, tk.END)
            self.entry_cliente.insert(0, f"{cliente.nombre} {cliente.apellido}")
            self.entry_cliente.configure(bg="lightgreen")
            self.venta.cliente = f"{cliente.nombre} {cliente.apellido}"
        except IndexError:
            pass

    def autocompletar_productos(self, event=None):
        texto = self.entry_producto.get().lower()
        self.listbox_productos.delete(0, tk.END)
        self.productos_encontrados = buscar_productos(texto)
        self.productos_encontrados.sort(key=lambda p: p.nombre.lower())
        
        for p in self.productos_encontrados:
            datos = f"{p.nombre} - {p.marca} - {p.tamanio} - ${p.precioventa:.2f} (Stock: {p.stock})"
            self.listbox_productos.insert(tk.END, datos)

    def seleccionar_producto(self, event=None):
        self.agregar_producto()
        
    def agregar_producto(self):
            try:
                index = self.listbox_productos.curselection()[0]
                producto = self.productos_encontrados[index]
                cantidad = int(self.cantidad_var.get()) if self.cantidad_var.get() else 1

                if cantidad <= 0: return

                if cantidad > producto.stock:
                    messagebox.showwarning("Stock insuficiente", f"Solo hay {producto.stock} en stock.", parent=self)
                    return

                # Agregamos el producto a la venta
                self.venta.agregar_producto(producto.nombre, cantidad, producto.precioventa)
                
                subtotal = cantidad * producto.precioventa
                
                # EL CAMBIO: Guardamos el ID del producto en el campo 'iid' del treeview (aunque no se vea una columna para él)
                self.tree.insert("", tk.END, iid=f"prod_{producto.id}", values=(
                    producto.nombre, producto.marca, producto.tamanio, 
                    producto.sabor, cantidad, f"${producto.precioventa:.2f}", 
                    f"${subtotal:.2f}"
                ))

                self.actualizar_total()
                self.entry_producto.delete(0, tk.END)
                self.cantidad_var.set("1")
                self.autocompletar_productos() 
                
            except (IndexError, ValueError):
                messagebox.showwarning("Atención", "Seleccioná un producto de la lista y poné una cantidad válida.", parent=self)
                
    def eliminar_producto_carrito(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            nombre_p = item['values'][0]
            self.venta.productos = [p for p in self.venta.productos if p[0] != nombre_p]
            self.tree.delete(selected_item)
            self.venta.calcular_total()
            self.actualizar_total()

    def actualizar_total(self):
        self.label_total.config(text=f"Total: ${self.venta.total_final:.2f}")

    def actualizar_descuento(self, event=None):
        try:
            desc = int(self.descuento_var.get())
            if 0 <= desc <= 100:
                self.venta.aplicar_descuento(desc)
                self.actualizar_total()
                self.entry_descuento.configure(bg="lightgreen")
            else:
                messagebox.showwarning("Error", "El descuento debe estar entre 0 y 100.", parent=self)
        except ValueError:
            messagebox.showwarning("Error", "Ingresá un número válido.", parent=self)

    def quitar_descuento(self):
        self.descuento_var.set(0)
        self.venta.aplicar_descuento(0)
        self.actualizar_total()
        self.entry_descuento.configure(bg="white")

    def confirmar_venta(self):
        if not self.venta.productos:
            messagebox.showwarning("Carrito vacío", "No hay productos en la venta.", parent=self)
            return

        cliente_final = self.entry_cliente.get() if not self.check_no_registrado.get() else "Consumidor Final"
        self.venta.cliente = cliente_final
        
        # 1. Guardar la venta
        guardar_venta(self.venta)
        
        # 2. Sumar a la caja (con el float() que ya arreglamos)
        sumar_a_caja(float(self.venta.total_final))
        
        # 3. --- NUEVO: DESCONTAR STOCK ---
        for item_id in self.tree.get_children():
            # Sacamos el ID que guardamos antes (quitando el prefijo 'prod_')
            id_real = int(item_id.replace("prod_", ""))
            valores = self.tree.item(item_id)['values']
            cantidad_vendida = int(valores[4]) # La columna 4 es la Cantidad
            
            # Buscamos el producto en la lista para saber el stock viejo
            for p in self.productos_encontrados:
                if p.id == id_real:
                    nuevo_stock = p.stock - cantidad_vendida
                    actualizar_stock(id_real, nuevo_stock)
                    break
        # ---------------------------------
        
        generar_factura_pdf(self.venta)
        messagebox.showinfo("Éxito", "Venta confirmada, stock actualizado y comprobante generado.", parent=self)
        
        # Refrescamos el catálogo del master si existe la función
        if hasattr(self.master, "cargar_productos"):
            self.master.cargar_productos()
            
        self.destroy()

    def registrar_nuevo_cliente(self):
        from views.clientes.cargar_cliente import CargarClienteView
        CargarClienteView(self)