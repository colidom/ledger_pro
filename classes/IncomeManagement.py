import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db.database import LadgerProDB
from utils.export_to_excel import export_to_excel


class IncomeManagement:
    def __init__(self):
        self.db = LadgerProDB("ladger_pro.db")

    def open_incomes_view(self):
        self.income_window = tk.Toplevel()
        self.income_window.title("Registro de Ingresos")
        self.income_window.geometry("1000x400")

        top_button_frame = tk.Frame(self.income_window)
        top_button_frame.pack(pady=10)

        tk.Button(
            top_button_frame,
            text="Añadir Ingreso",
            width=20,
            command=self.open_add_income_window,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            top_button_frame,
            text="Editar Ingreso",
            width=20,
            command=self.edit_and_save_income,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            top_button_frame,
            text="Eliminar Ingreso",
            width=20,
            command=self.delete_income,
        ).pack(side=tk.LEFT, padx=5)

        headers = ["Id", "Cantidad", "Entidad", "Fecha", "Descripción"]

        tk.Button(
            top_button_frame,
            text="Exportar a Excel",
            width=20,
            command=lambda: export_to_excel(
                self.db.get_all_incomes(), "ingresos", headers
            ),
        ).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(
            self.income_window,
            columns=("Id", "Cantidad", "Entidad", "Fecha", "Descripción"),
            show="headings",
        )
        self.tree.heading("Id", text="Id")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Entidad", text="Entidad")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Descripción", text="Descripción")

        self.load_incomes_into_tree()

        self.tree.pack(fill="both", expand=True)

        tk.Button(
            self.income_window, text="Cerrar", command=self.close_income_window
        ).pack()

    def open_add_income_window(self):
        self.add_income_window = tk.Toplevel()
        self.add_income_window.title("Añadir Ingreso")
        self.add_income_window.geometry("400x300")

        tk.Label(self.add_income_window, text="Cantidad de Ingreso:").pack()
        self.income_amount_entry = tk.Entry(self.add_income_window)
        self.income_amount_entry.pack()

        tk.Label(self.add_income_window, text="Entidad que realiza el ingreso:").pack()
        self.income_entity_var = tk.StringVar(self.add_income_window)
        entities = self.get_property_list() + ["Otros"]
        self.income_entity_var.set(entities[0])
        self.income_entity_menu = tk.OptionMenu(
            self.add_income_window, self.income_entity_var, *entities
        )
        self.income_entity_menu.pack()

        tk.Label(self.add_income_window, text="Fecha del Ingreso (DD/MM/YYYY):").pack()
        self.income_date_entry = tk.Entry(self.add_income_window)
        self.income_date_entry.insert(
            0, datetime.now().strftime("%d/%m/%Y")
        )  # Fecha por defecto: hoy
        self.income_date_entry.pack()

        tk.Label(self.add_income_window, text="Descripción:").pack()
        self.income_description_entry = tk.Text(
            self.add_income_window, height=5, width=30
        )
        self.income_description_entry.pack()

        tk.Button(
            self.add_income_window, text="Guardar Ingreso", command=self.save_income
        ).pack(pady=10)

    def save_income(self):
        amount = self.income_amount_entry.get()
        entity = self.income_entity_var.get()
        date = self.income_date_entry.get()
        description = self.income_description_entry.get("1.0", "end-1c")

        try:
            formatted_date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Error", "Por favor ingrese una fecha válida (DD/MM/YYYY)."
            )
            return

        if amount and entity and formatted_date:
            self.db.insert_income(amount, entity, formatted_date, description)
            messagebox.showinfo("Éxito", "El ingreso ha sido registrado correctamente.")
            self.add_income_window.destroy()
            self.load_incomes_into_tree()
        else:
            messagebox.showerror("Error", "Por favor complete todos los campos.")

    def edit_and_save_income(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            income_id = values[0]
            amount = values[1].split()[0]
            entity = values[2]
            date = values[3]
            description = values[4]
            self.open_edit_income_window(income_id, amount, entity, date, description)
        else:
            messagebox.showerror("Error", "Por favor seleccione un ingreso.")

    def open_edit_income_window(self, income_id, amount, entity, date, description):
        self.edit_income_window = tk.Toplevel()
        self.edit_income_window.title("Editar Ingreso")
        self.edit_income_window.geometry("400x300")

        tk.Label(self.edit_income_window, text="Cantidad de Ingreso:").pack()
        self.edit_income_amount_entry = tk.Entry(self.edit_income_window)
        self.edit_income_amount_entry.insert(0, amount)
        self.edit_income_amount_entry.pack()

        tk.Label(self.edit_income_window, text="Entidad que realiza el ingreso:").pack()
        self.edit_income_entity_var = tk.StringVar(self.edit_income_window)
        entities = self.get_property_list() + ["Otros"]
        self.edit_income_entity_var.set(entity)
        self.edit_income_entity_menu = tk.OptionMenu(
            self.edit_income_window, self.edit_income_entity_var, *entities
        )
        self.edit_income_entity_menu.pack()

        tk.Label(self.edit_income_window, text="Fecha del Ingreso (DD/MM/YYYY):").pack()
        self.edit_income_date_entry = tk.Entry(self.edit_income_window)
        self.edit_income_date_entry.insert(0, date)
        self.edit_income_date_entry.pack()

        tk.Label(self.edit_income_window, text="Descripción:").pack()
        self.edit_income_description_entry = tk.Text(
            self.edit_income_window, height=5, width=30
        )
        self.edit_income_description_entry.insert(tk.END, description)
        self.edit_income_description_entry.pack()

        tk.Button(
            self.edit_income_window,
            text="Guardar Cambios",
            command=self.save_edited_income,
        ).pack(pady=10)

    def delete_income(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmation = messagebox.askyesno(
                "Confirmar Eliminación",
                "¿Está seguro de  eliminar este ingreso?",
            )
        if confirmation:
            income_id = self.tree.item(selected_item, "values")[0]
            self.db.delete_income(income_id)
            self.tree.delete(selected_item)
            messagebox.showinfo(
                "Ingreso Eliminado",
                "El ingreso ha sido eliminado correctamente.",
            )
        else:
            messagebox.showerror("Error", "Por favor seleccione un ingreso.")

    def save_edited_income(self):
        amount = self.edit_income_amount_entry.get()
        entity = self.edit_income_entity_var.get()
        date = self.edit_income_date_entry.get()
        description = self.edit_income_description_entry.get("1.0", "end-1c")

        try:
            formatted_date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Error", "Por favor ingrese una fecha válida (DD/MM/YYYY)."
            )
            return

        selected_item = self.tree.selection()
        if selected_item:
            income_id = self.tree.item(selected_item, "values")[0]
            if amount and entity and formatted_date:
                self.db.update_income(
                    income_id, amount, entity, formatted_date, description
                )
                messagebox.showinfo(
                    "Éxito", "El ingreso ha sido actualizado correctamente."
                )
                self.edit_income_window.destroy()
                self.load_incomes_into_tree()
            else:
                messagebox.showerror("Error", "Por favor complete todos los campos.")
        else:
            messagebox.showerror("Error", "Por favor seleccione un ingreso.")

    def load_incomes_into_tree(self):
        incomes = self.db.get_all_incomes()
        for income in self.tree.get_children():
            self.tree.delete(income)
        for income in incomes:
            income_with_euro = list(income)
            if "/" in income[3]:
                income_date = datetime.strptime(income[3], "%d/%m/%Y")
            else:
                income_date = datetime.strptime(income[3], "%Y-%m-%d")
            income_with_euro[3] = income_date.strftime("%d/%m/%Y")
            income_with_euro[1] = f"{income[1]} €"
            self.tree.insert("", tk.END, values=income_with_euro)

    def get_property_list(self):
        properties = self.db.get_all_properties()
        property_list = [property_data[1] for property_data in properties]
        return property_list

    def close_income_window(self):
        self.income_window.destroy()
