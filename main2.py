from codebase.parser.parse import *
from codebase.util.utils import *
from codebase.revenue_excel.clean_excel import * 
from matplotlib import pyplot as plt
import threading


# parse_amazon(data_path='/Users/ardagulersoy/Desktop/Daily/us-ca_excel_1783.xlsx',
#              us_price_column='B',us_sale_column='C',ca_price_column='D',ca_sale_column='E')

revenue_calculator(data_path='/Users/ardagulersoy/Downloads/siralanmis_ve_temizlenmis_parca3.xlsx.xlsx',
                   column='F'
                   )


