from codebase.utils import *
from codebase.dataset_loader import DatasetLoader
from codebase.parser.parse import *

loader = DatasetLoader()
asin_list = loader.load_dataset()
url_list = asin_to_url(asin_list)
excel_dict_us = dict()
excel_dict_ca = dict()
index = 0
for url in url_list[:2]:
    index = index + 1
    asin = extract_asin(url)
    if 'amazon.com' in url:
        country = 'us'
        price = parse_asin_us(url)  
        price = 0
        excel_dict_us[asin] = price
    elif 'amazon.ca' in url:
        country = 'ca'
        try: 
            price = parse_asin_ca(url)
        except:
            price = 0
        excel_dict_ca[asin] = price
    # wb = create_excel(price=price, country=country, asin=asin, index=index)
    # excel_dict_ca.clear()
    # excel_dict_us.clear()
# wb.save('output/us-ca_excel_'+str(random.randint(1,10000))+'.xlsx')

print(excel_dict_ca)
print(excel_dict_us)