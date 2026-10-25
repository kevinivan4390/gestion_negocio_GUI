# views/empleados/catalogo_empleados.py

import tkinter as tk
from tkinter import ttk, messagebox
from views.empleados.cargar_empleado import CargarEmpleadoView
from views.empleados.detalle_empleado import DetalleEmpleadoView
from database.db_empleados import obtener_todos_empleados, buscar_empleados
from PIL import Image, ImageTk

class CatalogoEmpleadosView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Catálogo de Empleados")
        self.geometry("1100x700")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        self.plus_icon = ImageTk.PhotoImage(Image.open("resources/icons/plus_icon.png").resize((20, 20)))
        self.search_icon = ImageTk.PhotoImage(Image.open("resources/icons/search_icon.png").resize((20, 20)))

        frame_superior = tk.Frame(self)
        frame_superior.pack(pady=10, fill="x")

        label_buscar = tk.Label(frame_superior, text="Buscar Empleado:", image=self.search_icon, compound="left", font=("Arial", 12))
        label_buscar.pack(side=tk.LEFT, padx=5)

        self.buscar_var = tk.StringVar()
        entry_busqueda = tk.Entry(frame_superior, textvariable=self.buscar_var)
        entry_busqueda.pack(side=tk.LEFT, padx=5)
        entry_busqueda.bind("<KeyRelease>", self.autocompletar_busqueda)
        entry_busqueda.bind("<Return>", self.abrir_detalle_empleado)

        tk.Label(frame_superior, text="Ordenar por:").pack(side=tk.LEFT, padx=10)
        self.orden_var = tk.StringVar()
        self.combo_orden = ttk.Combobox(frame_superior, textvariable=self.orden_var, state="readonly")
        self.combo_orden['values'] = ("Nombre", "Apellido", "ID", "DNI")
        self.combo_orden.current(0)
        self.combo_orden.pack(side=tk.LEFT)
        self.combo_orden.bind("<<ComboboxSelected>>", self.ordenar_empleados)

        boton_agregar = tk.Button(frame_superior, text=" Agregar Empleado", image=self.plus_icon, compound="left", command=self.abrir_cargar_empleado, bg="white")
        boton_agregar.pack(side=tk.RIGHT, padx=10)

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True)

        self.scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")
        self.scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")

        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Nombre", "Apellido", "DNI", "Edad", "Cargo", "Salario"),
                                 show="headings", yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)
        self.scroll_y.config(command=self.tree.yview)
        self.scroll_x.config(command=self.tree.xview)

        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        columnas = ["ID", "Nombre", "Apellido", "DNI", "Edad", "Cargo", "Salario"]
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=150)

        self.tree.bind("<Double-1>", self.abrir_detalle_empleado)

        self.ver_todos_empleados()

    def ver_todos_empleados(self):
        self.tree.delete(*self.tree.get_children())
        self.empleados = obtener_todos_empleados()
        for e in self.empleados:
            self.tree.insert("", tk.END, values=(
                e.id, e.nombre, e.apellido, e.dni, e.edad, e.cargo, f"${e.salario:.2f}"
            ))

    def autocompletar_busqueda(self, event=None):
        filtro = self.buscar_var.get()
        self.tree.delete(*self.tree.get_children())
        if filtro:
            self.empleados = buscar_empleados(filtro)
        else:
            self.empleados = obtener_todos_empleados()

        for e in self.empleados:
            self.tree.insert("", tk.END, values=(
                e.id, e.nombre, e.apellido, e.dni, e.edad, e.cargo, f"${e.salario:.2f}"
            ))

        items = self.tree.get_children()
        if items:
            self.tree.selection_set(items[0])
            self.tree.focus(items[0])

    def ordenar_empleados(self, event):
        criterio = self.orden_var.get()
        if criterio == "Nombre":
            self.empleados.sort(key=lambda x: x.nombre.lower())
        elif criterio == "Apellido":
            self.empleados.sort(key=lambda x: x.apellido.lower())
        elif criterio == "ID":
            self.empleados.sort(key=lambda x: x.id)
        elif criterio == "DNI":
            self.empleados.sort(key=lambda x: str(x.dni))
        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tree.delete(*self.tree.get_children())
        for e in self.empleados:
            self.tree.insert("", tk.END, values=(
                e.id, e.nombre, e.apellido, e.dni, e.edad, e.cargo, f"${e.salario:.2f}"
            ))

    def abrir_cargar_empleado(self):
        CargarEmpleadoView(self)

    def abrir_detalle_empleado(self, event=None):
        seleccionado = self.tree.selection()
        if not seleccionado:
            messagebox.showwarning("Advertencia", "Seleccione un empleado.")
            return
        item = self.tree.item(seleccionado)
        valores = item["values"]

        if valores:
            datos_empleado = [
                int(valores[0]),              # id
                valores[1],                   # nombre
                valores[2],                   # apellido
                valores[3],                   # dni
                int(valores[4]),               # edad
                valores[5],                   # cargo
                float(str(valores[6]).replace("$", ""))  # salario
            ]
            DetalleEmpleadoView(self, datos_empleado)

