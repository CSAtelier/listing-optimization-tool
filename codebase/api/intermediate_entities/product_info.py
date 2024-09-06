from dataclasses import dataclass
from typing import List


@dataclass
class Product:
    asin: str
    imageUrl: str
    gl: str
    title: str
    price: float


@dataclass
class MyProducts:
    totalProductCount: int
    currentPage: int
    products: List[Product]


@dataclass
class OtherProducts:
    totalProductCount: int
    currentPage: int
    products: List[Product]


@dataclass
class ProductInfoData:
    countryCode: str
    merchantId: str
    searchKey: str
    myProducts: MyProducts
    otherProducts: OtherProducts


@dataclass
class ProductInfoResponse:
    succeed: bool
    data: ProductInfoData
