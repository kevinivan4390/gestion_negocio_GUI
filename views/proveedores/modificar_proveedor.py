# views/proveedores/modificar_proveedor.py

import tkinter as tk
from tkinter import messagebox
from models.proveedor import Proveedor
from utils.validaciones import validar_texto, validar_mail, validar_telefono

class ModificarProveedorView(tk.Toplevel):
    def __init__(self, master, datos_proveedor):
        super().__init__(master)
        self.title("Modificar Proveedor")
        self.geometry("400x500")
        self.master = master

        self.proveedor = Proveedor(*datos_proveedor)

        self.create_widgets()

    def create_widgets(self):
        labels = ["Nombre", "Teléfono", "Dirección", "Mail"]
        atributos = [self.proveedor.nombre, self.proveedor.telefono, self.proveedor.direccion, self.proveedor.mail]
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
        self.proveedor.nombre = self.entries["nombre"].get()
        self.proveedor.telefono = self.entries["teléfono"].get()
        self.proveedor.direccion = self.entries["dirección"].get()
        self.proveedor.mail = self.entries["mail"].get()

        if not self.proveedor.nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio.")
            return
        if not validar_texto(self.proveedor.nombre):
            messagebox.showwarning("Advertencia", "El nombre debe tener solo letras.")
            return
        if self.proveedor.mail and not validar_mail(self.proveedor.mail):
            messagebox.showwarning("Advertencia", "El correo no es válido.")
            return
        if self.proveedor.telefono and not validar_telefono(self.proveedor.telefono):
            messagebox.showwarning("Advertencia", "El teléfono no es válido.")
            return

        self.proveedor.guardar()
        messagebox.showinfo("Proveedor Modificado", "Los cambios fueron guardados correctamente.")
        self.master.ver_todos_proveedores()
        self.destroy()
