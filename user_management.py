import tkinter as tk
from tkinter import ttk, messagebox
from database import UserDatabase


class UserManagement:
    def __init__(self):
        self.db = UserDatabase("users.db")

    def open_create_user(self):
        self.create_user_window()

    def open_view_users(self):
        users = self.db.get_all_users()
        if users:
            user_list_window = tk.Toplevel()
            user_list_window.title("Lista de Usuarios")
            user_list_window.geometry("700x300")
            tree = ttk.Treeview(
                user_list_window,
                columns=(
                    "Id",
                    "Vivienda",
                    "Nombre",
                    "Apellidos",
                    "Campo Adicional",
                ),
                show="headings",
            )
            tree.heading("Id", text="Id")
            tree.heading("Vivienda", text="Vivienda")
            tree.heading("Nombre", text="Nombre")
            tree.heading("Apellidos", text="Apellidos")
            tree.heading("Campo Adicional", text="Campo Adicional")

            # Ajustar el ancho de las columnas automáticamente al contenido
            tree.column("Id", width=50)  # Anchura de la columna "Id"
            tree.column("Vivienda", width=100)  # Anchura de la columna "Vivienda"
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
        user_window = tk.Toplevel()
        user_window.title("Registro de Usuario")
        user_window.geometry("300x300")

        tk.Label(user_window, text="Vivienda:").pack(pady=5)
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
