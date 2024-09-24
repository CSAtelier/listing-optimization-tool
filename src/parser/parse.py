import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ..parsing_methods import *
from src.util.utils import *
from src.dataset_loader import DatasetLoader
import subprocess
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.chrome.options import Options
from config import kDeploymentEnvEnum, kDelay, kIsHeadless, kEnablePrice
import json

# Configure logging to write to a file
log_filename = "amazon_parser.log"
logging.basicConfig(
    level=logging.INFO,  # Set logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format of logs
    handlers=[
        logging.FileHandler(log_filename),  # Log to a file
        logging.StreamHandler()  # Optional: Log to the console as well
    ]
)

logger = logging.getLogger(__name__)

def setup_driver():
    logger.info("Setting up the WebDriver")
    options = Options()
    if kIsHeadless:
        options.add_argument("--headless=new")
    if kEnableHelium:
        logger.info("Helium extension enabled")
        extension_path = "extensions/oay"
        options.add_extension('extensions/helium10_extension.crx')
        options.add_argument(f"--load-extension={extension_path}") 
    driver = webdriver.Chrome(options=options)
    return driver

def setup_headful_display():
    """ Set up virtual display for running headful Chrome. """
    logger.info("Setting up virtual display")
    display_number = 1
    lock_file = f"/tmp/.X{display_number}-lock"
    while os.path.exists(lock_file):
        display_number += 1
        lock_file = f"/tmp/.X{display_number}-lock"
    
    subprocess.Popen(['Xvfb', f':{display_number}'])
    return f':{display_number}'

def open_browser_ratio(driver):
    logger.info("Opening browser to calculate revenue")
    calc_revenue(driver=driver)

def open_browser_us(driver, url, flag=False):
    logger.info(f"Opening US browser for URL: {url}")
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    if flag:
        try:
            captcha_handle(soup, driver)
            change_location_us(driver)
            logger.info("Handled CAPTCHA and changed location to US")
        except Exception as e:
            logger.error(f"Error handling CAPTCHA: {e}")
    return driver

def open_browser_ca(driver, url, flag=False):
    logger.info(f"Opening CA browser for URL: {url}")
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, features="lxml")
    if flag:
        try:
            captcha_handle(soup, driver)
            logger.info("Handled CAPTCHA for CA")
        except Exception as e:
            logger.error(f"Error handling CAPTCHA: {e}")
    return driver

def parse_asin_us(driver):
    logger.info("Parsing ASIN for US")
    try:   
        price = 0
        html_updated = driver.page_source
        soup_updated = BeautifulSoup(html_updated, features="lxml")
        price, sale, revenue = get_price_us(soup_updated, driver=driver)
        return price, sale, revenue
    except ValueError as e:
        logger.error(f"Error in parsing ASIN for US: {e}")
        pass

def parse_ratio(driver, asin):
    logger.info(f"Parsing ratio for ASIN: {asin}")
    open_browser_ratio(driver=driver)
    change_revenue_country(driver=driver, asin=asin)
    html_updated = driver.page_source
    soup = BeautifulSoup(html_updated, features="lxml")
    price = get_price_revenue(driver=driver)
    return price

def parse_loop_us(driver, url, flag=False):
    logger.info(f"Parsing US loop for URL: {url}")
    price_dict = dict()
    index = 0
    time.sleep(kDelay*3)
    driver = open_browser_us(driver, url='https://www.amazon.com/', flag=flag)
    price = 0
    index += 1
    asin = extract_asin(url)
    driver.get(url)
    time.sleep(kDelay)
    try:
        price, unit_sale, revenue = parse_asin_us(driver=driver)
        if kEnablePrice == False:
            price = 0
        if unit_sale == 'N/A':
            unit_sale = 0
    except Exception as e:
        logger.error(f"Error parsing US loop for ASIN: {asin}, Error: {e}")
        unit_sale = 0
        revenue = 0
    price_dict[asin] = [price, unit_sale, revenue]
    return price_dict

def parse_asin_ca(driver):
    logger.info("Parsing ASIN for CA")
    try:
        price = 0
        html_updated = driver.page_source
        soup_updated = BeautifulSoup(html_updated, features="lxml")
        price, sale, revenue = get_price_ca(soup_updated, driver=driver)
        return price, sale, revenue
    except ValueError as e:
        logger.error(f"Error in parsing ASIN for CA: {e}")
        pass

def parse_loop_ca(driver, url, flag=False):
    logger.info(f"Parsing CA loop for URL: {url}")
    price_dict = dict()
    index = 0
    time.sleep(kDelay*3)
    driver = open_browser_ca(driver, url='https://www.amazon.ca/', flag=flag)
    price = 0
    index += 1
    asin = extract_asin(url)
    driver.get(url)
    time.sleep(kDelay)
    try:
        price, unit_sale, revenue = parse_asin_ca(driver=driver)
        if kEnablePrice == False:
            price = 0
        if unit_sale == 'N/A':
            unit_sale = 0
    except Exception as e:
        logger.error(f"Error parsing CA loop for ASIN: {asin}, Error: {e}")
        revenue = 0
        unit_sale = 0
    price_dict[asin] = [price, unit_sale, revenue]
    return price_dict

def parse_amazon(data_path, us_price_column=None, us_sale_column=None,
                 ca_price_column=None, ca_sale_column=None, revenue_column=None):
    logger.info("Starting Amazon parsing")
    driver = setup_driver()
    loader = DatasetLoader(file_path=data_path)
    asin_list = loader.load_dataset()
    url_list_us, url_list_ca = asin_to_url(asin_list)
    for i in range(len(url_list_us[:kStop])):
        if i == 0:
            dict_us = parse_loop_us(driver=driver, url=url_list_us[i], flag=True)
            dict_ca = parse_loop_ca(driver=driver, url=url_list_ca[i], flag=True)
        else:
            dict_us = parse_loop_us(driver=driver, url=url_list_us[i], flag=False)
            dict_ca = parse_loop_ca(driver=driver, url=url_list_ca[i], flag=False)
        if i % 1 == 0:
            logger.info(f"Parsed {i} URLs. US: {dict_us}, CA: {dict_ca}")
            create_excel(dict_us, dict_ca, data_path=data_path, us_price_column=us_price_column, 
                         us_sale_column=us_sale_column, ca_price_column=ca_price_column, 
                         ca_sale_column=ca_sale_column, revenue_column=revenue_column, excel_index=i)
    return dict_us, dict_ca
