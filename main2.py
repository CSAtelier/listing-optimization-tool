from codebase.parser.parse import *
from codebase.util.utils import *
from codebase.revenue_excel.clean_excel import * 
from matplotlib import pyplot as plt
import threading

# dict_us = parse_loop_us(file_path='./persistance/data/a.csv')
# dict_ca = parse_loop_ca(file_path='./persistance/data/a.csv')

# create_excel_ratio(data_path='/Users/ardagulersoy/Desktop/Daily/us-ca_excel_3039.xlsx',save_path='/Users/ardagulersoy/Desktop/Daily/')
# # create_excel(dict_us, dict_ca, save_path='a')
# # print(usd_ca)

import threading
from codebase.parser.parse import parse_loop_us, parse_loop_ca

def parse_us_and_ca(file_path):
    # Create threads for parsing US and CA data
    thread_us = threading.Thread(target=parse_loop_us, kwargs={'file_path': file_path})
    thread_ca = threading.Thread(target=parse_loop_ca, kwargs={'file_path': file_path})
    
    # Start the threads
    thread_us.start()
    thread_ca.start()
    
    # Wait for both threads to finish
    thread_us.join()
    thread_ca.join()

if __name__ == "__main__":
    file_path = './persistance/data/a.csv'
    parse_us_and_ca(file_path)
    

