from codebase.parser.parse import *
from codebase.util.utils import *
from codebase.revenue_excel.clean_excel import * ß
import threading

dict_us = parse_loop_us(file_path='./persistance/data/a.csv')
# dict_ca = parse_loop_ca(file_path='./persistance/data/a.csv')

# create_excel_ratio(data_path='/Users/ardagulersoy/Desktop/Daily/us-ca_excel_3039.xlsx',save_path='/Users/ardagulersoy/Desktop/Daily/')
# create_excel(dict_us, dict_ca, save_path='a')
print(dict_us)



