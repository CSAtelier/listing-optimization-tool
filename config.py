from config_types import DeploymentEnvEnum, AsinProviderEnum
from collections import namedtuple


kDeploymentEnvEnum: DeploymentEnvEnum = DeploymentEnvEnum.LOCAL
kAsınProviderEnum: AsinProviderEnum = AsinProviderEnum.REDIS
kIsHeadless: bool = True



RateLimit = namedtuple('RateLimit', [
    'revenue_calculator_wait_time_on_success',
    'revenue_calculator_wait_time_on_error',
    'max_try_count'
    ])

rate_limit = RateLimit(
    revenue_calculator_wait_time_on_success= 2000.0,
    revenue_calculator_wait_time_on_error=5000.0,
    max_try_count= 10
    )
