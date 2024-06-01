import tkinter as tk
from tkinter import ttk, messagebox
from database import UserDatabase
from export_to_excel import export_to_excel


class HousingManagement:
    def __init__(self):
        self.db = UserDatabase("users.db")

    def open_view_housing(self):
        messagebox.showinfo("Viviendas", "Aquí se abrirá el registro de Vivienda.")
