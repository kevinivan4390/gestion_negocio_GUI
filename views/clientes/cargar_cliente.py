# views/clientes/cargar_cliente.py

import tkinter as tk
from tkinter import messagebox
from models.cliente import Cliente
from tkcalendar import DateEntry
from utils.validaciones import validar_texto, validar_numero, validar_mail, validar_telefono


class CargarClienteView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Agregar Cliente")
        self.geometry("400x500")
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        labels = ["Nombre", "Apellido", "Teléfono", "DNI", "Dirección", "Mail"]
        self.entries = {}

        for idx, label_text in enumerate(labels):
            label = tk.Label(self, text=label_text, font=("Arial", 12))
            label.pack(pady=(10 if idx == 0 else 5, 0))
            entry = tk.Entry(self, font=("Arial", 12))
            entry.pack(pady=5, padx=10, fill="x")
            self.entries[label_text.lower()] = entry

        boton_guardar = tk.Button(self, text="Guardar Cliente", command=self.guardar_cliente, bg="lightgrey", font=("Arial", 12))
        boton_guardar.pack(pady=20, ipadx=20, ipady=10)
        self.agregar_hover(boton_guardar)

    def agregar_hover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg="lightblue"))
        boton.bind("<Leave>", lambda e: boton.config(bg="lightgrey"))


    def guardar_cliente(self):
        nombre = self.entries["nombre"].get()
        apellido = self.entries["apellido"].get()
        telefono = self.entries["teléfono"].get()
        dni = self.entries["dni"].get()
        direccion = self.entries["dirección"].get()
        mail = self.entries["mail"].get()

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
        if mail and not validar_mail(mail):
            messagebox.showwarning("Advertencia", "El correo electrónico no es válido.")
            return
        if telefono and not validar_telefono(telefono):
            messagebox.showwarning("Advertencia", "El teléfono no es válido.")
            return

        cliente = Cliente(None, nombre, apellido, telefono, dni, direccion, mail)
        cliente.guardar()
        messagebox.showinfo("Cliente Guardado", "El cliente se guardó correctamente.")
        self.master.ver_todos_clientes()
        self.destroy()

    
