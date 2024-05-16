from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ..parsing_methods import *
from codebase.util.utils import *
from codebase.dataset_loader import DatasetLoader
import sys

def open_browser_ratio(driver):

    calc_revenue(driver=driver)
    

def open_browser_us(driver, url,):
    
    driver.get(url)
    html = driver.page_source
    print(driver.title)
    soup = BeautifulSoup(html,features="lxml")
    try:
        captcha_handle(soup,driver)
    except:
        pass
    try:
        change_location_us(driver)
    except:
        pass
    return driver


def open_browser_ca(driver, url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,features="lxml")
    try:
        captcha_handle(soup,driver)
    except:
        pass
    # change_location_ca(driver)
    return driver


def parse_asin_us(driver):
    
    try:   
        price = 0
        html_updated = driver.page_source
        soup_updated = BeautifulSoup(html_updated,features="lxml")
        price, sale = get_price_us(soup_updated)
        return price, sale
    
    except ValueError as e :
        print(e)
        print("Error in parsing")
        pass


def parse_ratio(driver, asin):
        
    open_browser_ratio(driver=driver)
    change_revenue_country(driver=driver, asin=asin)
    html_updated = driver.page_source
    soup = BeautifulSoup(html_updated,features="lxml")
    price = get_price_revenue(driver=driver)
    return price


def parse_loop_us(file_path):
    loader = DatasetLoader(file_path=file_path)
    asin_list = loader.load_dataset()
    url_list_us, url_list_ca = asin_to_url(asin_list)
    price_dict = dict()
    index = 0
    options = webdriver.ChromeOptions()
    my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    options.add_argument(f"--user-agent={my_user_agent}")
    options.add_argument("--headless=new")
    # options.add_argument('--disable-gpu')
    # options.add_argument('--no-sandbox')
    options.add_extension('/Users/ardagulersoy/Desktop/Daily/listing-optimization-tool/extensions/helium10_extension.crx')
    driver = webdriver.Chrome(options=options)
    driver = enable_extensions(driver)
    time.sleep(6)
    driver = open_browser_us(driver, url='https://www.amazon.com/')
    for url in url_list_us[1:3]:
        price = 0
        index = index + 1
        asin = extract_asin(url)
        driver.get(url)
        time.sleep(5)
        if 'amazon.com' in url:
            
            try:
                price, unit_sale = parse_asin_us(driver=driver)  
            except:
                unit_sale = 0
                pass

        price_dict[asin] = [price, unit_sale]

    print(price)
    return price_dict
        


def parse_asin_ca(driver):
    try:
        price = 0
        html_updated = driver.page_source
        soup_updated = BeautifulSoup(html_updated,features="lxml")
        price, sale = get_price_us(soup_updated)
        return price, sale
    
    except ValueError as e :
        print(e)
        print("Error in parsing")
        pass
    

def parse_loop_ca(file_path):
    loader = DatasetLoader(file_path=file_path)
    asin_list = loader.load_dataset()
    url_list_us, url_list_ca = asin_to_url(asin_list)
    price_dict = dict()
    index = 0
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_extension('/Users/ardagulersoy/Desktop/Daily/listing-optimization-tool/extensions/helium10_extension.crx')
    driver = webdriver.Chrome(options=options)
    driver = enable_extensions(driver)
    time.sleep(6)
    driver = open_browser_ca(driver, url='https://www.amazon.ca/')
    for url in url_list_ca[1:3]:
        price = 0
        index = index + 1
        asin = extract_asin(url)
        driver.get(url)
        time.sleep(5)
        if 'amazon.ca' in url:
            try:
                price, unit_sale = parse_asin_us(driver=driver)  
            except:
                unit_sale = 0
                pass
        print(price)
        price_dict[asin] = [price, unit_sale]
  

    return price_dict
        
