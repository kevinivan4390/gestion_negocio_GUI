# views/proveedores/catalogo_proveedores.py

import tkinter as tk
from tkinter import ttk, messagebox
from views.proveedores.cargar_proveedor import CargarProveedorView
from views.proveedores.detalle_proveedor import DetalleProveedorView
from database.db_proveedores import obtener_todos_proveedores, buscar_proveedores
from PIL import Image, ImageTk

class CatalogoProveedoresView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Catálogo de Proveedores")
        self.geometry("1000x700")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.plus_icon = ImageTk.PhotoImage(Image.open("resources/icons/plus_icon.png").resize((20, 20)))
        self.search_icon = ImageTk.PhotoImage(Image.open("resources/icons/search_icon.png").resize((20, 20)))

        frame_superior = tk.Frame(self)
        frame_superior.pack(pady=10, fill="x")

        label_buscar = tk.Label(frame_superior, text="Buscar Proveedor:", image=self.search_icon, compound="left", font=("Arial", 12))
        label_buscar.pack(side=tk.LEFT, padx=5)

        self.buscar_var = tk.StringVar()
        entry_busqueda = tk.Entry(frame_superior, textvariable=self.buscar_var)
        entry_busqueda.pack(side=tk.LEFT, padx=5)
        entry_busqueda.bind("<KeyRelease>", self.autocompletar_busqueda)
        entry_busqueda.bind("<Return>", self.abrir_detalle_proveedor)

        tk.Label(frame_superior, text="Ordenar por:").pack(side=tk.LEFT, padx=10)
        self.orden_var = tk.StringVar()
        self.combo_orden = ttk.Combobox(frame_superior, textvariable=self.orden_var, state="readonly")
        self.combo_orden['values'] = ("Nombre", "ID")
        self.combo_orden.current(0)
        self.combo_orden.pack(side=tk.LEFT)
        self.combo_orden.bind("<<ComboboxSelected>>", self.ordenar_proveedores)

        boton_agregar = tk.Button(frame_superior, text=" Agregar Proveedor", image=self.plus_icon, compound="left", command=self.abrir_cargar_proveedor, bg="white")
        boton_agregar.pack(side=tk.RIGHT, padx=10)

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True)

        self.scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
        self.scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Teléfono", "Dirección", "Mail"),
                                 show="headings", yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.scroll_y.config(command=self.tree.yview)
        self.scroll_x.config(command=self.tree.xview)

        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        columnas = ["ID", "Nombre", "Teléfono", "Dirección", "Mail"]
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=200)

        self.tree.bind("<Double-1>", self.abrir_detalle_proveedor)

        self.ver_todos_proveedores()

    def ver_todos_proveedores(self):
        self.tree.delete(*self.tree.get_children())
        self.proveedores = obtener_todos_proveedores()
        for p in self.proveedores:
            self.tree.insert("", tk.END, values=(
                p.id, p.nombre, p.telefono, p.direccion, p.mail
            ))

    def autocompletar_busqueda(self, event=None):
        filtro = self.buscar_var.get()
        self.tree.delete(*self.tree.get_children())
        if filtro:
            self.proveedores = buscar_proveedores(filtro)
        else:
            self.proveedores = obtener_todos_proveedores()

        for p in self.proveedores:
            self.tree.insert("", tk.END, values=(
                p.id, p.nombre, p.telefono, p.direccion, p.mail
            ))

        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])
            self.tree.focus(items[0])

    def ordenar_proveedores(self, event):
        criterio = self.orden_var.get()
        if criterio == "Nombre":
            self.proveedores.sort(key=lambda x: x.nombre.lower())
        elif criterio == "ID":
            self.proveedores.sort(key=lambda x: x.id)
        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.proveedores:
            self.tree.insert("", tk.END, values=(
                p.id, p.nombre, p.telefono, p.direccion, p.mail
            ))

    def abrir_cargar_proveedor(self):
        CargarProveedorView(self)

    def abrir_detalle_proveedor(self, event=None):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un proveedor.")
            return
        item = self.tree.item(seleccionado)
        proveedor = item["values"]
        DetalleProveedorView(self, proveedor)
