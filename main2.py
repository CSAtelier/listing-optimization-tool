from codebase.parser.parse import *
from codebase.util.utils import *
from codebase.revenue_excel.clean_excel import * 
import threading
from config import *


if kParse == True:
    parse_amazon(data_path=kDataDir,
                us_price_column=kUsPriceColumn ,us_sale_column=kUsSaleColumn,ca_price_column=kCaPriceColumn,ca_sale_column=kCaSaleColumn)

if kRevenueWithParse == True:
    revenue_calculator(data_path=kDataDir,
                    column=kRevenueColumn,
                    )


