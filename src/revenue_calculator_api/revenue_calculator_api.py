from typing import List, Any, Optional, Dict
from pprint import pprint as pp
import requests
import json
import logging
import sys
import os

from dataclasses import dataclass, asdict

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
from src.revenue_calculator_api.entities import ProductData, FeeInfo


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

def request_batch_fees(country_code: str):
    url = f"https://sellercentral.amazon.com/rcpublic/getbatchfees?countryCode={country_code}&locale=en-US"
    response = requests.post(url, headers=default_headers)
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



def request_product_search_by_asin(asin: str, country_code: str):

    url = f"https://sellercentral.amazon.com/rcpublic/searchproduct?countryCode={country_code}&locale=en-US"

    payload = {
        "keywords":asin,
        "countryCode":country_code,
        "searchType":"GENERAL",
        "pageOffset":1
    }

    response = requests.post(url, json=payload, headers=default_headers)

    return response



def request_fee_details_in_batch(list_of_products: List[ProductData], country_code: str):
    """
    Create a fee estimation request payload in batch for a list of ProductData.
    """
    fee_estimation_payload = {
        "feeEstimationRequestList": []
    }

    for product in list_of_products:
        product_payload = {
            "countryCode": "CA",  # Hardcoded country, you can modify as needed
            "itemInfo": {
                "asin": product.asin,
                "glProductGroupName": product.gl,
                "tRexId": "-1",  # Placeholder value
                "title": product.title,
                "packageLength": str(product.package_length),
                "packageWidth": str(product.package_width),
                "packageHeight": str(product.package_height),
                "dimensionUnit": product.dimension_unit,
                "packageWeight": str(product.package_weight),
                "weightUnit": product.weight_unit,
                "afnPriceStr": str(product.price),
                "mfnPriceStr": str(product.price),
                "mfnShippingPriceStr": "0",  # Default value
                "currency": product.currency,
                "isNewDefined": False  # Default value
            },
            "programIdList": ["0"],  # Default value
            "programParamMap": {
                "0": {
                    "program": "Core",
                    "inventoryPlace": "CA",  # Hardcoded country
                    "marketplace": "CA",  # Hardcoded marketplace
                    "commonInput": {
                        "averageInventoryUnitsStored": 1,  # Default value
                        "costOfGoodsSold": 0,  # Default value
                        "estimatedMonthlyUnitsSold": 1,  # Default value
                        "estimatesSales": 1,  # Default value
                        "miscellaneousCost": 0  # Default value
                    },
                    "nonMFNProgramInput": {
                        "isBubblewrapChosen": False,  # Default value
                        "isFBAInboundConvenienceChosen": False,  # Default value
                        "isLabelingChosen": False,  # Default value
                        "isOpaqueBaggingChosen": False,  # Default value
                        "isPolybaggingChosen": False,  # Default value
                        "isTapingChosen": False,  # Default value
                        "shippingToAmazon": 0  # Default value
                    }
                }
            },
            "isNonPeakSelected": True  # Default value
        }
        fee_estimation_payload["feeEstimationRequestList"].append(product_payload)
    
    url = f"https://sellercentral.amazon.com/rcpublic/getbatchfees?countryCode={country_code}&locale=en-US"
    response = requests.post(url, json=fee_estimation_payload, headers=default_headers)

    return response


def parse_product_data(response: requests.Response) -> Optional[ProductData]:
    """
    Parse the JSON response and populate a ProductData instance.

    :param response: requests.Response object returned by the API call
    :return: ProductData object or None if parsing fails
    """
    try:
        # Parse the JSON response
        data = response.json()

        # Check if the request was successful
        if data.get("succeed") and data["data"]["totalProductCount"] > 0:
            product_info = data["data"]["products"][0]

            # Extract relevant fields
            asin = product_info["asin"]
            gl = product_info["gl"]
            title = product_info["title"]
            package_length = product_info["length"]
            package_width = product_info["width"]
            package_height = product_info["height"]
            dimension_unit = product_info["dimensionUnit"]
            package_weight = product_info["weight"]
            weight_unit = product_info["weightUnit"]
            price = product_info["price"]
            currency = product_info["currency"]
            brand_name = product_info.get("brandName")
            sales_rank = product_info.get("salesRank")
            sales_rank_context_name = product_info.get("salesRankContextName")
            customer_reviews_count = product_info.get("customerReviewsCount")
            customer_reviews_rating = product_info.get("customerReviewsRating")
            customer_reviews_rating_value = product_info.get("customerReviewsRatingValue")
            offer_count = product_info.get("offerCount")

            # Create and return the ProductData instance
            return ProductData(
                asin=asin,
                gl=gl,
                title=title,
                package_length=package_length,
                package_width=package_width,
                package_height=package_height,
                dimension_unit=dimension_unit,
                package_weight=package_weight,
                weight_unit=weight_unit,
                price=price,
                currency=currency,
                brand_name=brand_name,
                sales_rank=sales_rank,
                sales_rank_context_name=sales_rank_context_name,
                customer_reviews_count=customer_reviews_count,
                customer_reviews_rating=customer_reviews_rating,
                customer_reviews_rating_value=customer_reviews_rating_value,
                offer_count=offer_count
            )
        else:
            print("Failed to retrieve product data or no products found.")
            return None

    except (KeyError, ValueError) as e:
        print(f"Error parsing the response: {e}")
        return None


def extract_fees_from_report(report) -> Optional[FeeInfo]:
    """
    Extract fulfillment fee and referral fee from a product report row and return it as a FeeDetails object.
    
    Args:
        report (list): The row data in the 'batchFeeEstimationCsvReport'.
    
    Returns:
        FeeDetails: A dataclass containing the ASIN, fulfillment fee, and referral fee.
        Returns None if the row does not contain valid data.
    """
    asin = report[2]
    
    try:
        fulfillment_fee = float(report[19])  # Convert fulfillment fee to float
        referral_fee = float(report[21])     # Convert referral fee to float
    except (ValueError, TypeError):
        # Handle cases where the fees are not valid numbers
        return None

    return FeeInfo(
        asin=asin,
        fulfillment_fee=fulfillment_fee,
        referral_fee=referral_fee
    )

def parse_fees_from_json_response(json_response)-> Dict[str, FeeInfo]:
    """
    Parse the JSON response and extract fees for all products as FeeDetails objects.
    
    Args:
        json_response (dict): JSON response containing the fee report.
    
    Returns:
        list: A list of FeeDetails objects for each product.
    """
    fee_report = json_response.get('data', {}).get('batchFeeEstimationCsvReport', [])
    
    fees: Dict[str, FeeInfo] = dict()
    for row in fee_report[2:]:  # Start at index 2 to skip headers
        if row[2]:  # Only process rows with valid ASINs
            fee_data = extract_fees_from_report(row)
            if fee_data:
                fees[fee_data.asin] = fee_data
    
    return fees


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
