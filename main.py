import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import UserDatabase
import webbrowser


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("LedgerPro - Gestión de Comunidad")
        self.root.geometry("400x400")

        # Inicializar la base de datos
        self.db = UserDatabase("users.db")

        self.create_widgets()

        self.create_widgets()

    def create_widgets(self):
        # Título
        tk.Label(self.root, text="LedgerPro", font=("Arial", 26)).pack(pady=25)

        # Botones de navegación
        tk.Button(
            self.root, text="Registro de Usuarios", width=25, command=self.open_users
        ).pack(pady=5)
        tk.Button(
            self.root, text="Registro de Ingresos", width=25, command=self.open_income
        ).pack(pady=5)
        tk.Button(
            self.root, text="Registro de Gastos", width=25, command=self.open_expenses
        ).pack(pady=5)
        tk.Button(
            self.root, text="Deudas de Vecinos", width=25, command=self.open_debts
        ).pack(pady=5)

        # Enlace a GitHub
        self.add_github_link()

    def add_github_link(self):
        # Cargar el icono de GitHub
        github_image = Image.open(
            "./img/github_icon.jpg"
        )  # Asegúrate de tener este archivo en el mismo directorio
        github_image = github_image.resize((30, 30), Image.BILINEAR)
        github_icon = ImageTk.PhotoImage(github_image)

        # Crear el botón con el icono de GitHub
        github_button = tk.Button(
            self.root, image=github_icon, command=self.open_github
        )
        github_button.image = github_icon  # Guardar una referencia para evitar que se recoja por el recolector de basura
        github_button.pack(pady=20)

    def open_github(self):
        webbrowser.open_new("https://github.com/colidom/ledger_pro")

    def open_users(self):
        messagebox.showinfo("Usuarios", "Aquí se abrirá la gestión de usuarios.")

    def open_income(self):
        messagebox.showinfo("Ingresos", "Aquí se abrirá el registro de ingresos.")

    def open_expenses(self):
        messagebox.showinfo("Gastos", "Aquí se abrirá el registro de gastos.")

    def open_debts(self):
        messagebox.showinfo("Deudas", "Aquí se abrirá la gestión de deudas.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
