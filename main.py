from codebase.parser.parse import *
from codebase.utils import create_excel


dict_us = parse_loop_us(file_path='./persistance/data')
dict_ca = parse_loop_ca(file_path='./persistance/data')

create_excel(dict_us, dict_ca)

print(dict_us, dict_ca)
