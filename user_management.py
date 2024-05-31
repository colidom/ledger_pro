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
        self.house_number_entry = tk.Entry(user_window)
        self.house_number_entry.pack(pady=5)

        tk.Label(user_window, text="Nombre:").pack(pady=5)
        self.name_entry = tk.Entry(user_window)
        self.name_entry.pack(pady=5)

        tk.Label(user_window, text="Apellidos:").pack(pady=5)
        self.lastname_entry = tk.Entry(user_window)
        self.lastname_entry.pack(pady=5)

        tk.Label(user_window, text="Campo Adicional:").pack(pady=5)
        self.additional_field_entry = tk.Entry(user_window)
        self.additional_field_entry.pack(pady=5)

        tk.Button(
            user_window,
            text="Guardar",
            command=self.save_user,
        ).pack(pady=10)

    def save_user(self):
        house_number = self.house_number_entry.get()
        name = self.name_entry.get()
        lastname = self.lastname_entry.get()
        additional_field = self.additional_field_entry.get()

        if house_number and name and lastname:
            self.db.insert_user(house_number, name, lastname, additional_field)
            messagebox.showinfo(
                "Usuario Guardado", "El usuario ha sido registrado correctamente."
            )
        else:
            messagebox.showerror(
                "Error", "Por favor complete todos los campos obligatorios."
            )

    def edit_user(self):
        selected_item = self.tree.selection()[0]
        if selected_item:
            # Obtener los valores del usuario seleccionado
            values = self.tree.item(selected_item, "values")
            user_id = values[0]  # ID del usuario
            house_number = values[1]
            name = values[2]
            lastname = values[3]
            additional_field = values[4]

            # Abrir la ventana de edición
            edit_window = tk.Toplevel()
            edit_window.title("Editar Usuario")
            edit_window.geometry("300x300")

            tk.Label(edit_window, text="Vivienda:").pack(pady=5)
            house_number_entry = tk.Entry(edit_window)
            house_number_entry.insert(0, house_number)
            house_number_entry.pack(pady=5)

            tk.Label(edit_window, text="Nombre:").pack(pady=5)
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, name)
            name_entry.pack(pady=5)

            tk.Label(edit_window, text="Apellidos:").pack(pady=5)
            lastname_entry = tk.Entry(edit_window)
            lastname_entry.insert(0, lastname)
            lastname_entry.pack(pady=5)

            tk.Label(edit_window, text="Campo Adicional:").pack(pady=5)
            additional_field_entry = tk.Entry(edit_window)
            additional_field_entry.insert(0, additional_field)
            additional_field_entry.pack(pady=5)

            # Botón para guardar los cambios
            tk.Button(
                edit_window,
                text="Guardar Cambios",
                command=lambda: self.update_user(
                    user_id,
                    house_number_entry.get(),
                    name_entry.get(),
                    lastname_entry.get(),
                    additional_field_entry.get(),
                    edit_window,
                ),
            ).pack(pady=10)
        else:
            messagebox.showerror("Error", "Por favor seleccione un usuario.")

    def update_user(
        self, user_id, house_number, name, lastname, additional_field, window
    ):
        if house_number and name and lastname:
            self.db.update_user(user_id, house_number, name, lastname, additional_field)
            messagebox.showinfo(
                "Usuario Actualizado", "El usuario ha sido actualizado correctamente."
            )
            window.destroy()
        else:
            messagebox.showerror(
                "Error", "Por favor complete todos los campos obligatorios."
            )

    def delete_user(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmation = messagebox.askyesno(
                "Confirmar Eliminación",
                "¿Está seguro de que desea eliminar este usuario?",
            )
            if confirmation:
                # Obtener el ID del usuario seleccionado
                user_id = self.tree.item(selected_item, "values")[0]
                # Eliminar el usuario de la base de datos
                self.db.delete_user(user_id)
                # Eliminar el usuario de la vista
                self.tree.delete(selected_item)
                messagebox.showinfo(
                    "Usuario Eliminado", "El usuario ha sido eliminado correctamente."
                )
        else:
            messagebox.showerror("Error", "Por favor seleccione un usuario.")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
