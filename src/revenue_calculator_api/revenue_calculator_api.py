from typing import List
from pprint import pprint as pp
import requests
import json
import logging
import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

logging.basicConfig(
    filename='app.log',       # Log file name
    level=logging.DEBUG,        # Logging level (INFO, DEBUG, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    filemode='a'               # Use 'w' to overwrite, 'a' to append
)

# from http_utilities import handle_http_fetch
from src.revenue_calculator_api.http_utilities import handle_http_fetch

default_headers = {
    'Host': 'sellercentral.amazon.com',
    'Pragma': "no-cache",
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'referer': 'https://sellercentral.amazon.com/hz/fba/profitabilitycalculator/index?lang=en',
    'sec-ch-ua': '"Chromium";v="128", "Not:A-Brand";v="24", "Brave";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}


def request_product_info(asin: str, country_code: str):
    detail_url = f"https://sellercentral.amazon.com/rcpublic/productmatch?searchKey={asin}&countryCode={country_code}&locale=en-US"
    detail = requests.get(detail_url, headers=default_headers)
    return detail

def request_additional_product_info(asin: str, country_code: str):
    further_detail_url = f"https://sellercentral.amazon.com/rcpublic/getadditionalpronductinfo?asin={asin}&countryCode={country_code}&fnsku=&searchType=GENERAL&locale=en-US"
    further_detail = requests.get(further_detail_url, headers=default_headers)
    return further_detail


def request_program_ids(country_code: str):
    url = f"https://sellercentral.amazon.com/rcpublic/getprograms?countryCode={country_code}&mSku=&locale=en-US"
    response = requests.get(url, headers=default_headers)
    return response
    
    
def parse_program_ids(response: requests.Response):
    data = json.loads(response.text)

    program_ids = []
    for program in data["programInfoList"]:
        name = program["name"]
        display_priority = program["displayPriority"]
        concatenated_value = f"{name}#{display_priority}"
        program_ids.append(concatenated_value)
    return program_ids

def request_fee_details(asin: str, country_code: str, currency: str, gl: str, price: float, program_ids: List[str]):

    fee_url = f"https://sellercentral.amazon.com/rcpublic/getfees?countryCode={country_code}&locale=en-US"
    payload = {"countryCode": country_code, "itemInfo": {"asin": asin, "glProductGroupName": gl, "packageLength": "0", "packageWidth": "0", "packageHeight": "0", "dimensionUnit": "", "packageWeight": "0",
                                                         "weightUnit": "", "afnPriceStr": 10.0, "mfnPriceStr": 10.0, "mfnShippingPriceStr": "0", "currency": currency, "isNewDefined": False}, "programIdList": program_ids, "programParamMap": {}}
    response = requests.post(fee_url, json=payload, headers=default_headers)
    return response


if __name__ == "__main__":

    from pprint import pprint as pp
    country_code = "CA"
    currency = "CAD"
    asin = "B08B2GFJ1C"
    
    detail_response= handle_http_fetch(request_product_info, asin, country_code)
    additional_info_response = handle_http_fetch(request_additional_product_info, asin, country_code)

    parsed_detail = json.loads(detail_response.text)
    gl_value = parsed_detail["data"]["otherProducts"]["products"][0]["gl"]
    parsed_further_detail = json.loads(additional_info_response.text)
    price = parsed_further_detail["data"]["price"]["amount"]

    program_ids_response = handle_http_fetch(request_program_ids, country_code)
    program_ids = parse_program_ids(program_ids_response)
    program_ids.pop()

    fee_detail_response = handle_http_fetch(request_fee_details, asin, country_code, currency,
                          gl_value, price, program_ids)

    pp(detail_response.text)
    print("--------")
    pp(additional_info_response.text)
    print("--------")
    pp(fee_detail_response.text)

    # response = get_fee_details("B08B2GFJ1C", "CA", "CAD", "gl_kitchen", 68.9, ["Core#0", "MFN#1"])

    # pp(response.text)
