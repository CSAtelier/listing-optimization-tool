import openpyxl
import random
from src.dataset_loader import DatasetLoader
from currency_converter import CurrencyConverter

def asin_to_url(asin_list):
    url_list_us = []
    url_list_ca = []
    for asin in asin_list:
        url_list_us.append(f"https://www.amazon.com/dp/{asin}")
        url_list_ca.append(f"https://www.amazon.ca/dp/{asin}")
    return url_list_us, url_list_ca

def create_excel(price_dict_us, price_dict_ca,
                 data_path,us_price_column=None,ca_price_column=None,us_sale_column=None,ca_sale_column=None,revenue_column=None):

    wb = openpyxl.load_workbook(data_path)
    ws = wb.active
    # ws['A1'] = 'ASIN'
    # ws['B1'] = 'US Prices'
    # ws['C1'] = 'US Sale'
    # ws['D1'] = 'CA Prices'
    # ws['E1'] = 'CA Sale'
    # ws['F1'] = 'US/CA'
    # ws['G1'] = 'URL Amazon US'
    # ws['H1'] = 'URL Amazon CA'
    key_list = list(price_dict_us.keys())
    for i in range(len(key_list)):
        if us_price_column != None:
            ws[us_price_column+f'{i+2}'] = price_dict_us[key_list[i]][0]
        if ca_price_column != None:
            ws[ca_price_column+f'{i+2}']  = price_dict_ca[key_list[i]][0]
        if us_sale_column != None:
            ws[us_sale_column+f'{i+2}']  = float(price_dict_us[key_list[i]][1])
        if ca_sale_column != None:
            ws[ca_sale_column+f'{i+2}']  = float(price_dict_ca[key_list[i]][1])
        if revenue_column != None:
            c = CurrencyConverter()
            usd_cad = c.convert(1, 'USD', 'CAD') 
            usd_cad_price = (float(price_dict_us[key_list[i]][0])*1.06)*usd_cad
            shipping = 2.5*usd_cad
            cost = usd_cad_price + shipping
            print(usd_cad_price, shipping, cost,float(price_dict_ca[key_list[i]][2]))
            ws[revenue_column+f'{i+2}']  = ((float(price_dict_ca[key_list[i]][2])-cost)*100.0)/cost
        # ws[f'A{i+2}'] = key_list[i]
        # ws[f'B{i+2}'] = price_dict_us[key_list[i]][0]
        # ws[f'C{i+2}'] = float(price_dict_us[key_list[i]][1].replace(',', '.'))
        # ws[f'D{i+2}'] = price_dict_ca[key_list[i]][0]
        # ws[f'E{i+2}'] = float(price_dict_ca[key_list[i]][1].replace(',', '.'))
        # ws[f'G{i+2}'] = f"https://www.amazon.com/dp/{key_list[i]}"
        # ws[f'H{i+2}'] = f"https://www.amazon.ca/dp/{key_list[i]}"
        if price_dict_ca[key_list[i]] == 0 or price_dict_us[key_list[i]] == 0:
            ws[f'F{i+2}'] = 0
        else:
            try:
                ws[f'F{i+2}'] = price_dict_us[key_list[i]][0]/price_dict_ca[key_list[i]][0]
            except:
                ws[f'F{i+2}'] = 0
    # wb.save(save_path + '/us-ca_excel_'+str(random.randint(1,10000))+'.xlsx')
    wb.save(data_path)
    # file_name = save_path + '/us-ca_excel_'+str(random.randint(1,10000))+'.xlsx'

    

def extract_asin(url):
    parts = url.split('/')
    dp_index = parts.index('dp')
    asin = parts[dp_index + 1]
    return asin

    