from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ..parsing_methods import *
from codebase.util.utils import *
from codebase.dataset_loader import DatasetLoader
import subprocess
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
from selenium.webdriver.chrome.options import Options
from config import kDeploymentEnvEnum, kDelay, kIsHeadless, kEnablePrice


def setup_headful_display():
    """ Set up virtual display for running headful Chrome. """
    # Find a free display number
    display_number = 1
    lock_file = f"/tmp/.X{display_number}-lock"
    while os.path.exists(lock_file):
        display_number += 1
        lock_file = f"/tmp/.X{display_number}-lock"
    
    subprocess.Popen(['Xvfb', f':{display_number}'])
    return f':{display_number}'


def open_browser_ratio(driver):

    calc_revenue(driver=driver)
    

def open_browser_us(driver, url,):
    
    driver.get(url)
    html = driver.page_source
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
    # display = setup_headful_display()
    options = Options()
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    if kEnableHelium == True:
        options.add_extension('extensions/helium10_extension.crx')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    index = 0
    if kEnableHelium == True:
        driver = enable_extensions(driver)
    time.sleep(kDelay*3)
    driver = open_browser_us(driver, url='https://www.amazon.com/')
    driver.switch_to.window(driver.window_handles[0])
    for url in url_list_us[0:3]:
        price = 0
        index = index + 1
        asin = extract_asin(url)
        driver.get(url)
        time.sleep(kDelay)
        if kEnableHelium == True:
            time.sleep(kDelay)
        if 'amazon.com' in url:
            
            try:
                price, unit_sale = parse_asin_us(driver=driver)  
                if kEnablePrice == False:
                    price = 0
                
            except:
                unit_sale = '0,0'
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
    # display = setup_headful_display()
    options = Options()
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    if kEnableHelium == True:
        options.add_extension('extensions/helium10_extension.crx')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    index = 0
    if kEnableHelium == True:
        driver = enable_extensions(driver)
    time.sleep(kDelay*3)
    driver = open_browser_ca(driver, url='https://www.amazon.ca/')
    driver.switch_to.window(driver.window_handles[0])
    for url in url_list_ca[0:3]:
        price = 0
        index = index + 1
        asin = extract_asin(url)
        driver.get(url)
        time.sleep(kDelay)
        if kEnableHelium == True:
            time.sleep(kDelay)
        if 'amazon.ca' in url:
            try:
                price, unit_sale = parse_asin_us(driver=driver)  
                if kEnablePrice == False:
                    price = 0
            except:
                unit_sale ='0,0'
                pass
        print(price)
        price_dict[asin] = [price, unit_sale]
  

    return price_dict

def parse_amazon(data_path,us_price_column=None,us_sale_column=None,
                      ca_price_column=None,ca_sale_column=None):
    dict_us = parse_loop_us(file_path=data_path)
    dict_ca = parse_loop_ca(file_path=data_path)
    print(dict_us, dict_ca)
    create_excel(dict_us, dict_ca,data_path=data_path,us_price_column=us_price_column,us_sale_column=us_sale_column,
                      ca_price_column=ca_price_column,ca_sale_column=ca_sale_column)
    return dict_us,dict_ca
