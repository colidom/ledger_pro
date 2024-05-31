# export_to_excel.py

from tkinter import filedialog
from openpyxl import Workbook


def export_to_excel(data):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        initialfile="usuarios",
        filetypes=[("Excel files", "*.xlsx")],
    )
    if file_path:
        wb = Workbook()
        ws = wb.active
        ws.append(["Id", "Vivienda", "Nombre", "Apellidos", "Teléfono"])
        for row in data:
            ws.append(row)
        wb.save(file_path)
