from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ..parsing_methods import *
from src.util.utils import *
from src.dataset_loader import DatasetLoader
import subprocess
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from config import kDeploymentEnvEnum, kDelay, kIsHeadless, kEnablePrice, kEnableHelium
import json
import sys
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    
    if kIsHeadless:
        options.add_argument("--headless=new")
    
    if kEnableHelium:
        extension_path = "extensions/oay"
        options.add_extension('extensions/helium10_extension.crx')
        options.add_argument(f"--load-extension={extension_path}") 
    
    driver = webdriver.Chrome(options=options)
    return driver

def capture_network_traffic(driver):
    for request in driver.requests:
        if request.response:
            request_url = request.url
            response_status = request.response.status_code

def open_browser_us(driver, url, flag=False):
    driver.get(url)
    capture_network_traffic(driver)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    if flag:
        try:
            captcha_handle(soup, driver)
            change_location_us(driver)
        except Exception:
            pass
    return driver

def open_browser_ca(driver, url, flag=False):
    driver.get(url)
    capture_network_traffic(driver)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    if flag:
        try:
            captcha_handle(soup, driver)
        except Exception:
            pass
    return driver

def parse_asin_us(driver):
    try:   
        html_updated = driver.page_source
        soup_updated = BeautifulSoup(html_updated, features="lxml")
        price, sale, revenue = get_price_us(soup_updated, driver=driver)
        return price, sale, revenue
    except Exception as e:
        print(f"Error parsing US ASIN: {e}")
        return 0, 'N/A', 0  # Return default values


def parse_asin_ca(driver):
    try:
        html_updated = driver.page_source
        soup_updated = BeautifulSoup(html_updated, features="lxml")
        price, sale, revenue = get_price_ca(soup_updated, driver=driver)
        return price, sale, revenue
    except ValueError:
        return 0, 'N/A', 0  # Return default values

def parse_loop_us(driver, url, flag=False):
    price_dict = {}
    driver = open_browser_us(driver, url='https://www.amazon.com/', flag=flag)
    asin = extract_asin(url[0])
    driver.get(url[0])
    time.sleep(kDelay)
    
    price, unit_sale, revenue = parse_asin_us(driver)
    if kEnablePrice == False:
        price = 0
    if unit_sale == 'N/A':
        unit_sale = 0

    price_dict[asin] = [price, unit_sale, revenue]
    return price_dict

def parse_loop_ca(driver, url, flag=False):
    price_dict = {}
    driver = open_browser_ca(driver, url='https://www.amazon.ca/', flag=flag)
    asin = extract_asin(url[0])
    driver.get(url[0])
    time.sleep(kDelay)
    
    price, unit_sale, revenue = parse_asin_ca(driver)
    if kEnablePrice == False:
        price = 0
    if unit_sale == 'N/A':
        unit_sale = 0

    price_dict[asin] = [price, unit_sale, revenue]
    return price_dict

def parse_amazon(data_path=None, us_price_column=None, us_sale_column=None,
                 ca_price_column=None, ca_sale_column=None, revenue_column=None):
    driver = setup_driver()

    priority = 1
    batch_size = 10

    loader = DatasetLoader(csv_path=data_path, priority=priority, batch_size=batch_size)
    redis_empty_retry_interval = 30
    processed_asins = set()
    print(priority)
    while True:
        loader.load_dataset()
        asin_list = loader.load_dataset_from_redis()

        # Filter out already processed ASINs
        new_asins = [asin for asin in asin_list if asin not in processed_asins]

        print(f"New ASINs to process: {new_asins}")
        if new_asins:
            for asin in new_asins:
                url_us, url_ca = asin_to_url([asin])
                print(asin)
                dict_us = parse_loop_us(driver, url_us, flag=True)
                dict_ca = parse_loop_ca(driver, url_ca, flag=True)

                # Retry for US parsing
                if any(value[0] == 0 for value in dict_us.values()):
                    dict_us = parse_loop_us(driver, url_us, flag=False)

                # Retry for CA parsing
                if any(value[0] == 0 for value in dict_ca.values()):
                    dict_ca = parse_loop_ca(driver, url_ca, flag=False)

                # Create CSV files with parsed results
                print(dict_us, dict_ca)
                create_csv(dict_us, dict_ca, data_path=data_path, us_price_column=us_price_column, 
                        us_sale_column=us_sale_column, ca_price_column=ca_price_column, 
                        ca_sale_column=ca_sale_column, revenue_column=revenue_column)

                # Add processed ASIN to the set
                processed_asins.add(asin)
                # Remove the ASIN from Redis
                loader.redis_client.zrem('asin_queue', asin)

        else:
            # If there are no new ASINs, listen for new ones
            time.sleep(redis_empty_retry_interval)

    driver.quit()
