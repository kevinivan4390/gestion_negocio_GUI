# main.py

import tkinter as tk
from views.main_menu import MainMenu

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Gestión Comercial")
    root.geometry("800x600")
    app = MainMenu(master=root)
    app.mainloop()


