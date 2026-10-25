# views/empleados/cargar_empleado.py

import tkinter as tk
from tkinter import messagebox
from models.empleado import Empleado
from utils.validaciones import validar_texto, validar_numero, validar_decimal

class CargarEmpleadoView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Agregar Empleado")
        self.geometry("400x550")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        labels = ["Nombre", "Apellido", "DNI", "Edad", "Cargo", "Salario"]
        self.entries = {}

        for idx, label_text in enumerate(labels):
            label = tk.Label(self, text=label_text, font=("Arial", 12))
            label.pack(pady=(10 if idx == 0 else 5, 0))
            entry = tk.Entry(self, font=("Arial", 12))
            entry.pack(pady=5, padx=10, fill="x")
            self.entries[label_text.lower()] = entry

        boton_guardar = tk.Button(self, text="Guardar Empleado", command=self.guardar_empleado, bg="lightgrey", font=("Arial", 12))
        boton_guardar.pack(pady=20, ipadx=20, ipady=10)
        self.agregar_hover(boton_guardar)

    def agregar_hover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg="lightblue"))
        boton.bind("<Leave>", lambda e: boton.config(bg="lightgrey"))


    def guardar_empleado(self):
        nombre = self.entries["nombre"].get()
        apellido = self.entries["apellido"].get()
        dni = self.entries["dni"].get()
        edad = self.entries["edad"].get()
        cargo = self.entries["cargo"].get()
        salario = self.entries["salario"].get()

        # Validaciones
        if not (nombre and apellido and dni):
            messagebox.showwarning("Advertencia", "Nombre, Apellido y DNI son obligatorios.")
            return
        if not validar_texto(nombre) or not validar_texto(apellido):
            messagebox.showwarning("Advertencia", "El nombre y apellido deben contener solo letras.")
            return
        if not validar_numero(dni):
            messagebox.showwarning("Advertencia", "El DNI debe ser numérico.")
            return
        if edad and not validar_numero(edad):
            messagebox.showwarning("Advertencia", "La edad debe ser un número positivo.")
            return
        if salario and not validar_decimal(salario):
            messagebox.showwarning("Advertencia", "El salario debe ser un número positivo.")
            return

        empleado = Empleado(None, nombre, apellido, dni, edad, cargo, salario)
        empleado.guardar()
        messagebox.showinfo("Empleado Guardado", "El empleado se guardó correctamente.")
        self.master.ver_todos_empleados()
        self.destroy()

