from codebase.parser.parse import *
from codebase.util.utils import *
from codebase.revenue_excel.clean_excel import * 
from matplotlib import pyplot as plt
import concurrent.futures
import threading

# Parse US Amazon with 
# dict_us = parse_loop_us(file_path='./persistance/data/a.csv')
# Parse CA Amazon
# dict_ca = parse_loop_ca(file_path='./persistance/data/a.csv')

def main():
    thread1 = threading.Thread(target=parse_loop_us(file_path='./persistance/data/a.csv'))
    thread2 = threading.Thread(target=parse_loop_ca(file_path='./persistance/data/a.csv'))
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    print("Both parsers have finished execution.")

if __name__ == "__main__":
    main()



