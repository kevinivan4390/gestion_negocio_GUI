# views/productos/catalogo_productos.py

import tkinter as tk
from tkinter import ttk, messagebox
from views.productos.cargar_producto import CargarProductoView
from views.productos.detalle_producto import DetalleProductoView
from database.db_productos import obtener_todos_productos, buscar_productos
from PIL import Image, ImageTk

class CatalogoProductosView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Catálogo de Productos")
        self.geometry("1100x700")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # === Cargar íconos ===
        self.plus_icon = ImageTk.PhotoImage(Image.open("resources/icons/plus_icon.png").resize((20, 20)))
        self.search_icon = ImageTk.PhotoImage(Image.open("resources/icons/search_icon.png").resize((20, 20)))

        # === Frame superior ===
        frame_superior = tk.Frame(self)
        frame_superior.pack(pady=10, fill="x")

        # Buscar producto (con icono al lado)
        label_buscar = tk.Label(frame_superior, text="Buscar Producto:", image=self.search_icon, compound="left", font=("Arial", 12))
        label_buscar.pack(side=tk.LEFT, padx=5)

        self.buscar_var = tk.StringVar()
        entry_busqueda = tk.Entry(frame_superior, textvariable=self.buscar_var)
        entry_busqueda.pack(side=tk.LEFT, padx=5)
        entry_busqueda.bind("<KeyRelease>", self.autocompletar_busqueda)
        entry_busqueda.bind("<Return>", self.abrir_detalle_producto)

        # Combobox de ordenamiento
        tk.Label(frame_superior, text="Ordenar por:").pack(side=tk.LEFT, padx=10)
        self.orden_var = tk.StringVar()
        self.combo_orden = ttk.Combobox(frame_superior, textvariable=self.orden_var, state="readonly")
        self.combo_orden['values'] = ("Nombre", "ID", "Fecha de vencimiento", "Variedad")
        self.combo_orden.current(0)
        self.combo_orden.pack(side=tk.LEFT)
        self.combo_orden.bind("<<ComboboxSelected>>", self.ordenar_productos)

        # Botón Agregar Producto
        boton_agregar = tk.Button(frame_superior, text=" Agregar Producto", image=self.plus_icon, compound="left", command=self.abrir_cargar_producto, bg="white")
        boton_agregar.pack(side=tk.RIGHT, padx=10)

        # === Frame para la tabla ===
        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True)

        self.scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
        self.scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Variedad", "Nombre", "Marca", "Tamaño", "Sabor", "Precio Compra", "Precio Venta", "Stock", "Vencimiento"),
                                 show="headings", yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.scroll_y.config(command=self.tree.yview)
        self.scroll_x.config(command=self.tree.xview)

        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        columnas = ["ID", "Variedad", "Nombre", "Marca", "Tamaño", "Sabor", "Precio Compra", "Precio Venta", "Stock", "Vencimiento"]
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=120)

        self.tree.bind("<Double-1>", self.abrir_detalle_producto)

        self.ver_todos_productos()

    def ver_todos_productos(self):
        self.tree.delete(*self.tree.get_children())
        self.productos = obtener_todos_productos()
        for p in self.productos:
            self.tree.insert("", tk.END, values=(
                p.id, p.variedad, p.nombre, p.marca, p.tamanio, p.sabor, f"${p.preciocompra:.2f}", f"${p.precioventa:.2f}", p.stock, p.vencimiento
            ))

    def autocompletar_busqueda(self, event=None):
        filtro = self.buscar_var.get()
        self.tree.delete(*self.tree.get_children())
        if filtro:
            self.productos = buscar_productos(filtro)
        else:
            self.productos = obtener_todos_productos()

        for p in self.productos:
            self.tree.insert("", tk.END, values=(
                p.id, p.variedad, p.nombre, p.marca, p.tamanio, p.sabor, f"${p.preciocompra:.2f}", f"${p.precioventa:.2f}", p.stock, p.vencimiento
            ))

        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])
            self.tree.focus(items[0])

    def ordenar_productos(self, event):
        criterio = self.orden_var.get()
        if criterio == "Nombre":
            self.productos.sort(key=lambda x: x.nombre.lower())
        elif criterio == "ID":
            self.productos.sort(key=lambda x: x.id)
        elif criterio == "Fecha de vencimiento":
            self.productos.sort(key=lambda x: str(x.vencimiento))
        elif criterio == "Variedad":
            self.productos.sort(key=lambda x: x.variedad.lower())
        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.productos:
            self.tree.insert("", tk.END, values=(
                p.id, p.variedad, p.nombre, p.marca, p.tamanio, p.sabor, f"${p.preciocompra:.2f}", f"${p.precioventa:.2f}", p.stock, p.vencimiento
            ))

    def abrir_cargar_producto(self):
        CargarProductoView(self)
        self.withdraw()

    def abrir_detalle_producto(self, event=None):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un producto.")
            return
        item = self.tree.item(seleccionado)
        producto = item["values"]
        DetalleProductoView(self, producto)
        self.withdraw()