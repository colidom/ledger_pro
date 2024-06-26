import tkinter as tk
from tkinter import ttk, messagebox
from db.database import LadgerProDB
from utils.export_to_excel import export_to_excel


class DebtsManagement:
    def __init__(self):
        self.db = LadgerProDB("ladger_pro.db")

    def open_debts_view(self):
        properties_with_debt = self.db.get_properties_with_debt()
        debt_list_window = tk.Toplevel()
        debt_list_window.title("Deudas de Vecinos")
        debt_list_window.geometry("800x300")

        headers = ["Id", "Vivienda", "Vecino", "Deuda Total", "Pagos Pendientes"]
        # Botón para exportar a Excel
        tk.Button(
            debt_list_window,
            text="Exportar a excel",
            width=20,
            command=lambda: export_to_excel(
                properties_with_debt, "deudas_vecinos", headers
            ),  # Llama a la función export_to_excel con los datos
        ).pack(
            side=tk.TOP, padx=5, pady=5
        )  # Agregamos pady=5 para espaciar

        self.tree = ttk.Treeview(
            debt_list_window,
            columns=("Id", "Vivienda", "Vecino", "Deuda Total", "Pagos Pendientes"),
            show="headings",
        )
        self.tree.heading("Id", text="Id")
        self.tree.heading("Vivienda", text="Vivienda")
        self.tree.heading("Vecino", text="Vecino")
        self.tree.heading("Deuda Total", text="Deuda Total")
        self.tree.heading("Pagos Pendientes", text="Pagos Pendientes")

        for debt_data in properties_with_debt:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    debt_data[0],
                    debt_data[1],
                    debt_data[2],
                    f"{debt_data[3]}€",
                    debt_data[4],
                ),
            )

        self.tree.pack(fill="both", expand=True)

        # Botón para cerrar la ventana
        tk.Button(
            debt_list_window,
            text="Cerrar",
            command=debt_list_window.destroy,
        ).pack(side=tk.BOTTOM, padx=5)
