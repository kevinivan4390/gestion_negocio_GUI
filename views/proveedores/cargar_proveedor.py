# views/proveedores/cargar_proveedor.py

import tkinter as tk
from tkinter import messagebox
from models.proveedor import Proveedor
from utils.validaciones import validar_texto, validar_mail, validar_telefono

class CargarProveedorView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Agregar Proveedor")
        self.geometry("400x500")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        labels = ["Nombre", "Teléfono", "Dirección", "Mail"]
        self.entries = {}

        for idx, label_text in enumerate(labels):
            label = tk.Label(self, text=label_text, font=("Arial", 12))
            label.pack(pady=(10 if idx == 0 else 5, 0))
            entry = tk.Entry(self, font=("Arial", 12))
            entry.pack(pady=5, padx=10, fill="x")
            self.entries[label_text.lower()] = entry

        boton_guardar = tk.Button(self, text="Guardar Proveedor", command=self.guardar_proveedor, bg="lightgrey", font=("Arial", 12))
        boton_guardar.pack(pady=20, ipadx=20, ipady=10)
        self.agregar_hover(boton_guardar)

    def agregar_hover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg="lightblue"))
        boton.bind("<Leave>", lambda e: boton.config(bg="lightgrey"))

    def guardar_proveedor(self):
        nombre = self.entries["nombre"].get()
        telefono = self.entries["teléfono"].get()
        direccion = self.entries["dirección"].get()
        mail = self.entries["mail"].get()

        if not nombre:
            messagebox.showwarning("Advertencia", "El nombre es obligatorio.")
            return
        if not validar_texto(nombre):
            messagebox.showwarning("Advertencia", "El nombre debe tener solo letras.")
            return
        if mail and not validar_mail(mail):
            messagebox.showwarning("Advertencia", "El correo no es válido.")
            return
        if telefono and not validar_telefono(telefono):
            messagebox.showwarning("Advertencia", "El teléfono no es válido.")
            return

        proveedor = Proveedor(None, nombre, telefono, direccion, mail)
        proveedor.guardar()
        messagebox.showinfo("Proveedor Guardado", "El proveedor se guardó correctamente.")
        self.master.ver_todos_proveedores()
        self.destroy()
