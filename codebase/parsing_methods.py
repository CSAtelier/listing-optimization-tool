from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium_recaptcha_solver import RecaptchaSolver

import time
import re
import requests
import cv2 
import pytesseract
import sys
from config import *
from config_types import DeploymentEnvEnum

def captcha_handle(response,driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "field-keywords")))
    img = response.find_all("img")[0]["src"]
    captcha = AmazonCaptcha.fromlink(img)
    solution = captcha.solve()
    driver.find_element(By.NAME, "field-keywords").send_keys(solution) 
    driver.find_element(By.CLASS_NAME, "a-button-text").click()


def change_location_us(driver):
    
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "nav-global-location-popover-link")))
    driver.find_element(By.ID, "nav-global-location-popover-link").click()
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput")))
    postcode_form = driver.find_element(By.ID, "GLUXZipUpdateInput").send_keys("73001") 
    postcode_button = driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdate"]/span/input').click()
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="a-popover-1"]/div/div[2]/span/span')))
    time.sleep(kDelay)
    continue_button = driver.find_element(By.XPATH, '//*[@id="a-popover-1"]/div/div[2]/span/span').click()
    time.sleep(kDelay)


def get_price_us(response):
    if kEnableHelium == True:
        try:
            sale = 0
            price = response.find('span', attrs = {'class':'a-offscreen'})
            unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            sale = unit_sale.text

        except:
            sale = 0
            price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
            sale = unit_sale.text

    else:
        try:
            sale = '0,0'
            price = response.find('span', attrs = {'class':'a-offscreen'})
            price = re.search(r'\$\d+\.\d+', price.text).group()

        except:
            sale = '0,0'
            price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
            price = re.search(r'\$\d+\.\d+', price.text).group()

    return float(price[1:]), sale


def change_location_ca(driver):
    
    driver.find_element(By.ID, "nav-global-location-popover-link").click()
    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput_0")))
    # postcode_form0 = driver.find_element(By.ID, "GLUXZipUpdateInput_0").send_keys("M5V") 
    # postcode_form1 = driver.find_element(By.ID, "GLUXZipUpdateInput_1").send_keys("3L9") 
    # postcode_button = driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdate"]/span/input').click()
    # time.sleep(2)
    # continue_button = driver.find_element(By.XPATH, '//*[@id="a-popover-3"]/div/div[2]/span').click()


def get_price_ca(response):
    if kEnableHelium == True:
        try:
            sale = 0
            price = response.find('span', attrs = {'class':'a-offscreen'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
            sale = unit_sale.text
        except:
            sale = 0
            price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
            sale = unit_sale.text
    else:
        try:
            sale = 0
            price = response.find('span', attrs = {'class':'a-offscreen'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
        except:
            sale = 0
            price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
    return float(price[1:]),sale


def change_revenue_country(driver, asin):
    
    driver.find_element(By.CLASS_NAME, "dropdown-country").click()
    select = driver.find_element(By.XPATH, '//*[@id="ProductSearchInput"]/kat-dropdown/kat-option[2]').click()
    driver.find_element(By.XPATH, '//*[@id="ProductSearchInput"]/kat-input').send_keys(asin)
    driver.find_element(By.XPATH, '//*[@id="ProductSearchInput"]/kat-button').click()

    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput")))
    # postcode_form = driver.find_element(By.ID, "GLUXZipUpdateInput").send_keys("73001") 
    # postcode_button = driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdate"]/span/input').click()
    # time.sleep(2)
    # continue_button = driver.find_element(By.XPATH, '//*[@id="a-popover-1"]/div/div[2]/span/span').click()
    # # continue_button.click()
    # time.sleep(2)


def calc_revenue(driver):
    driver.get('https://sellercentral.amazon.com/hz/fba/profitabilitycalculator/index?lang=en_US')
    html = driver.page_source
    response = BeautifulSoup(html,features="lxml")
    driver.find_element(By.CLASS_NAME, "spacing-top-small").click()


def get_price_revenue(driver):

    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
    time.sleep(2)
    driver.save_screenshot('screenie3.png')
    img = cv2.imread("screenie3.png", cv2.IMREAD_COLOR)
    img = img[kRevenueCrop[0]:kRevenueCrop[1],kRevenueCrop[2]:kRevenueCrop[3]]
    # img = img[1080:1115,620:800]
    # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    custom_config = r'--oem 3 --psm 6'
    price = pytesseract.image_to_string(img, config=custom_config)
    print(price)
    index_ca = price.find('CA')
    price_cleaned = price[index_ca:]
    print(price_cleaned[4:-2])
    try:
        price = float(price_cleaned[4:-2])
    except:
        price = 0
    return price

def enable_extensions(driver):

    if kDeploymentEnvEnum == DeploymentEnvEnum.LOCAL:

        driver.get('https://members.helium10.com/user/signin')
        driver.switch_to.window(driver.window_handles[0])
        # First login try
        driver.find_element(By.ID, "loginform-email").send_keys('akucukoduk16@ku.edu.tr')
        driver.find_element(By.ID, "loginform-password").send_keys('Abdullah1.')
        time.sleep(kDelay)
        driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
        time.sleep(kDelay*5)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        if driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary.error-container__btn') != None:
            button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary.error-container__btn')
            button.click()
            time.sleep(kDelay)
            driver.find_element(By.ID, "loginform-email").send_keys('akucukoduk16@ku.edu.tr')
            driver.find_element(By.ID, "loginform-password").send_keys('Abdullah1.')
            # try:
            #     recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
            #     solver = RecaptchaSolver(driver=driver)
            #     solver.click_recaptcha_v2(iframe=recaptcha_iframe)
            # except:
            #     pass
            driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
            time.sleep(kDelay+2)
        else:
            pass

    return driver
