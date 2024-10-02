from src.parser.parse import *
from src.util.utils import *
from src.revenue_excel.clean_excel import * 
import threading
from config import *


if kParse == True:
    parse_amazon(data_path=kDataPath,
                us_price_column=kUsPriceColumn ,us_sale_column=kUsSaleColumn,ca_price_column=kCaPriceColumn,ca_sale_column=kCaSaleColumn,
                revenue_column=kRevenueColumn
                )

# if kRevenueWithParse == True:
#     revenue_calculator(data_path=kDataDir,
#                     column=kRevenueColumn,
#                     )


