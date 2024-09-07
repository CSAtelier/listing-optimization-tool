from tkinter import filedialog
from ..parser.parse import *
from ..util.utils import create_excel
from ..revenue_excel.clean_excel import create_excel_ratio

def select_data_folder():
    global selected_folder_path
    folder_path = filedialog.askopenfilename()
    if folder_path:
        selected_folder_path = folder_path
        print("Selected data folder:", selected_folder_path)
    

def select_save_folder():
    global selected_save_folder_path
    folder_save_path = filedialog.askdirectory()
    if folder_save_path:
        selected_save_folder_path = folder_save_path
        print("Selected save folder:", selected_save_folder_path)


def run_parsing():
    global selected_folder_path
    if selected_folder_path:
        print("Using selected folder in another function:", selected_folder_path)
        dict_us = parse_loop_us(file_path=selected_folder_path)
        dict_ca = parse_loop_ca(file_path=selected_folder_path)
        create_excel(price_dict_ca=dict_ca, price_dict_us=dict_us, save_path=selected_save_folder_path)
        print(dict_us, dict_ca)
    else:
        print("Please select a folder first.")


def get_ratio():
    global selected_folder_path
    if selected_folder_path:
        print("Using selected folder in another function:", selected_folder_path)
        create_excel_ratio(data_path=selected_folder_path, save_path=selected_save_folder_path)
    else:
        print("Please select a folder first.")