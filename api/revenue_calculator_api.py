import requests
from requests.exceptions import RequestException
import json
from typing import List, Dict, Any
import logging

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


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_request(url: str, method: str = 'GET', headers: Dict[str, str] = None, payload: Dict[str, Any] = None) -> requests.Response:
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, json=payload, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        response.raise_for_status()
        return response
    except RequestException as e:
        logger.error(f"Request failed: {e}")
        logger.debug(f"Request details: URL={url}, Method={method}, Headers={headers}, Payload={payload}")
        raise

def get_detail(asin: str, country_code: str) -> Dict[str, Any]:
    detail_url = f"https://sellercentral.amazon.com/rcpublic/productmatch?searchKey={asin}&countryCode={country_code}&locale=en-US"
    further_detail_url = f"https://sellercentral.amazon.com/rcpublic/getadditionalpronductinfo?asin={asin}&countryCode={country_code}&fnsku=&searchType=GENERAL&locale=en-US"

    detail = make_request(detail_url, headers=default_headers)
    further_detail = make_request(further_detail_url, headers=default_headers)
    
    return {
        'detail': detail.json(),
        'further_detail': further_detail.json()
    }

def get_program_ids(country_code: str) -> List[str]:
    url = f"https://sellercentral.amazon.com/rcpublic/getprograms?countryCode={country_code}&mSku=&locale=en-US"
    response = make_request(url, headers=default_headers)
    data = response.json()

    return [f"{program['name']}#{program['displayPriority']}" for program in data["programInfoList"]]

def get_fee_details(asin: str, country_code: str, currency: str, gl: str, price: float, program_ids: List[str]) -> Dict[str, Any]:
    fee_url = f"https://sellercentral.amazon.com/rcpublic/getfees?countryCode={country_code}&locale=en-US"
    payload = {
        "countryCode": country_code,
        "itemInfo": {
            "asin": asin,
            "glProductGroupName": gl,
            "packageLength": "0",
            "packageWidth": "0",
            "packageHeight": "0",
            "dimensionUnit": "",
            "packageWeight": "0",
            "weightUnit": "",
            "afnPriceStr": str(price),
            "mfnPriceStr": str(price),
            "mfnShippingPriceStr": "0",
            "currency": currency,
            "isNewDefined": False
        },
        "programIdList": program_ids,
        "programParamMap": {}
    }
    response = make_request(fee_url, method='POST', json=payload, headers=default_headers)
    return response.json()

if __name__ == "__main__":
    try:
        country_code = "CA"
        currency = "CAD"
        asin = "B08B2GFJ1C"
        
        detail_info = get_detail(asin, country_code)
        gl_value = detail_info['detail']["data"]["otherProducts"]["products"][0]["gl"]
        price = detail_info['further_detail']["data"]["price"]["amount"]

        program_ids = get_program_ids(country_code)
        program_ids.pop()  # Remove the last item as in the original code
        
        fee_details = get_fee_details(asin, country_code, currency, gl_value, price, program_ids)
        
        logger.info("Detail information:")
        logger.info(json.dumps(detail_info['detail'], indent=2))
        logger.info("Further detail information:")
        logger.info(json.dumps(detail_info['further_detail'], indent=2))
        logger.info("Fee details:")
        logger.info(json.dumps(fee_details, indent=2))
    
    except Exception as e:
        logger.exception("An error occurred during script execution")