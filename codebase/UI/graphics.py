from ..UI.backend import *
from tkinter import *
import tkinter as tk

def run_UI():
    root = tk.Tk()
    root.title("Tradify")

    root.geometry("400x400")  

    label = tk.Label(root, text="List Optimization Tool")
    label.pack(pady=10)
    print("UI activated")
    select_button = tk.Button(root, text="Select Save Folder", command=select_save_folder)
    select_button.pack(pady=10)

    select_button = tk.Button(root, text="Select Excel File", command=select_data_folder)
    select_button.pack(pady=10)

    use_button = tk.Button(root, text="Run Parser", command=run_parsing)
    use_button.pack(pady=10)

    clean_button = tk.Button(root, text="Get Ratio", command=get_ratio)
    clean_button.pack(pady=10)

    root.mainloop()