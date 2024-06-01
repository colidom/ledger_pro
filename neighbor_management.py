import tkinter as tk
from tkinter import ttk, messagebox
from database import LadgerProDB
from export_to_excel import export_to_excel


class NeighborManagement:
    def __init__(self):
        self.db = LadgerProDB("ladger_pro.db")

    def open_create_neighbor(self):
        self.create_neighbor_window()

    def open_view_neighbors(self):
        neighbors = self.db.get_all_neighbors()
        neighbor_list_window = tk.Toplevel()
        neighbor_list_window.title("Lista de Usuarios")
        neighbor_list_window.geometry("700x300")

        # Frame para los botones de arriba
        top_button_frame = tk.Frame(neighbor_list_window)
        top_button_frame.pack(pady=10)

        # Botones para registrar, editar, eliminar y exportar usuarios
        tk.Button(
            top_button_frame,
            text="Registrar vecino",
            width=15,
            command=self.open_create_neighbor,
        ).pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(
            top_button_frame,
            text="Editar vecino",
            width=15,
            command=self.edit_neighbor,
            state=tk.DISABLED,  # Inicialmente deshabilitado
        )
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(
            top_button_frame,
            text="Eliminar vecino",
            width=15,
            command=self.delete_neighbor,
            state=tk.DISABLED,  # Inicialmente deshabilitado
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)

        headers = ["Id", "Vivienda", "Nombre", "Apellidos", "Teléfono"]
        tk.Button(
            top_button_frame,
            text="Exportar a excel",
            width=15,
            command=lambda: export_to_excel(
                neighbors, "usuarios", headers
            ),  # Llama a la función export_to_excel con los datos de vecino y el nombre por defecto "usuarios"
        ).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(
            neighbor_list_window,
            columns=(
                "Id",
                "Vivienda",
                "Nombre",
                "Apellidos",
                "Teléfono",
            ),
            show="headings",
        )
        self.tree.heading("Id", text="Id")
        self.tree.heading("Vivienda", text="Vivienda")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Apellidos", text="Apellidos")
        self.tree.heading("Teléfono", text="Teléfono")

        # Calcular el ancho máximo de cada columna
        if neighbors:
            max_widths = [
                max(len(str(neighbor[i])) for neighbor in neighbors) * 10
                for i in range(len(neighbors[0]))
            ]
        else:
            max_widths = [
                0,
                0,
                0,
                0,
                0,
            ]  # Define anchos predeterminados si no hay usuarios

        # Ajustar el ancho de las columnas automáticamente al contenido
        for i, column in enumerate(self.tree["columns"]):
            self.tree.column(column, width=max_widths[i])

        for neighbor in neighbors:
            self.tree.insert("", tk.END, values=neighbor)
        self.tree.pack(fill="both", expand=True)

        # Enlazar la función de selección del árbol
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

    def create_neighbor_window(self):
        self.neighbor_window = tk.Toplevel()
        self.neighbor_window.title("Registro de Usuario")
        self.neighbor_window.geometry("300x300")

        tk.Label(self.neighbor_window, text="Vivienda:").pack(pady=5)

        # Aquí agregamos el Combobox para seleccionar la Vivienda
        properties = self.db.get_all_properties()
        property_options = [property_data[1] for property_data in properties]
        self.selected_property = tk.StringVar(self.neighbor_window)

        # Verificar si hay viviendas
        if property_options:
            self.selected_property.set(property_options[0])
        else:
            property_options = ["No se han dado de alta viviendas aún"]
            self.selected_property.set(property_options[0])

        ttk.Combobox(
            self.neighbor_window,
            textvariable=self.selected_property,
            values=property_options,
        ).pack(pady=5)

        tk.Label(self.neighbor_window, text="Nombre:").pack(pady=5)
        self.name_entry = tk.Entry(self.neighbor_window)
        self.name_entry.pack(pady=5)

        tk.Label(self.neighbor_window, text="Apellidos:").pack(pady=5)
        self.lastname_entry = tk.Entry(self.neighbor_window)
        self.lastname_entry.pack(pady=5)

        tk.Label(self.neighbor_window, text="Teléfono:").pack(pady=5)
        self.phone_entry = tk.Entry(self.neighbor_window)
        self.phone_entry.pack(pady=5)

        # Botón para guardar el vecino
        tk.Button(
            self.neighbor_window,
            text="Guardar",
            command=self.save_neighbor,
        ).pack(pady=10)

    def refresh_neighbor_list(self):
        neighbors = self.db.get_all_neighbors()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for neighbor in neighbors:
            self.tree.insert("", tk.END, values=neighbor)

    def save_neighbor(self):
        house_number = self.selected_property.get()
        name = self.name_entry.get()
        lastname = self.lastname_entry.get()
        phone = self.phone_entry.get()

        if not house_number or not name or not lastname or not phone:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        property_id = None
        properties = self.db.get_all_properties()
        for prop in properties:
            if prop[1] == house_number:
                property_id = prop[0]
                break

        if property_id is None:
            messagebox.showerror("Error", "No se encontró la vivienda seleccionada.")
            return

        try:
            self.db.insert_neighbor(house_number, name, lastname, phone, property_id)
            messagebox.showinfo("Éxito", "Vecino guardado exitosamente.")
            self.neighbor_window.destroy()  # Cerrar la ventana de creación
            self.refresh_neighbor_list()  # Refrescar la lista de vecinos
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el vecino: {e}")

    def edit_neighbor(self):
        selected_item = self.tree.selection()[0]
        if selected_item:
            # Obtener los valores del vecino seleccionado
            values = self.tree.item(selected_item, "values")
            neighbor_id = values[0]  # ID del vecino
            house_number = values[1]
            name = values[2]
            lastname = values[3]
            phone = values[4]

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

            tk.Label(edit_window, text="Teléfono:").pack(pady=5)
            phone_entry_edit = tk.Entry(edit_window)
            phone_entry_edit.insert(0, phone)
            phone_entry_edit.pack(pady=5)

            # Botón para guardar los cambios
            tk.Button(
                edit_window,
                text="Guardar Cambios",
                command=lambda: self.update_neighbor(
                    neighbor_id,
                    house_number_entry.get(),
                    name_entry.get(),
                    lastname_entry.get(),
                    phone_entry_edit.get(),
                    edit_window,
                ),
            ).pack(pady=10)
        else:
            messagebox.showerror("Error", "Por favor seleccione un vecino.")

    def update_neighbor(
        self, neighbor_id, house_number, name, lastname, additional_field, window
    ):
        if house_number and name and lastname:
            self.db.update_neighbor(
                neighbor_id, house_number, name, lastname, additional_field
            )
            # Actualizar la fila en el Treeview con los nuevos valores
            selected_item = self.tree.selection()
            self.tree.item(
                selected_item,
                values=(neighbor_id, house_number, name, lastname, additional_field),
            )
            messagebox.showinfo(
                "Usuario Actualizado", "El vecino ha sido actualizado correctamente."
            )
            window.destroy()
        else:
            messagebox.showerror(
                "Error", "Por favor complete todos los campos obligatorios."
            )

    def delete_neighbor(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmation = messagebox.askyesno(
                "Confirmar Eliminación",
                "¿Está seguro de que desea eliminar este vecino?",
            )
            if confirmation:
                # Obtener el ID del vecino seleccionado
                neighbor_id = self.tree.item(selected_item, "values")[0]
                # Eliminar el vecino de la base de datos
                self.db.delete_neighbor(neighbor_id)
                # Eliminar el vecino de la vista
                self.tree.delete(selected_item)
                messagebox.showinfo(
                    "Usuario Eliminado", "El vecino ha sido eliminado correctamente."
                )
        else:
            messagebox.showerror("Error", "Por favor seleccione un vecino.")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
