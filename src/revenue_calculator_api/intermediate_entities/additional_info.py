from dataclasses import dataclass

@dataclass
class Price:
    amount: float
    currency: str


@dataclass
class Shipping:
    amount: float
    currency: str


@dataclass
class AdditionalInfoData:
    asin: str
    soldBy: str
    condition: str
    shipsFrom: str
    price: Price
    shipping: Shipping


@dataclass
class AdditionalInfoResponse:
    succeed: bool
    data: AdditionalInfoData
