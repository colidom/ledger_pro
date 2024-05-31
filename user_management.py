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

            # Frame para los botones de arriba
            top_button_frame = tk.Frame(user_list_window)
            top_button_frame.pack(pady=10)

            # Botones para registrar, editar y eliminar usuarios
            self.edit_button = tk.Button(
                top_button_frame,
                text="Editar usuario",
                width=15,
                command=self.edit_user,
                state=tk.DISABLED,  # Inicialmente deshabilitado
            )
            self.edit_button.pack(side=tk.LEFT, padx=5)

            self.delete_button = tk.Button(
                top_button_frame,
                text="Eliminar usuario",
                width=15,
                command=self.delete_user,
                state=tk.DISABLED,  # Inicialmente deshabilitado
            )
            self.delete_button.pack(side=tk.LEFT, padx=5)

            tk.Button(
                top_button_frame,
                text="Registrar usuario",
                width=15,
                command=self.open_create_user,
            ).pack(side=tk.LEFT, padx=5)

            self.tree = ttk.Treeview(
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
            self.tree.heading("Id", text="Id")
            self.tree.heading("Vivienda", text="Vivienda")
            self.tree.heading("Nombre", text="Nombre")
            self.tree.heading("Apellidos", text="Apellidos")
            self.tree.heading("Campo Adicional", text="Campo Adicional")

            # Ajustar el ancho de las columnas automáticamente al contenido
            self.tree.column("Id", width=50)  # Anchura de la columna "Id"
            self.tree.column("Vivienda", width=100)  # Anchura de la columna "Vivienda"
            self.tree.column("Nombre", width=100)  # Anchura de la columna "Nombre"
            self.tree.column(
                "Apellidos", width=150
            )  # Anchura de la columna "Apellidos"
            self.tree.column(
                "Campo Adicional", width=200
            )  # Anchura de la columna "Campo Adicional"

            for user in users:
                self.tree.insert("", tk.END, values=user)
            self.tree.pack(fill="both", expand=True)

            # Enlazar la función de selección del árbol
            self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
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

    def edit_user(self):
        messagebox.showinfo(
            "Editar Usuario", "¡El usuario ha sido editado correctamente!"
        )

    def delete_user(self):
        messagebox.showinfo(
            "Eliminar Usuario", "¡El usuario ha sido eliminado correctamente!"
        )

    def on_tree_select(self, event):
        # Obtener el índice del elemento seleccionado
        selected_item = self.tree.selection()
        # Habilitar/deshabilitar los botones según si hay un usuario seleccionado
        if selected_item:
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)


# Prueba del código
if __name__ == "__main__":
    user_management = UserManagement()
    user_management.open_view_users()
