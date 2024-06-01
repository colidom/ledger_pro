import tkinter as tk
from tkinter import ttk, messagebox
from database import LadgerProDB
from export_to_excel import export_to_excel


class DebtsManagement:
    def __init__(self):
        self.db = LadgerProDB("ladger_pro.db")

    def open_debts_view(self):
        properties_with_debt = self.db.get_properties_with_debt()
        debt_list_window = tk.Toplevel()
        debt_list_window.title("Deudas de Vecinos")
        debt_list_window.geometry("800x300")

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
            self.tree.insert("", tk.END, values=debt_data)

        self.tree.pack(fill="both", expand=True)
