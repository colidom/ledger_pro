import tkinter as tk
from tkinter import ttk, messagebox
from database import LadgerProDB
from export_to_excel import export_to_excel


class PropertyManagement:
    def __init__(self):
        self.db = LadgerProDB("ladger_pro.db")

    def open_view_properties(self):
        messagebox.showinfo("Viviendas", "Aquí se abrirá el registro de Vivienda.")
