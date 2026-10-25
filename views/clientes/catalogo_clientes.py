# views/clientes/catalogo_clientes.py

import tkinter as tk
from tkinter import ttk, messagebox
from views.clientes.cargar_cliente import CargarClienteView
from views.clientes.detalle_cliente import DetalleClienteView
from database.db_clientes import obtener_todos_clientes, buscar_clientes
from PIL import Image, ImageTk

class CatalogoClientesView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Catálogo de Clientes")
        
        # === Centrar Ventana ===
        ancho_v = 1100
        alto_v = 700
        x = (self.winfo_screenwidth() // 2) - (ancho_v // 2)
        y = (self.winfo_screenheight() // 2) - (alto_v // 2)
        self.geometry(f"{ancho_v}x{alto_v}+{x}+{y}")
        
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.plus_icon = ImageTk.PhotoImage(Image.open("resources/icons/plus_icon.png").resize((20, 20)))
        self.search_icon = ImageTk.PhotoImage(Image.open("resources/icons/search_icon.png").resize((20, 20)))

        frame_superior = tk.Frame(self)
        frame_superior.pack(pady=10, fill="x")

        label_buscar = tk.Label(frame_superior, text="Buscar Cliente:", image=self.search_icon, compound="left", font=("Arial", 12))
        label_buscar.pack(side=tk.LEFT, padx=5)

        self.buscar_var = tk.StringVar()
        entry_busqueda = tk.Entry(frame_superior, textvariable=self.buscar_var)
        entry_busqueda.pack(side=tk.LEFT, padx=5)
        entry_busqueda.bind("<KeyRelease>", self.autocompletar_busqueda)
        entry_busqueda.bind("<Return>", self.abrir_detalle_cliente)

        tk.Label(frame_superior, text="Ordenar por:").pack(side=tk.LEFT, padx=10)
        self.orden_var = tk.StringVar()
        self.combo_orden = ttk.Combobox(frame_superior, textvariable=self.orden_var, state="readonly")
        self.combo_orden['values'] = ("Nombre", "Apellido", "ID", "DNI")
        self.combo_orden.current(0)
        self.combo_orden.pack(side=tk.LEFT)
        self.combo_orden.bind("<<ComboboxSelected>>", self.ordenar_clientes)

        boton_agregar = tk.Button(frame_superior, text=" Agregar Cliente", image=self.plus_icon, compound="left", command=self.abrir_cargar_cliente, bg="white")
        boton_agregar.pack(side=tk.RIGHT, padx=10)

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True)

        self.scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
        self.scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Apellido", "DNI", "Teléfono", "Dirección", "Mail"),
                                 show="headings", yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.scroll_y.config(command=self.tree.yview)
        self.scroll_x.config(command=self.tree.xview)

        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        columnas = ["ID", "Nombre", "Apellido", "DNI", "Teléfono", "Dirección", "Mail"]
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=150)

        self.tree.bind("<Double-1>", self.abrir_detalle_cliente)
        self.ver_todos_clientes()

    def ver_todos_clientes(self):
        self.tree.delete(*self.tree.get_children())
        self.clientes = obtener_todos_clientes()
        for c in self.clientes:
            self.tree.insert("", tk.END, values=(
                c.id, c.nombre, c.apellido, c.dni, c.telefono, c.direccion, c.mail
            ))

    def autocompletar_busqueda(self, event=None):
        filtro = self.buscar_var.get()
        self.tree.delete(*self.tree.get_children())
        if filtro:
            self.clientes = buscar_clientes(filtro)
        else:
            self.clientes = obtener_todos_clientes()

        for c in self.clientes:
            self.tree.insert("", tk.END, values=(
                c.id, c.nombre, c.apellido, c.dni, c.telefono, c.direccion, c.mail
            ))

    def ordenar_clientes(self, event):
        criterio = self.orden_var.get()
        if criterio == "Nombre":
            self.clientes.sort(key=lambda x: x.nombre.lower())
        elif criterio == "Apellido":
            self.clientes.sort(key=lambda x: x.apellido.lower())
        elif criterio == "ID":
            self.clientes.sort(key=lambda x: x.id)
        elif criterio == "DNI":
            self.clientes.sort(key=lambda x: str(x.dni))
        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tree.delete(*self.tree.get_children())
        for c in self.clientes:
            self.tree.insert("", tk.END, values=(
                c.id, c.nombre, c.apellido, c.dni, c.telefono, c.direccion, c.mail
            ))

    # === ACÁ ESTÁ EL FLUJO IGUAL A PRODUCTOS ===
    def abrir_cargar_cliente(self):
        CargarClienteView(self)
        self.withdraw()

    def abrir_detalle_cliente(self, event=None):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un cliente.", parent=self)
            return
        item = self.tree.item(seleccionado)
        cliente = item["values"]
        DetalleClienteView(self, cliente)
        self.withdraw()