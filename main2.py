from codebase.parser.parse import *
from codebase.util.utils import *
from codebase.revenue_excel.clean_excel import * 
import threading

# Parse US Amazon with 
dict_us = parse_loop_us(file_path='./persistance/data/a.csv')
# Parse CA Amazon
dict_ca = parse_loop_ca(file_path='./persistance/data/a.csv')
# Create excel file for the US and CA prices
create_excel(dict_us, dict_ca, save_path='/Users/ardagulersoy/Desktop/Daily')

# Create excel file with revenue calculator. You can run this function separately since you are giving the price values through data_path, which contains the parameters of
# already parsed ASIN numbers
create_excel_ratio(data_path='/Users/ardagulersoy/Desktop/Daily/us-ca_excel_8543.xlsx',save_path='/Users/ardagulersoy/Desktop/Daily/')


