from datetime import date
from typing import Optional
from enum import Enum
import json
from dataclasses import dataclass



class Country(Enum):
    """Docstring for MyEnum."""
    USA = "US"
    CANADA = "CA"

    def __str__(self):
        return self.value
    
class Currency(Enum):
    """Docstring for MyEnum."""
    USD = "USD"
    CAD = "CAD"

    def __str__(self):
        return self.value

@dataclass
class ProductData:
    asin: str
    gl: str
    title: str
    package_length: float
    package_width: float
    package_height: float
    dimension_unit: str
    package_weight: float
    weight_unit: str
    price: float
    currency: str
    brand_name: Optional[str]  # Brand Name of the product
    sales_rank: Optional[int]  # Sales rank
    sales_rank_context_name: Optional[str]  # Sales rank context (category)
    customer_reviews_count: Optional[int]  # Number of customer reviews
    customer_reviews_rating: Optional[str]  # Customer review rating (e.g., "4.4 out of 5 stars")
    customer_reviews_rating_value: Optional[float]  # Numerical value of the rating (e.g., 4.4)
    offer_count: Optional[int]  # Number of offers available

    def to_json(self) -> str:
        """
        Serialize the dataclass instance to a JSON string.
        """
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, data: str) -> 'ProductData':
        """
        Deserialize a JSON string to a dataclass instance.
        """
        return cls(**json.loads(data))
    
@dataclass
class FeeInfo:
    asin: str
    fulfillment_fee: float
    referral_fee: float

class ArbitrageProduct:
    def __init__(self, product_data: ProductData, target_currency: str, base_currency: str, exchange_rate: float,
                 target_country_code: str, source_country_code: str, cost_of_sourcing: float,
                 cost_of_shipment: float, fulfillment_fee: float, referral_fee: float, tax_rate: float,
                 timestamp: date):
        # Copy values from ProductData
        self._asin = product_data.asin
        self._title = product_data.title
        self._gl = product_data.gl
        self._package_length = product_data.package_length
        self._package_width = product_data.package_width
        self._package_height = product_data.package_height
        self._dimension_unit = product_data.dimension_unit
        self._package_weight = product_data.package_weight
        self._weight_unit = product_data.weight_unit
        self._brand_name = product_data.brand_name
        self._sales_rank = product_data.sales_rank
        self._sales_rank_context_name = product_data.sales_rank_context_name
        self._customer_reviews_count = product_data.customer_reviews_count
        self._customer_reviews_rating = product_data.customer_reviews_rating
        self._customer_reviews_rating_value = product_data.customer_reviews_rating_value
        self._offer_count = product_data.offer_count

        # Arbitrage specific values
        self._target_currency = target_currency
        self._base_currency = base_currency
        self._exchange_rate = exchange_rate  # Exchange rate from target currency to base currency
        self._target_country_code = target_country_code
        self._source_country_code = source_country_code
        self._cost_of_sourcing = cost_of_sourcing  # In base currency
        self._cost_of_shipment = cost_of_shipment  # In base currency
        self._fulfillment_fee = fulfillment_fee  # In target currency
        self._referral_fee = referral_fee  # In target currency
        self._tax_rate = tax_rate
        self._timestamp = timestamp

    @property
    def asin(self) -> str:
        return self._asin

    @property
    def sale_price(self) -> float:
        """
        Convert sale price from target currency to base currency using the exchange rate.
        """
        return self._cost_of_sourcing * self._exchange_rate

    @property
    def total_fees(self) -> float:
        """
        Calculate the total Amazon fees (fulfillment + referral) in base currency.
        """
        return (self._fulfillment_fee + self._referral_fee) / self._exchange_rate

    @property
    def cogs(self) -> float:
        """
        COGS (Cost of Goods Sold): Sourcing cost + shipment cost in base currency.
        """
        return self._cost_of_sourcing + self._cost_of_shipment

    @property
    def total_costs(self) -> float:
        """
        Total costs include COGS and Amazon fees, all in base currency.
        """
        return self.cogs + self.total_fees

    @property
    def net_profit_before_tax(self) -> float:
        """
        Net Profit Before Tax = Sale price (in base currency) - total costs (in base currency).
        """
        return self.sale_price - self.total_costs

    @property
    def tax_amount(self) -> float:
        """
        Calculate the tax amount on the net profit before tax in base currency.
        """
        return self.net_profit_before_tax * self._tax_rate

    @property
    def net_profit(self) -> float:
        """
        Net Profit = Net Profit Before Tax - tax amount (in base currency).
        """
        return self.net_profit_before_tax - self.tax_amount

    @property
    def net_profit_margin(self) -> float:
        """
        Net Profit Margin as a percentage of net profit before tax.
        """
        if self.net_profit_before_tax != 0:
            return (self.net_profit / self.total_costs) * 100
        return 0.0  # Avoid division by zero

    def __str__(self):
        """
        Custom string representation for easier reading.
        """
        return (f"ASIN: {self._asin}\n"
                f"Title: {self._title}\n"
                f"Sale Price: {self.sale_price:.2f} {self._base_currency}\n"
                f"Brand: {self._brand_name or 'N/A'}\n"
                f"Sales Rank: {self._sales_rank} ({self._sales_rank_context_name})\n"
                f"Reviews: {self._customer_reviews_count}, Rating: {self._customer_reviews_rating_value:.1f} stars\n"
                f"Cost of Sourcing: {self._cost_of_sourcing:.2f} {self._base_currency}\n"
                f"Cost of Shipment: {self._cost_of_shipment:.2f} {self._base_currency}\n"
                f"Amazon Fees: {self.total_fees:.2f} {self._base_currency}\n"
                f"COGS: {self.cogs:.2f} {self._base_currency}\n"
                f"Total Costs: {self.total_costs:.2f} {self._base_currency}\n"
                f"Net Profit Before Tax: {self.net_profit_before_tax:.2f} {self._base_currency}\n"
                f"Tax Amount: {self.tax_amount:.2f} {self._base_currency}\n"
                f"Net Profit: {self.net_profit:.2f} {self._base_currency}\n"
                f"Net Profit Margin: {self.net_profit_margin:.2f}%\n"
                f"Timestamp: {self._timestamp}")


if __name__ == "__main__":
    product_data = ProductData(
        asin="B08B2GFJ1C",
        gl="gl_home",
        title="Cedar Oil - Giles and Kendall - Restores the Original Aroma of Cedar Wood, 8 oz",
        package_length=10.0,
        package_width=5.0,
        package_height=5.0,
        dimension_unit="centimeters",
        package_weight=0.5,
        weight_unit="kilograms",
        price=100.0,
        currency="CAD",
        brand_name="Giles and Kendall",
        sales_rank=10000,
        sales_rank_context_name="Home Improvement",
        customer_reviews_count=200,
        customer_reviews_rating="4.5 out of 5 stars",
        customer_reviews_rating_value=4.5,
        offer_count=10
    )

    arbitrage_product = ArbitrageProduct(
        product_data=product_data,
        target_currency="CAD",
        base_currency="USD",
        exchange_rate=1.25,
        target_country_code="CA",
        source_country_code="US",
        cost_of_sourcing=40.0,
        cost_of_shipment=10.0,
        fulfillment_fee=10.0,
        referral_fee=5.0,
        tax_rate=0.15,
        timestamp=date.today()
    )

    print(arbitrage_product)