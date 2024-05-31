import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from main_window import MainWindow

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()
