import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database import UserDatabase
from tkinter import ttk  # Importamos ttk para usar ttk.Treeview


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("LedgerPro - Gestión de Comunidad")
        self.root.geometry("400x400")

        # Inicializar la base de datos
        self.db = UserDatabase("users.db")

        self.create_widgets()

    def create_widgets(self):
        # Título
        tk.Label(self.root, text="LedgerPro", font=("Arial", 26)).pack(pady=25)

        # Botones de navegación
        tk.Button(
            self.root,
            text="Registro de Usuarios",
            width=25,
            command=self.open_create_user,
        ).pack(pady=5)
        tk.Button(
            self.root, text="Ver Usuarios", width=25, command=self.open_view_users
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
        import webbrowser

        webbrowser.open_new("https://github.com/colidom/ledger_pro")

    def open_create_user(self):
        self.create_user_window()

    def open_view_users(self):
        users = self.db.get_all_users()
        if users:
            user_list_window = tk.Toplevel(self.root)
            user_list_window.title("Lista de Usuarios")
            user_list_window.geometry("700x300")
            tree = ttk.Treeview(
                user_list_window,
                columns=(
                    "Id",
                    "Número de Vivienda",
                    "Nombre",
                    "Apellidos",
                    "Campo Adicional",
                ),
                show="headings",
            )
            tree.heading("Id", text="Id")
            tree.heading("Número de Vivienda", text="Número de Vivienda")
            tree.heading("Nombre", text="Nombre")
            tree.heading("Apellidos", text="Apellidos")
            tree.heading("Campo Adicional", text="Campo Adicional")

            # Ajustar el ancho de las columnas automáticamente al contenido
            tree.column("Id", width=50)  # Anchura de la columna "Id"
            tree.column(
                "Número de Vivienda", width=100
            )  # Anchura de la columna "Número de Vivienda"
            tree.column("Nombre", width=100)  # Anchura de la columna "Nombre"
            tree.column("Apellidos", width=150)  # Anchura de la columna "Apellidos"
            tree.column(
                "Campo Adicional", width=200
            )  # Anchura de la columna "Campo Adicional"

            for user in users:
                tree.insert("", tk.END, values=user)
            tree.pack(fill="both", expand=True)
        else:
            messagebox.showinfo(
                "No hay Usuarios", "No hay usuarios registrados en la base de datos."
            )

    def create_user_window(self):
        user_window = tk.Toplevel(self.root)
        user_window.title("Registro de Usuario")
        user_window.geometry("300x200")

        tk.Label(user_window, text="Número de Vivienda:").pack(pady=5)
        house_number_entry = tk.Entry(user_window)
        house_number_entry.pack(pady=5)

        tk.Label(user_window, text="Nombre:").pack(pady=5)
        name_entry = tk.Entry(user_window)
        name_entry.pack(pady=5)

        tk.Label(user_window, text="Apellidos:").pack(pady=5)
        lastname_entry = tk.Entry(user_window)
        lastname_entry.pack(pady=5)

        tk.Label(user_window, text="Campo Adicional:").pack(pady=5)
        additional_field_entry = tk.Entry(user_window)
        additional_field_entry.pack(pady=5)

        tk.Button(
            user_window,
            text="Guardar",
            command=lambda: self.save_user(
                house_number_entry.get(),
                name_entry.get(),
                lastname_entry.get(),
                additional_field_entry.get(),
                user_window,
            ),
        ).pack(pady=10)

    def save_user(self, house_number, name, lastname, additional_field, window):
        self.db.insert_user(house_number, name, lastname, additional_field)
        messagebox.showinfo(
            "Usuario Guardado", "El usuario ha sido registrado correctamente."
        )
        window.destroy()

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
