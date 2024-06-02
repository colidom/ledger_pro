import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db.database import LadgerProDB
from utils.export_to_excel import export_to_excel


class ExpenseManagement:
    def __init__(self):
        self.db = LadgerProDB("ladger_pro.db")

    def open_expenses_view(self):
        self.expense_window = tk.Toplevel()
        self.expense_window.title("Registro de Gastos")
        self.expense_window.geometry("1000x400")

        top_button_frame = tk.Frame(self.expense_window)
        top_button_frame.pack(pady=10)

        tk.Button(
            top_button_frame,
            text="Añadir Gasto",
            width=20,
            command=self.open_add_expense_window,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            top_button_frame,
            text="Editar Gasto",
            width=20,
            command=self.edit_expense,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            top_button_frame,
            text="Eliminar Gasto",
            width=20,
            command=self.delete_expense,
        ).pack(side=tk.LEFT, padx=5)

        headers = ["Id", "Cantidad", "Fecha", "Descripción"]

        tk.Button(
            top_button_frame,
            text="Exportar a Excel",
            width=20,
            command=lambda: export_to_excel(
                self.db.get_all_expenses(), "gastos", headers
            ),
        ).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(
            self.expense_window,
            columns=("Id", "Cantidad", "Fecha", "Descripción"),
            show="headings",
        )
        self.tree.heading("Id", text="Id")
        self.tree.heading("Cantidad", text="Cantidad")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Descripción", text="Descripción")

        self.load_expenses_into_tree()

        self.tree.pack(fill="both", expand=True)

        tk.Button(
            self.expense_window, text="Cerrar", command=self.expense_window.destroy
        ).pack(side=tk.BOTTOM, pady=10)

    def open_add_expense_window(self):
        self.add_expense_window = tk.Toplevel()
        self.add_expense_window.title("Añadir Gasto")
        self.add_expense_window.geometry("400x300")

        tk.Label(self.add_expense_window, text="Cantidad de Gasto:").pack()
        self.expense_amount_entry = tk.Entry(self.add_expense_window)
        self.expense_amount_entry.pack()

        tk.Label(self.add_expense_window, text="Fecha del Gasto (DD/MM/YYYY):").pack()
        self.expense_date_entry = tk.Entry(self.add_expense_window)
        self.expense_date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.expense_date_entry.pack()

        tk.Label(self.add_expense_window, text="Descripción:").pack()
        self.expense_description_entry = tk.Text(
            self.add_expense_window, height=5, width=30
        )
        self.expense_description_entry.pack()

        tk.Button(
            self.add_expense_window, text="Guardar Gasto", command=self.save_expense
        ).pack(pady=10)

    def save_expense(self):
        amount = self.expense_amount_entry.get()
        date = self.expense_date_entry.get()
        description = self.expense_description_entry.get("1.0", "end-1c")

        try:
            formatted_date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Error", "Por favor ingrese una fecha válida (DD/MM/YYYY)."
            )
            return

        if amount and formatted_date and description:
            self.db.insert_expense(amount, formatted_date, description)
            messagebox.showinfo("Éxito", "El gasto ha sido registrado correctamente.")
            self.add_expense_window.destroy()
            self.load_expenses_into_tree()
        else:
            messagebox.showerror("Error", "Por favor complete todos los campos.")

    def edit_expense(self):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item, "values")
            expense_id = values[0]
            amount = values[1].split()[0]
            date = values[2]
            description = values[3]
            self.open_edit_expense_window(expense_id, amount, date, description)
        else:
            messagebox.showerror("Error", "Por favor seleccione un gasto.")

    def open_edit_expense_window(self, expense_id, amount, date, description):
        self.edit_expense_window = tk.Toplevel()
        self.edit_expense_window.title("Editar Gasto")
        self.edit_expense_window.geometry("400x300")

        tk.Label(self.edit_expense_window, text="Cantidad de Gasto:").pack()
        self.edit_expense_amount_entry = tk.Entry(self.edit_expense_window)
        self.edit_expense_amount_entry.insert(0, amount)
        self.edit_expense_amount_entry.pack()

        tk.Label(self.edit_expense_window, text="Fecha del Gasto (DD/MM/YYYY):").pack()
        self.edit_expense_date_entry = tk.Entry(self.edit_expense_window)
        self.edit_expense_date_entry.insert(0, date)
        self.edit_expense_date_entry.pack()

        tk.Label(self.edit_expense_window, text="Descripción:").pack()
        self.edit_expense_description_entry = tk.Text(
            self.edit_expense_window, height=5, width=30
        )
        self.edit_expense_description_entry.insert(tk.END, description)
        self.edit_expense_description_entry.pack()

        tk.Button(
            self.edit_expense_window,
            text="Guardar Cambios",
            command=self.save_edited_expense,
        ).pack(pady=10)

    def delete_expense(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmation = messagebox.askyesno(
                "Confirmar Eliminación",
                "¿Está seguro de que desea eliminar este gasto?",
            )
            if confirmation:
                expense_id = self.tree.item(selected_item, "values")[0]
                self.db.delete_expense(expense_id)
                self.tree.delete(selected_item)
                messagebox.showinfo(
                    "Gasto Eliminado",
                    "El gasto ha sido eliminado correctamente.",
                )
        else:
            messagebox.showerror("Error", "Por favor seleccione un gasto.")

    def save_edited_expense(self):
        amount = self.edit_expense_amount_entry.get()
        date = self.edit_expense_date_entry.get()
        description = self.edit_expense_description_entry.get("1.0", "end-1c")

        try:
            formatted_date = datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror(
                "Error", "Por favor ingrese una fecha válida (DD/MM/YYYY)."
            )
            return

        selected_item = self.tree.selection()
        if selected_item:
            expense_id = self.tree.item(selected_item, "values")[0]
            if amount and formatted_date and description:
                self.db.update_expense(expense_id, amount, formatted_date, description)
                messagebox.showinfo(
                    "Éxito", "El gasto ha sido actualizado correctamente."
                )
                self.edit_expense_window.destroy()
                self.load_expenses_into_tree()
            else:
                messagebox.showerror("Error", "Por favor complete todos los campos.")
        else:
            messagebox.showerror("Error", "Por favor seleccione un gasto.")

    def load_expenses_into_tree(self):
        expenses = self.db.get_all_expenses()
        for expense in self.tree.get_children():
            self.tree.delete(expense)
        for expense in expenses:
            # Convertir la fecha al formato DD/MM/YYYY
            formatted_date = datetime.strptime(expense[2], "%Y-%m-%d").strftime(
                "%d/%m/%Y"
            )
            self.tree.insert(
                "",
                tk.END,
                values=(expense[0], f"{expense[1]}€", formatted_date, expense[3]),
            )
