from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ..utils import *



def parse_asin_us(url):
    try:
        price = 0
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,features="lxml")
        captcha_handle(soup,driver)
        change_location_us(driver)
        html_updated = driver.page_source
        soup_updated = BeautifulSoup(html_updated,features="lxml")
        price = get_price_us(soup_updated)
        driver.quit()
        return price
    
    except ValueError as e :
        print(e)
        print("Error in parsing")
        pass


def parse_asin_ca(url):
    try:
        price = 0
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html,features="lxml")
        captcha_handle(soup,driver)
        change_location_ca(driver)
        html_updated = driver.page_source
        soup_updated = BeautifulSoup(html_updated,features="lxml")
        price = get_price_ca(soup_updated)
        driver.quit()
        return price
    
    except ValueError as e :
        print(e)
        print("Error in parsing")
        pass