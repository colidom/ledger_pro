from tkinter import filedialog
from openpyxl import Workbook


def export_to_excel(data, default_name, headers):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        initialfile=default_name,
        filetypes=[("Excel files", "*.xlsx")],
    )
    if file_path:
        wb = Workbook()
        ws = wb.active
        ws.append(headers)  # Les pasamos las cabeceras al fichero
        for row in data:
            ws.append(row)
        wb.save(file_path)
