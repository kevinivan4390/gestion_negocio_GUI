# views/clientes/modificar_cliente.py

import tkinter as tk
from tkinter import messagebox
from models.cliente import Cliente

class ModificarClienteView(tk.Toplevel):
    def __init__(self, master, datos_cliente):
        super().__init__(master)
        self.title("Modificar Cliente")
        self.geometry("400x500")
        self.master = master

        self.cliente = Cliente(*datos_cliente)

        self.create_widgets()

    def create_widgets(self):
        labels = ["Nombre", "Apellido", "Teléfono", "DNI", "Dirección", "Mail"]
        atributos = [self.cliente.nombre, self.cliente.apellido, self.cliente.telefono, self.cliente.dni, self.cliente.direccion, self.cliente.mail]
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
        self.cliente.nombre = self.entries["nombre"].get()
        self.cliente.apellido = self.entries["apellido"].get()
        self.cliente.telefono = self.entries["teléfono"].get()
        self.cliente.dni = self.entries["dni"].get()
        self.cliente.direccion = self.entries["dirección"].get()
        self.cliente.mail = self.entries["mail"].get()

        self.cliente.guardar()
        messagebox.showinfo("Cliente Modificado", "Los cambios fueron guardados correctamente.")
        self.master.ver_todos_clientes()
        self.destroy()
