# views/caja/detalle_caja.py

import tkinter as tk
from tkinter import messagebox
from database.db_caja import obtener_total_caja, modificar_total_caja
from PIL import Image, ImageTk

class DetalleCajaView(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Detalle de Caja")
        self.master = master

        # === CONFIGURACIÓN DE POSICIÓN, FOCO Y BLOQUEO ===
        ancho_v = 800
        alto_v = 500
        x = (self.winfo_screenwidth() // 2) - (ancho_v // 2)
        y = (self.winfo_screenheight() // 2) - (alto_v // 2)
        self.geometry(f"{ancho_v}x{alto_v}+{x}+{y}")
        
        # Bloqueamos el resto de las ventanas para que solo puedas usar esta
        self.grab_set() 
        self.attributes("-topmost", True)
        self.focus_force()
        # ================================================

        self.create_widgets()

    def create_widgets(self):
        # Iconos
        self.refresh_icon = ImageTk.PhotoImage(Image.open("resources/icons/edit_icon.png").resize((24, 24)))
        self.reset_icon = ImageTk.PhotoImage(Image.open("resources/icons/reset_icon.png").resize((24, 24)))
        self.cash_icon = ImageTk.PhotoImage(Image.open("resources/icons/cash_icon.png").resize((64, 64)))
        self.cashbag_icon = ImageTk.PhotoImage(Image.open("resources/icons/cashbag_icon.png").resize((144, 144)))
        self.gold_icon = ImageTk.PhotoImage(Image.open("resources/icons/gold_icon.png").resize((144, 144)))

        # Frame principal
        frame_principal = tk.Frame(self)
        frame_principal.pack(expand=True, fill="both", padx=20, pady=20)

        frame_izquierdo = tk.Frame(frame_principal)
        frame_izquierdo.pack(side="left", expand=True, fill="y")
        tk.Label(frame_izquierdo, image=self.cashbag_icon).pack(expand=True, anchor="center")

        frame_central = tk.Frame(frame_principal)
        frame_central.pack(side="left", expand=True, fill="both")

        tk.Label(frame_central, image=self.cash_icon).pack(pady=10)
        tk.Label(frame_central, text="Total Actual en Caja:", font=("Arial", 16)).pack(pady=10)

        self.total_var = tk.StringVar()
        self.actualizar_total()

        self.label_total = tk.Label(frame_central, textvariable=self.total_var, font=("Arial", 24, "bold"))
        self.label_total.pack(pady=10)

        frame_modificar = tk.Frame(frame_central)
        frame_modificar.pack(pady=20)

        self.entry_modificar_total = tk.Entry(frame_modificar, font=("Arial", 14))
        self.entry_modificar_total.pack(side=tk.LEFT, padx=10)
        self.entry_modificar_total.bind("<Return>", self.modificar_total)

        boton_modificar = tk.Button(frame_modificar, image=self.refresh_icon, command=self.modificar_total, bg="white")
        boton_modificar.pack(side=tk.LEFT, padx=10)
        self.agregar_hover(boton_modificar)

        boton_reiniciar = tk.Button(frame_central, text=" Reiniciar Caja a 0", image=self.reset_icon, compound="left", font=("Arial", 12), bg="white", command=self.reiniciar_caja)
        boton_reiniciar.pack(pady=20, ipadx=20, ipady=10)
        self.agregar_hover(boton_reiniciar)

        frame_derecho = tk.Frame(frame_principal)
        frame_derecho.pack(side="right", expand=True, fill="y")
        tk.Label(frame_derecho, image=self.gold_icon).pack(expand=True, anchor="center")

    def agregar_hover(self, boton):
        boton.bind("<Enter>", lambda e: boton.config(bg="lightblue"))
        boton.bind("<Leave>", lambda e: boton.config(bg="white"))

    def actualizar_total(self):
        try:
            total_actual = float(obtener_total_caja())
            self.total_var.set(f"${total_actual:.2f}")
        except:
            self.total_var.set("$0.00")

    def modificar_total(self, event=None):
        try:
            monto = float(self.entry_modificar_total.get())
            total_actual = float(obtener_total_caja())
            nuevo_total = total_actual + monto
            
            if nuevo_total < 0:
                messagebox.showwarning("Valor inválido", "El total no puede ser negativo.", parent=self)
                return

            confirmar = messagebox.askyesno("Confirmar Movimiento", f"¿Desea sumar ${monto:.2f} al total?", parent=self)
            if confirmar:
                modificar_total_caja(nuevo_total)
                messagebox.showinfo("Éxito", "Caja actualizada correctamente.", parent=self)
                
                # Cerramos todo y volvemos a la principal
                self.cerrar_y_volver()

        except ValueError:
            messagebox.showwarning("Error", "Ingrese un número válido.", parent=self)

    def reiniciar_caja(self):
        confirmar = messagebox.askyesno("Confirmar Reinicio", "¿Está seguro que desea reiniciar la caja a 0?\n¡Esta acción no se puede deshacer!", parent=self)
        if confirmar:
            modificar_total_caja(0)
            messagebox.showinfo("Caja Reiniciada", "La caja fue reiniciada exitosamente.", parent=self)
            
            # Cerramos todo y volvemos a la principal
            self.cerrar_y_volver()

    def cerrar_y_volver(self):
        """Libera el mouse y cierra la ventana para quedar en la pantalla principal"""
        self.grab_release()
        self.destroy()

    # Si cierran con la X, también liberamos el bloqueo
    def destroy(self):
        self.grab_release()
        super().destroy()