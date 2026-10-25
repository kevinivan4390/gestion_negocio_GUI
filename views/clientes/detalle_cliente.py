# views/clientes/detalle_cliente.py

import tkinter as tk
from tkinter import messagebox
from models.cliente import Cliente
from views.clientes.modificar_cliente import ModificarClienteView
from PIL import Image, ImageTk

class DetalleClienteView(tk.Toplevel):
    def __init__(self, master, datos_cliente):
        super().__init__(master)
        self.title(f"Detalle Cliente ID {datos_cliente[0]}")
        self.geometry("600x650")
        self.master = master

        self.cliente = Cliente(*datos_cliente)

        self.create_widgets()

    def create_widgets(self):
        self.edit_icon = ImageTk.PhotoImage(Image.open("resources/icons/edit_icon.png").resize((24, 24)))
        self.delete_icon = ImageTk.PhotoImage(Image.open("resources/icons/delete_icon.png").resize((24, 24)))
        self.back_icon = ImageTk.PhotoImage(Image.open("resources/icons/back_icon.png").resize((24, 24)))

        tk.Label(self, text="Detalle del Cliente", font=("Arial", 20, "bold")).pack(pady=20)

        atributos = [
            ("Nombre", self.cliente.nombre),
            ("Apellido", self.cliente.apellido),
            ("Teléfono", self.cliente.telefono),
            ("DNI", self.cliente.dni),
            ("Dirección", self.cliente.direccion),
            ("Mail", self.cliente.mail)
        ]

        for label, valor in atributos:
            tk.Label(self, text=f"{label}: {valor}", font=("Arial", 13)).pack(pady=3)

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=30)

        boton_modificar = tk.Button(frame_botones, text=" Modificar Cliente", image=self.edit_icon, compound="left", font=("Arial", 12), bg="lightgrey", command=self.modificar_cliente)
        boton_modificar.grid(row=0, column=0, padx=10, pady=10, ipadx=20, ipady=10)

        boton_eliminar = tk.Button(frame_botones, text=" Eliminar Cliente", image=self.delete_icon, compound="left", font=("Arial", 12), bg="lightgrey", command=self.eliminar_cliente)
        boton_eliminar.grid(row=0, column=1, padx=10, pady=10, ipadx=20, ipady=10)

        boton_volver = tk.Button(frame_botones, text=" Volver al Catálogo", image=self.back_icon, compound="left", font=("Arial", 12), bg="lightgrey", command=self.destroy)
        boton_volver.grid(row=1, column=0, columnspan=2, pady=20, ipadx=40, ipady=10)

        self.agregar_hover(boton_modificar)
        self.agregar_hover(boton_eliminar)
        self.agregar_hover(boton_volver)

    def agregar_hover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg="lightblue"))
        boton.bind("<Leave>", lambda e: boton.config(bg="lightgrey"))

    def modificar_cliente(self):
        # El cambio clave es pasarle self.master (el Catálogo)
        ModificarClienteView(self.master, [
            self.cliente.id, self.cliente.nombre, self.cliente.apellido,
            self.cliente.telefono, self.cliente.dni, self.cliente.direccion, self.cliente.mail
        ])
        # Cerramos el detalle para que cuando cerremos modificar, 
        # aterricemos directo en el catálogo.
        self.destroy()

    def eliminar_cliente(self):
        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que desea eliminar a '{self.cliente.nombre} {self.cliente.apellido}'?")
        if confirmar:
            self.cliente.eliminar()
            messagebox.showinfo("Cliente Eliminado", "Cliente eliminado correctamente.")
            self.master.ver_todos_clientes()
            self.destroy()
