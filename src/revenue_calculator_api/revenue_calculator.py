
import json
import logging
from datetime import date
from typing import List, Tuple, NamedTuple, Dict

import sys, os
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from src.revenue_calculator_api.entities import ArbitrageProduct, Country, Currency, FeeInfo, ProductData
from src.revenue_calculator_api.revenue_calculator_api import handle_http_fetch, request_additional_product_info, request_fee_details, request_product_info, request_program_ids, parse_program_ids
from src.revenue_calculator_api.revenue_calculator_api import request_product_search_by_asin, request_fee_details_in_batch, parse_product_data, parse_fees_from_json_response


from config import tax_rate


logger = logging.getLogger("RevenueCalculator")

class ProductParams(NamedTuple):
    asin: str
    base_country: Country
    target_country: Country
    base_currency: Currency
    target_currency: Currency
    exchange_rate: float
    cost_of_shipment: float
        


# Now define your batch processing function
def get_arbitrage_product_in_batches(products: List[ProductParams], target_country: Country):
    """
    This function processes a batch of arbitrage products.
    
    :param products: List of tuples, where each tuple represents the parameters
                     (asin, base_country, target_country, base_currency, target_currency, exchange_rate, cost_of_shipment)
    :return: List of results for each arbitrage product.
    """
    base_results: Dict[str, ProductData] = dict()
    target_results: Dict[str, ProductData] = dict()
    product_data_lists: List[ProductData] = []
    
    for product in products:

        try:
             # Unpack the tuple into individual parameters
            asin, base_country, target_country, base_currency, target_currency, exchange_rate, cost_of_shipment = product
            
            target_result = request_product_search_by_asin(asin, target_country.value)
            maybe_product_data_target = parse_product_data(target_result)
            if maybe_product_data_target is not None:
                product_data_lists.append(maybe_product_data_base)
                target_results[asin] = maybe_product_data_target


            base_result = request_product_search_by_asin(asin, base_country.value)
            maybe_product_data_base =  parse_product_data(base_result)
            if maybe_product_data_target is not None:
                base_results[asin] = maybe_product_data_target
        except Exception as e:
            logger.error(f"get_arbitrage_product_in_batches: failed the search for the {product}")
    

    try:
        fee_response = request_fee_details_in_batch(product_data_lists, target_country.value)
        dict_of_fees: Dict[str, FeeInfo] = parse_fees_from_json_response(fee_response)
    except Exception as e:
        logger.error(f"Error while fetching fee details: {e}")
        return []
    
    # Prepare the final list of ArbitrageProduct objects
    arbitrage_products = []
    for asin in target_results:
        target_product_data = target_results[asin]
        base_product_data = base_results.get(asin)
        fee_info = dict_of_fees.get(asin)

        if not fee_info or not base_product_data:
            logger.warning(f"Missing data for ASIN: {asin}")
            continue

        # Create ArbitrageProduct
        arbitrage_product = ArbitrageProduct(
            product_data=target_product_data,
            target_currency=target_currency.value,
            base_currency=base_currency.value,
            exchange_rate=exchange_rate,
            target_country_code=target_country.value,
            source_country_code=base_country.value,
            cost_of_sourcing=base_product_data.price,
            cost_of_shipment=cost_of_shipment,
            fulfillment_fee=fee_info.fulfillment_fee,
            referral_fee=fee_info.referral_fee,
            tax_rate=tax_rate,  # Assuming a tax rate or fetch it from another source
            timestamp=date.today()
        )
        arbitrage_products.append(arbitrage_product)

    return arbitrage_products





def get_arbitrage_product(asin: str, base_country: Country, target_country: Country, base_currency: Currency, target_currency: Currency, exchange_rate: float, cost_of_shipment: float):

    base_info = json.loads(handle_http_fetch(request_product_info, asin, target_country.value).text)
    base_price_info = json.loads(handle_http_fetch(request_additional_product_info, asin, target_country.value).text)
    target_price_info = json.loads(handle_http_fetch(request_additional_product_info, asin, base_country.value).text)

    sale_price = base_price_info["data"]["price"]["amount"]
    sourcing_cost = target_price_info["data"]["price"]["amount"]

    gl_value = base_info["data"]["otherProducts"]["products"][0]["gl"]
    # program_ids_response = handle_http_fetch(request_program_ids, target_country.value)
    # program_ids = parse_program_ids(program_ids_response)
    # program_ids.pop()
    program_ids = [
    "Core#0",
    "MFN#1"
    ]
    fee_detail_response = json.loads(handle_http_fetch(request_fee_details, asin, target_country.value, target_currency.value,
                          gl_value, sale_price, program_ids).text)
    
    referral_fee = 0
    fulfillment_fee = 0

    try:
        core_fees = fee_detail_response["data"]["programFeeResultMap"].get("Core#0", {})
        
        # Extract the fulfillment fee
        fulfillment_fee_info = core_fees.get("otherFeeInfoMap", {}).get("FulfillmentFee", {})
        fulfillment_fee = fulfillment_fee_info.get("feeAmount", {}).get("amount", 0.0)
        
        # Extract the referral fee
        referral_fee_info = core_fees.get("otherFeeInfoMap", {}).get("ReferralFee", {})
        referral_fee = referral_fee_info.get("feeAmount", {}).get("amount", 0.0)
    except KeyError as e:
        logger.error(f"Failed extracting fees: asin= {asin}, error= {e}")
        referral_fee = fulfillment_fee = 0


    return ArbitrageProduct(
        asin= asin,
        target_currency= target_currency.value,
        base_currency= base_currency.value,
        exchange_rate= exchange_rate,  # 1 USD = 1.25 CAD
        target_country_code= base_country.value,
        source_country_code= base_country.value,
        sale_price= sale_price,  # Sale price in CAD
        cost_of_sourcing= sourcing_cost,  # Sourcing cost in USD
        cost_of_shipment= cost_of_shipment,  # Shipment cost in USD
        fulfillment_fee= fulfillment_fee,  # Fulfillment fee in CAD
        referral_fee= referral_fee,  # Referral fee in CAD
        tax_rate = tax_rate,  # 15% tax rate
        timestamp=date.today()  # Current date
    )



if __name__ == "__main__":

    from pprint import pprint as pp
    country_code = "CA"
    currency = "CAD"
    asin = "B08B2GFJ1C"
    
    # arbitrage_product = get_arbitrage_product(asin, base_country=Country.USA, target_country=Country.CANADA, base_currency=Currency.USD, target_currency=Currency.CAD, exchange_rate= 1.36 , cost_of_shipment = 2.5)
    # print(arbitrage_product)


    products = [
    ProductParams("B08B2GFJ1C", Country.USA, Country.CANADA, Currency.USD, Currency.CAD, 1.25, 5.0),
    ProductParams("B00DHHOQSA", Country.CANADA, Country.USA, Currency.CAD, Currency.USD, 0.8, 10.0),
    ]

    arbitrage_products = get_arbitrage_product_in_batches(products, Country.CANADA)

    # Print each arbitrage product
    for product in arbitrage_products:
        print(product)
    

    