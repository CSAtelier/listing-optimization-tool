from dataclasses import dataclass

@dataclass
class FeeDetail:
    asin: str
    currency: str
    countryCode : str
    price: float
    total_fee : float
    fullfillment_fee: float
    referral_fee: float


