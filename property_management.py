import tkinter as tk
from tkinter import ttk, messagebox
from database import LadgerProDB
from export_to_excel import export_to_excel


class PropertyManagement:
    def __init__(self):
        self.db = LadgerProDB("ladger_pro.db")

    def open_view_properties(self):
        properties = self.db.get_all_properties()
        property_list_window = tk.Toplevel()
        property_list_window.title("Lista de Viviendas")
        property_list_window.geometry("800x300")  # Aumentar el ancho de la ventana

        # Frame para los botones de arriba
        top_button_frame = tk.Frame(property_list_window)
        top_button_frame.pack(pady=10)

        # Botones para registrar, editar, eliminar y exportar viviendas
        tk.Button(
            top_button_frame,
            text="Registrar vivienda",
            width=20,
            command=self.open_create_property,
        ).pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(
            top_button_frame,
            text="Editar vivienda",
            width=20,
            command=self.edit_property,
            state=tk.DISABLED,  # Inicialmente deshabilitado
        )
        self.edit_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(
            top_button_frame,
            text="Eliminar vivienda",
            width=20,
            command=self.delete_property,
            state=tk.DISABLED,  # Inicialmente deshabilitado
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)

        headers = ["Id", "Vivienda", "Al Corriente de Pago", "Deuda Actual"]
        tk.Button(
            top_button_frame,
            text="Exportar a excel",
            width=20,
            command=lambda: export_to_excel(
                properties, "viviendas", headers
            ),  # Llama a la función export_to_excel con los datos
        ).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(
            property_list_window,
            columns=(
                "Id",
                "Vivienda",
                "Al Corriente de Pago",
                "Deuda Actual",
            ),
            show="headings",
        )
        self.tree.heading("Id", text="Id")
        self.tree.heading("Vivienda", text="Vivienda")
        self.tree.heading("Al Corriente de Pago", text="Al Corriente de Pago")
        self.tree.heading("Deuda Actual", text="Deuda Actual")

        # Configurar los colores de las etiquetas
        self.tree.tag_configure("debt", foreground="red")
        self.tree.tag_configure("no_debt", foreground="green")

        self.load_properties_into_tree(properties)

        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def load_properties_into_tree(self, properties):
        for property_data in properties:
            property_data = list(property_data)
            if property_data[2] == "No":
                tag = "debt"
            else:
                tag = "no_debt"
            property_data[3] = f"{property_data[3]}€" if property_data[3] else "0€"
            self.tree.insert("", tk.END, values=property_data, tags=(tag,))

    def open_create_property(self):
        self.create_property_window()

    def create_property_window(self):
        self.property_window = tk.Toplevel()
        self.property_window.title("Registro de Vivienda")
        self.property_window.geometry("300x300")

        tk.Label(self.property_window, text="Vivienda:").pack(pady=5)
        self.property_number_entry = tk.Entry(self.property_window)
        self.property_number_entry.pack(pady=5)

        tk.Label(self.property_window, text="Al Corriente de Pago:").pack(pady=5)
        self.is_paid_combobox = ttk.Combobox(
            self.property_window, state="readonly", values=["Si", "No"]
        )
        self.is_paid_combobox.pack(pady=5)
        self.is_paid_combobox.bind("<<ComboboxSelected>>", self.toggle_debt_entry)

        tk.Label(self.property_window, text="Deuda Actual:").pack(pady=5)
        self.debt_entry = tk.Entry(self.property_window, state="disabled")
        self.debt_entry.pack(pady=5)

        tk.Button(
            self.property_window,
            text="Registrar",
            command=self.save_property,
        ).pack(pady=10)

    def toggle_debt_entry(self, event):
        if self.is_paid_combobox.get() == "No":
            self.debt_entry.config(state="normal")
        else:
            self.debt_entry.config(state="disabled")
            self.debt_entry.delete(0, tk.END)

    def save_property(self):
        property_number = self.property_number_entry.get()
        is_paid = self.is_paid_combobox.get()
        debt_amount = self.debt_entry.get() if is_paid == "No" else "0"

        if property_number and is_paid:
            # Eliminar la Vivienda de marcador de posición "N/A" si existe
            for item in self.tree.get_children():
                values = self.tree.item(item, "values")
                if values[1] == "N/A":
                    self.tree.delete(item)
                    break

            self.db.insert_property(property_number, is_paid, debt_amount)
            # Obtener el ID de la vivienda recién insertada
            property_id = self.db.cursor.lastrowid
            # Insertar la nueva fila en el Treeview
            tag = "debt" if debt_amount != "0" else "no_debt"
            self.tree.insert(
                "",
                tk.END,
                values=(property_id, property_number, is_paid, f"{debt_amount}€"),
                tags=(tag,),
            )
            messagebox.showinfo(
                "Vivienda Guardada", "La Vivienda ha sido registrada correctamente."
            )
            # Cerrar la ventana de creación de vivienda
            self.property_window.destroy()
        else:
            messagebox.showerror(
                "Error", "Por favor complete todos los campos obligatorios."
            )

    def edit_property(self):
        selected_item = self.tree.selection()[0]
        if selected_item:
            # Obtener los valores de la vivienda seleccionada
            values = self.tree.item(selected_item, "values")
            property_id = values[0]  # ID de la vivienda
            property_number = values[1]
            is_paid = values[2]
            debt_amount = values[3].replace("€", "")

            # Abrir la ventana de edición
            edit_window = tk.Toplevel()
            edit_window.title("Editar Vivienda")
            edit_window.geometry("300x300")

            tk.Label(edit_window, text="Vivienda:").pack(pady=5)
            property_number_entry = tk.Entry(edit_window)
            property_number_entry.insert(0, property_number)
            property_number_entry.pack(pady=5)

            tk.Label(edit_window, text="Al Corriente de Pago:").pack(pady=5)
            is_paid_combobox = ttk.Combobox(
                edit_window, state="readonly", values=["Si", "No"]
            )
            is_paid_combobox.set(is_paid)
            is_paid_combobox.pack(pady=5)
            is_paid_combobox.bind("<<ComboboxSelected>>", self.toggle_edit_debt_entry)

            tk.Label(edit_window, text="Deuda Actual:").pack(pady=5)
            debt_entry = tk.Entry(
                edit_window, state="normal" if is_paid == "No" else "disabled"
            )
            debt_entry.insert(0, debt_amount)
            debt_entry.pack(pady=5)

            # Botón para guardar los cambios
            tk.Button(
                edit_window,
                text="Guardar Cambios",
                command=lambda: self.update_property(
                    property_id,
                    property_number_entry.get(),
                    is_paid_combobox.get(),
                    debt_entry.get() if is_paid_combobox.get() == "No" else "0",
                    edit_window,
                ),
            ).pack(pady=10)

    def update_property(
        self, property_id, property_number, is_paid, debt_amount, window
    ):
        if property_number and is_paid:
            self.db.update_property(property_id, property_number, is_paid, debt_amount)
            # Actualizar la fila en el Treeview con los nuevos valores
            selected_item = self.tree.selection()
            tag = "debt" if debt_amount != "0" else "no_debt"
            self.tree.item(
                selected_item,
                values=(property_id, property_number, is_paid, f"{debt_amount}€"),
                tags=(tag,),
            )
            messagebox.showinfo(
                "Vivienda Actualizada",
                "La vivienda ha sido actualizada correctamente.",
            )
            window.destroy()
        else:
            messagebox.showerror(
                "Error", "Por favor complete todos los campos obligatorios."
            )

    def toggle_edit_debt_entry(self, event):
        if event.widget.get() == "No":
            event.widget.master.children["!entry3"].config(state="normal")
        else:
            event.widget.master.children["!entry3"].config(state="disabled")
            event.widget.master.children["!entry3"].delete(0, tk.END)

    def delete_property(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmation = messagebox.askyesno(
                "Confirmar Eliminación",
                "¿Está seguro de que desea eliminar esta Vivienda?",
            )
            if confirmation:
                # Obtener el ID de la Vivienda seleccionada
                property_id = self.tree.item(selected_item, "values")[0]
                # Eliminar la Vivienda de la base de datos
                self.db.delete_property(property_id)
                # Eliminar la Vivienda de la vista
                self.tree.delete(selected_item)
                messagebox.showinfo(
                    "Vivienda Eliminada",
                    "La Vivienda ha sido eliminada correctamente.",
                )
        else:
            messagebox.showerror("Error", "Por favor seleccione una Vivienda.")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.edit_button.config(state=tk.NORMAL)
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.edit_button.config(state=tk.DISABLED)
            self.delete_button.config(state=tk.DISABLED)
