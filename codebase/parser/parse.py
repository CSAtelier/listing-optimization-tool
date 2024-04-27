from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import undetected_chromedriver as webdriver
from ..utils import *



def parse_asin(url):
    try:
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        # html = browser.page_source
        # soup = BeautifulSoup(html,features="lxml")
        captcha_handle(driver)
        # change_locationg(driver)
        # while True:
        #     pass
    except:
        print("Error in parsing")
        pass
