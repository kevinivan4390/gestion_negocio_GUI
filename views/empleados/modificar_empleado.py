# views/empleados/modificar_empleado.py

import tkinter as tk
from tkinter import messagebox
from models.empleado import Empleado

class ModificarEmpleadoView(tk.Toplevel):
    def __init__(self, master, datos_empleado):
        super().__init__(master)
        self.title("Modificar Empleado")
        self.geometry("400x550")
        self.master = master

        self.empleado = Empleado(*datos_empleado)

        self.create_widgets()

    def create_widgets(self):
        labels = ["Nombre", "Apellido", "DNI", "Edad", "Cargo", "Salario"]
        atributos = [self.empleado.nombre, self.empleado.apellido, self.empleado.dni, self.empleado.edad, self.empleado.cargo, self.empleado.salario]
        self.entries = {}

        for idx, (label_text, valor) in enumerate(zip(labels, atributos)):
            label = tk.Label(self, text=label_text, font=("Arial", 12))
            label.pack(pady=(10 if idx == 0 else 5, 0))
            entry = tk.Entry(self, font=("Arial", 12))
            entry.insert(0, valor)
            entry.pack(pady=5, padx=10, fill="x")
            self.entries[label_text.lower()] = entry

        boton_guardar = tk.Button(self, text="Guardar Cambios", command=self.guardar_cambios, bg="lightgrey", font=("Arial", 12))
        boton_guardar.pack(pady=20, ipadx=20, ipady=10)
        self.agregar_hover(boton_guardar)

    def agregar_hover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg="lightblue"))
        boton.bind("<Leave>", lambda e: boton.config(bg="lightgrey"))

    def guardar_cambios(self):
        self.empleado.nombre = self.entries["nombre"].get()
        self.empleado.apellido = self.entries["apellido"].get()
        self.empleado.dni = self.entries["dni"].get()
        self.empleado.edad = self.entries["edad"].get()
        self.empleado.cargo = self.entries["cargo"].get()
        self.empleado.salario = self.entries["salario"].get()

        self.empleado.guardar()
        messagebox.showinfo("Empleado Modificado", "Los cambios fueron guardados correctamente.")
        self.master.ver_todos_empleados()
        self.destroy()
