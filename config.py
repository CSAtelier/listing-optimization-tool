from config_types import DeploymentEnvEnum, AsinProviderEnum
from collections import namedtuple
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


kDataPath: str = 'persistance/data/Serhat_list.xlsx'


kDeploymentEnvEnum: DeploymentEnvEnum = DeploymentEnvEnum.LOCAL
kIsHeadless: bool = False
kDelay: int = 6
kRevenueCrop: list= [226,266,624,787]
kStop: int = 1
# [226,266,624,787][624,787,226,266]

kParse: bool = True
kEnableHelium: bool = True
kEnablePrice: bool =  True

kRevenueWithParse: bool = False

kDataDir: str = "persistance/data/Serhat_list.xlsx"
kRevenueColumn: str = "J"
kUsPriceColumn: str = "K"
kCaPriceColumn: str = "L"
kUsSaleColumn: str = "M"
kCaSaleColumn: str = "N"
kAsınProviderEnum: AsinProviderEnum = AsinProviderEnum.REDIS



tax_rate = 0.15

RateLimit = namedtuple('RateLimit', [
    'revenue_calculator_wait_time_on_success',
    'revenue_calculator_wait_time_on_error',
    'max_try_count'
    ])

rate_limit = RateLimit(
    revenue_calculator_wait_time_on_success= 5000.0,
    revenue_calculator_wait_time_on_error=10000.0,
    max_try_count= 10
    )
