from typing import List
from pprint import pprint as pp
import requests
import json


default_headers ={
  'Pragma': 'no-cache',
  'Accept': 'application/json',
  'accept-encoding': 'gzip, deflate, br, zstd',
  'accept-language': "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
  'referer': 'https://sellercentral.amazon.com/hz/fba/profitabilitycalculator/index?lang=en_US',
  'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'sec-gpc': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',

}


def get_detail(asin: str, country_code: str):
    detail_url = f"https://sellercentral.amazon.com/rcpublic/productmatch?searchKey={asin}&countryCode={country_code}&locale=en-US"
    further_detail_url = f"https://sellercentral.amazon.com/rcpublic/getadditionalpronductinfo?asin={asin}&countryCode={country_code}&fnsku=&searchType=GENERAL&locale=en-US"

    detail = requests.get(detail_url, headers=default_headers)
    further_detail = requests.get(further_detail_url, headers=default_headers)
    print(detail.text)
    return detail, further_detail


def get_program_ids(country_code: str):
    url = f"https://sellercentral.amazon.com/rcpublic/getprograms?countryCode={country_code}&mSku=&locale=en-US"
    response = requests.get(url, headers=default_headers)
    data = json.loads(response.text)

    program_ids = []
    for program in data["programInfoList"]:
        name = program["name"]
        display_priority = program["displayPriority"]
        concatenated_value = f"{name}#{display_priority}"
        program_ids.append(concatenated_value)
    return program_ids


def get_fee_details(asin: str, country_code: str, currency: str, gl: str, price: float, program_ids: List[str]):

    fee_url = f"https://sellercentral.amazon.com/rcpublic/getfees?countryCode={country_code}&locale=en-US"
    payload = {"countryCode": country_code, "itemInfo": {"asin": asin, "glProductGroupName": gl, "packageLength": "0", "packageWidth": "0", "packageHeight": "0", "dimensionUnit": "", "packageWeight": "0",
                                                         "weightUnit": "", "afnPriceStr": str(price), "mfnPriceStr": str(price), "mfnShippingPriceStr": "0", "currency": currency, "isNewDefined": False}, "programIdList": program_ids, "programParamMap": {}}
    response = requests.post(fee_url, json=payload, headers=default_headers)
    return response

def get_info(asin):
    from pprint import pprint as pp
    country_code = "CA"
    currency = "CAD"
    detail, further_detail = get_detail(asin, country_code)

    parsed_detail = json.loads(detail.text)
    gl_value = parsed_detail["data"]["otherProducts"]["products"][0]["gl"]

    parsed_further_detail = json.loads(further_detail.text)
    price = parsed_further_detail["data"]["price"]["amount"]

    program_ids = get_program_ids(country_code)
    program_ids.pop()
    fee = get_fee_details(asin, country_code, currency,
                          gl_value, price, program_ids)

    pp(detail.text)
    print("--------")
    pp(further_detail.text)
    print("--------")
    pp(fee.text)


