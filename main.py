from src.parser.parse import *
from src.util.utils import *
from src.revenue_excel.clean_excel import * 
import threading
from config import *
import argparse  # Import argparse for command-line arguments



if kParse == True:
    # parse_amazon(data_path=kDataPath,
    #             us_price_column=kUsPriceColumn ,us_sale_column=kUsSaleColumn,ca_price_column=kCaPriceColumn,ca_sale_column=kCaSaleColumn,
    #             revenue_column=kRevenueColumn
    #             )
    # parser = argparse.ArgumentParser(description="Amazon Parser")
    # parser.add_argument('--data-path', type=str, help='Path to save parsed data')
    # parser.add_argument('--us-price-column', type=str, help='Column name for US price')
    # parser.add_argument('--us-sale-column', type=str, help='Column name for US sale')
    # parser.add_argument('--ca-price-column', type=str, help='Column name for CA price')
    # parser.add_argument('--ca-sale-column', type=str, help='Column name for CA sale')
    # parser.add_argument('--revenue-column', type=str, help='Column name for revenue')
    # parser.add_argument('--csv-path', type=str, help='Path to the CSV file containing ASINs')
    # parser.add_argument('--priority', type=int, help='Priority for pushing ASINs to Redis')

    # args = parser.parse_args()
    
    # parse_amazon(data_path=args.data_path, us_price_column=args.us_price_column, 
    #               us_sale_column=args.us_sale_column, ca_price_column=args.ca_price_column, 
    #               ca_sale_column=args.ca_sale_column, revenue_column=args.revenue_column, 
    #               csv_path=args.csv_path, priority=args.priority)
    parse_amazon(data_path=kDataPath,
                us_price_column=kUsPriceColumn ,us_sale_column=kUsSaleColumn,ca_price_column=kCaPriceColumn,ca_sale_column=kCaSaleColumn,
                revenue_column=kRevenueColumn
                )

# if kRevenueWithParse == True:
#     revenue_calculator(data_path=kDataDir,
#                     column=kRevenueColumn,
#                     )


