from datetime import date
from enum import Enum


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
    

class ArbitrageProduct:
    def __init__(self, asin: str, target_currency: str, base_currency: str, exchange_rate: float,
                 target_country_code: str, source_country_code: str, sale_price: float,
                 cost_of_sourcing: float, cost_of_shipment: float, fulfillment_fee: float,
                 referral_fee: float, tax_rate: float, timestamp: date):
        self._asin = asin
        self._target_currency = target_currency
        self._base_currency = base_currency
        self._exchange_rate = exchange_rate  # Exchange rate from target currency to base currency
        self._target_country_code = target_country_code
        self._source_country_code = source_country_code
        self._sale_price = sale_price  # In target currency
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
        return self._sale_price / self._exchange_rate

    @property
    def fulfillment_fee(self) -> float:
        """
        Convert fulfillment fee from target currency to base currency using the exchange rate.
        """
        return self._fulfillment_fee / self._exchange_rate

    @property
    def referral_fee(self) -> float:
        """
        Convert referral fee from target currency to base currency using the exchange rate.
        """
        return self._referral_fee / self._exchange_rate

    @property
    def total_fees(self) -> float:
        """
        Calculate the total Amazon fees (fulfillment + referral) in base currency.
        """
        return self.fulfillment_fee + self.referral_fee

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

    def currency(self):
        """
        Display the target and base currencies along with the exchange rate.
        """
        return f"Target Currency: {self._target_currency}, Base Currency: {self._base_currency}, Exchange Rate: {self._exchange_rate}"

    def __str__(self):
        """
        Custom string representation for easier reading.
        """
        return (f"ASIN: {self._asin}\n"
                f"Sale Price: {self.sale_price:.2f} {self._base_currency}\n"
                f"Cost of Sourcing: {self._cost_of_sourcing:.2f} {self._base_currency}\n"
                f"Cost of Shipment: {self._cost_of_shipment:.2f} {self._base_currency}\n"
                f"Amazon Fees: {self.total_fees:.2f} {self._base_currency}\n"
                f"COGS: {self.cogs:.2f} {self._base_currency}\n"
                f"Total Costs: {self.total_costs:.2f} {self._base_currency}\n"
                f"Net Profit Before Tax: {self.net_profit_before_tax:.2f} {self._base_currency}\n"
                f"Tax Amount: {self.tax_amount:.2f} {self._base_currency}\n"
                f"Net Profit: {self.net_profit:.2f} {self._base_currency}\n"
                f"Net Profit Margin: {self.net_profit_margin:.2f}%\n"
                f"Timestamp: {self._timestamp}\n"
                f"{self.currency()}")

if __name__ == "__main__":
    arbitrage_product = ArbitrageProduct(
        asin="B08B2GFJ1C",
        target_currency="CAD",
        base_currency="USD",
        exchange_rate=1.25,  # 1 USD = 1.25 CAD
        target_country_code="CA",
        source_country_code="US",
        sale_price=100.0,  # Sale price in CAD
        cost_of_sourcing=40.0,  # Sourcing cost in USD
        cost_of_shipment=10.0,  # Shipment cost in USD
        fulfillment_fee=10.0,  # Fulfillment fee in CAD
        referral_fee=5.0,  # Referral fee in CAD
        tax_rate=0.15,  # 15% tax rate
        timestamp=date.today()  # Current date
    )

    # Accessing computed properties:
    print(arbitrage_product)
