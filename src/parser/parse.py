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

def setup_driver():

    options = Options()
    if kIsHeadless == True:
        options.add_argument("--headless=new")
    if kEnableHelium == True:
        extension_path = "extensions/oay"
        options.add_extension('extensions/helium10_extension.crx')
        options.add_argument(f"--load-extension={extension_path}") 
    driver = webdriver.Chrome(options=options)
    # if kEnableHelium == True:
    #     extension_popup_url = "chrome://extensions/?id=ankbemgeefkagbfgnjjaboocalfnoehb/index.html"
    #     # # Navigate to the extension's popup page
    #     driver.get(extension_popup_url)
    #     time.sleep(2)
    #     page_source = driver.page_source
    #     response = BeautifulSoup(page_source, 'lxml')
    #     root = response.find('div', attrs = {'id':'__root'})
    #     # print(root)
    #     # main = root.find('main', attrs = {'class':'flex flex-col h-full text-white w-full h-full'})
    #     while True:
    #         continue
    #     # driver.find_element(By.CLASS_NAME, 'bg-primary text-white cursor-pointer gap-2 inline-flex justify-center items-center rounded-md text-center font-medium text-xl w-full h-[50px]').click()
    
    return driver


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
    

def open_browser_us(driver, url,flag=False):
    
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,features="lxml")
    if flag == True:
        captcha_handle(soup,driver)
        change_location_us(driver)
    else:
        pass

    return driver


def open_browser_ca(driver, url,flag=False):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html,features="lxml")
    if flag == True:
        captcha_handle(soup,driver)
    else:
        pass
    # change_location_ca(driver)
    return driver


def parse_asin_us(driver):
    
    try:   
        price = 0
        html_updated = driver.page_source
        soup_updated = BeautifulSoup(html_updated,features="lxml")
        price, sale, revenue = get_price_us(soup_updated,driver=driver)
        print(price, sale, revenue)
        return price, sale, revenue
    
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


def parse_loop_us(driver,url,flag=False):
    price_dict = dict()
    # display = setup_headful_display()
    index = 0
    if kEnableHelium == True:
        # driver = enable_extensions(driver)
        pass
    time.sleep(kDelay*3)
    driver = open_browser_us(driver, url='https://www.amazon.com/',flag=flag)
    # driver.switch_to.window(driver.window_handles[0])
    # for url in url_list_us[0:kStop]:
    price = 0
    index = index + 1
    asin = extract_asin(url)
    driver.get(url)
    time.sleep(kDelay)
    if kEnableHelium == True:
        time.sleep(kDelay)
    if 'amazon.com' in url:
        
        try:
            price, unit_sale,revenue = parse_asin_us(driver=driver)
            if kEnablePrice == False:
                price = 0
            if unit_sale == 'N/A':
                unit_sale = "0"
            
        except:
            unit_sale = '0'
            revenue = 0
            pass

    price_dict[asin] = [price, unit_sale, revenue]

    return price_dict
        


def parse_asin_ca(driver):
    try:
        price = 0
        html_updated = driver.page_source
        soup_updated = BeautifulSoup(html_updated,features="lxml")
        price, sale,revenue = get_price_ca(soup_updated,driver=driver)
        print(price, sale, revenue)
        return price, sale, revenue
    
    except ValueError as e :
        print(e)
        print("Error in parsing")
        pass
    

def parse_loop_ca(driver,url,flag=False):
    # loader = DatasetLoader(file_path=file_path)
    # asin_list = loader.load_dataset()
    # url_list_us, url_list_ca = asin_to_url(asin_list)
    price_dict = dict()
    # display = setup_headful_display()
    index = 0
    if kEnableHelium == True:
        pass
    time.sleep(kDelay*3)
    driver = open_browser_ca(driver, url='https://www.amazon.ca/',flag=flag)
    # driver.switch_to.window(driver.window_handles[0])
    # for url in url_list_ca[0:kStop]:
    price = 0
    index = index + 1
    asin = extract_asin(url)
    driver.get(url)
    time.sleep(kDelay)
    if kEnableHelium == True:
        time.sleep(kDelay)
    if 'amazon.ca' in url:
        
        try:
            price, unit_sale,revenue = parse_asin_ca(driver=driver)
            if kEnablePrice == False:
                price = 0
            if unit_sale == 'N/A':
                unit_sale = "0"
            
        except:
            revenue = 0
            unit_sale = '0'
            pass

    price_dict[asin] = [price, unit_sale, revenue]

    return price_dict
        

def parse_amazon(data_path,us_price_column=None,us_sale_column=None,
                      ca_price_column=None,ca_sale_column=None,revenue_column=None):
    driver = setup_driver()
    loader = DatasetLoader(file_path=data_path)
    asin_list = loader.load_dataset()
    url_list_us, url_list_ca = asin_to_url(asin_list)
    for i in range(len(url_list_us[:kStop])):
        if i == 0:
            dict_us = parse_loop_us(driver=driver,url=url_list_us[i],flag=True)
            dict_ca = parse_loop_ca(driver=driver,url=url_list_ca[i],flag=True)
        else:
            dict_us = parse_loop_us(driver=driver,url=url_list_us[i],flag=False)
            dict_ca = parse_loop_ca(driver=driver,url=url_list_ca[i],flag=False)
        if i % 1 == 0:
            print(dict_us, dict_ca,i)
            create_excel(dict_us, dict_ca,data_path=data_path,us_price_column=us_price_column,us_sale_column=us_sale_column,
                            ca_price_column=ca_price_column,ca_sale_column=ca_sale_column,revenue_column=revenue_column,excel_index=i)
    return dict_us,dict_ca
