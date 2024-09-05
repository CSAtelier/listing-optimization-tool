import requests
from typing import Callable
import logging
import time

from config import rate_limit
from constants import MILISECONDS_IN_A_SECOND

logger = logging.getLogger(__name__)

HttpResponseCallable = Callable[..., requests.Response]


def handle_http_fetch(fetch_callback: HttpResponseCallable, *args, **kwargs):
    
    for trial_no in range(rate_limit.max_try_count):
        
        response = fetch_callback(*args, **kwargs)

        if response.status_code < 300:
            logger.info(f"Received HTTP OK trial[{trial_no}]: url = {response.url}")
            time.sleep(rate_limit.revenue_calculator_wait_time_on_success / MILISECONDS_IN_A_SECOND)
            return response
        
        logger.error(f"Failed trial[{trial_no}]: url = {response.url}, code = {response.status_code}")

        if response.status_code == 429:
            logger.error(f"Received too many requests: url = {response.url}")
        
        time.sleep(rate_limit.revenue_calculator_wait_time_on_error / MILISECONDS_IN_A_SECOND)
    
    return None