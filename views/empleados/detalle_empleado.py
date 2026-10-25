# views/empleados/detalle_empleado.py

import tkinter as tk
from tkinter import messagebox
from models.empleado import Empleado
from views.empleados.modificar_empleado import ModificarEmpleadoView
from PIL import Image, ImageTk

class DetalleEmpleadoView(tk.Toplevel):
    def __init__(self, master, datos_empleado):
        super().__init__(master)
        self.title(f"Detalle Empleado ID {datos_empleado[0]}")
        self.geometry("600x650")
        self.master = master

        self.empleado = Empleado(*datos_empleado)

        self.create_widgets()

    def create_widgets(self):
        self.edit_icon = ImageTk.PhotoImage(Image.open("resources/icons/edit_icon.png").resize((24, 24)))
        self.delete_icon = ImageTk.PhotoImage(Image.open("resources/icons/delete_icon.png").resize((24, 24)))
        self.back_icon = ImageTk.PhotoImage(Image.open("resources/icons/back_icon.png").resize((24, 24)))

        tk.Label(self, text="Detalle del Empleado", font=("Arial", 20, "bold")).pack(pady=20)

        atributos = [
            ("Nombre", self.empleado.nombre),
            ("Apellido", self.empleado.apellido),
            ("DNI", self.empleado.dni),
            ("Edad", self.empleado.edad),
            ("Cargo", self.empleado.cargo),
            ("Salario", f"${self.empleado.salario:.2f}")
        ]

        for label, valor in atributos:
            tk.Label(self, text=f"{label}: {valor}", font=("Arial", 13)).pack(pady=3)

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=30)

        boton_modificar = tk.Button(frame_botones, text=" Modificar Empleado", image=self.edit_icon, compound="left", font=("Arial", 12), bg="lightgrey", command=self.modificar_empleado)
        boton_modificar.grid(row=0, column=0, padx=10, pady=10, ipadx=20, ipady=10)

        boton_eliminar = tk.Button(frame_botones, text=" Eliminar Empleado", image=self.delete_icon, compound="left", font=("Arial", 12), bg="lightgrey", command=self.eliminar_empleado)
        boton_eliminar.grid(row=0, column=1, padx=10, pady=10, ipadx=20, ipady=10)

        boton_volver = tk.Button(frame_botones, text=" Volver al Catálogo", image=self.back_icon, compound="left", font=("Arial", 12), bg="lightgrey", command=self.destroy)
        boton_volver.grid(row=1, column=0, columnspan=2, pady=20, ipadx=40, ipady=10)

        self.agregar_hover(boton_modificar)
        self.agregar_hover(boton_eliminar)
        self.agregar_hover(boton_volver)

    def agregar_hover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg="lightblue"))
        boton.bind("<Leave>", lambda e: boton.config(bg="lightgrey"))

    def modificar_empleado(self):
        ModificarEmpleadoView(self, [
            self.empleado.id,
            self.empleado.nombre,
            self.empleado.apellido,
            self.empleado.dni,
            self.empleado.edad,
            self.empleado.cargo,
            self.empleado.salario
        ])

    def eliminar_empleado(self):
        confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Seguro que desea eliminar a '{self.empleado.nombre} {self.empleado.apellido}'?")
        if confirmar:
            self.empleado.eliminar()
            messagebox.showinfo("Empleado Eliminado", "Empleado eliminado correctamente.")
            self.master.ver_todos_empleados()
            self.destroy()
