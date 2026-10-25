# views/proveedores/detalle_proveedor.py

import tkinter as tk
from tkinter import messagebox
from models.proveedor import Proveedor
from views.proveedores.modificar_proveedor import ModificarProveedorView
from PIL import Image, ImageTk

class DetalleProveedorView(tk.Toplevel):
    def __init__(self, master, datos_proveedor):
        super().__init__(master)
        self.title(f"Detalle Proveedor ID {datos_proveedor[0]}")
        self.geometry("600x600")
        self.master = master

        self.proveedor = Proveedor(*datos_proveedor)

        self.create_widgets()

    def create_widgets(self):
        self.edit_icon = ImageTk.PhotoImage(Image.open("resources/icons/edit_icon.png").resize((24, 24)))
        self.delete_icon = ImageTk.PhotoImage(Image.open("resources/icons/delete_icon.png").resize((24, 24)))
        self.back_icon = ImageTk.PhotoImage(Image.open("resources/icons/back_icon.png").resize((24, 24)))

        tk.Label(self, text="Detalle del Proveedor", font=("Arial", 20, "bold")).pack(pady=20)

        atributos = [
            ("Nombre", self.proveedor.nombre),
            ("Teléfono", self.proveedor.telefono),
            ("Dirección", self.proveedor.direccion),
            ("Mail", self.proveedor.mail)
        ]

        for label, valor in atributos:
            tk.Label(self, text=f"{label}: {valor}", font=("Arial", 13)).pack(pady=3)

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=30)

        boton_modificar = tk.Button(frame_botones, text=" Modificar Proveedor", image=self.edit_icon, compound="left", font=("Arial", 12), bg="lightgrey", command=self.modificar_proveedor)
        boton_modificar.grid(row=0, column=0, padx=10, pady=10, ipadx=20, ipady=10)

        boton_eliminar = tk.Button(frame_botones, text=" Eliminar Proveedor", image=self.delete_icon, compound="left", font=("Arial", 12), bg="lightgrey", command=self.eliminar_proveedor)
        boton_eliminar.grid(row=0, column=1, padx=10, pady=10, ipadx=20, ipady=10)

        boton_volver = tk.Button(frame_botones, text=" Volver al Catálogo", image=self.back_icon, compound="left", font=("Arial", 12), bg="lightgrey", command=self.destroy)
        boton_volver.grid(row=1, column=0, columnspan=2, pady=20, ipadx=40, ipady=10)

        self.agregar_hover(boton_modificar)
        self.agregar_hover(boton_eliminar)
        self.agregar_hover(boton_volver)

    def agregar_hover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg="lightblue"))
        boton.bind("<Leave>", lambda e: boton.config(bg="lightgrey"))

    def modificar_proveedor(self):
        ModificarProveedorView(self, [
            self.proveedor.id,
            self.proveedor.nombre,
            self.proveedor.telefono,
            self.proveedor.direccion,
            self.proveedor.mail
        ])

    def eliminar_proveedor(self):
        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que desea eliminar a '{self.proveedor.nombre}'?")
        if confirmar:
            self.proveedor.eliminar()
            messagebox.showinfo("Proveedor Eliminado", "Proveedor eliminado correctamente.")
            self.master.ver_todos_proveedores()
            self.destroy()
