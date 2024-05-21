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
    # driver.implicitly_wait(1)
    time.sleep(2)
    continue_button = driver.find_element(By.XPATH, '//*[@id="a-popover-1"]/div/div[2]/span/span').click()
    #time.sleep(5)


def get_price_us(response):
    try:
        sale = 0
        price = response.find('span', attrs = {'class':'a-offscreen'})
        unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
        price = re.search(r'\$\d+\.\d+', price.text).group()
        sale = unit_sale.text

    except:
        price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
        price = re.search(r'\$\d+\.\d+', price.text).group()
        unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
        sale = unit_sale.text


    return float(price[1:]), sale


def change_location_ca(driver):
    
    driver.find_element(By.ID, "nav-global-location-popover-link").click()
    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput_0")))
    # postcode_form0 = driver.find_element(By.ID, "GLUXZipUpdateInput_0").send_keys("M5V") 
    # postcode_form1 = driver.find_element(By.ID, "GLUXZipUpdateInput_1").send_keys("3L9") 
    # postcode_button = driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdate"]/span/input').click()
    # #time.sleep(2)
    # continue_button = driver.find_element(By.XPATH, '//*[@id="a-popover-3"]/div/div[2]/span').click()


def get_price_ca(response):
    try:
        price = response.find('span', attrs = {'class':'a-offscreen'})
        price = re.search(r'\$\d+\.\d+', price.text).group()
        unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
    except:
        price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
        price = re.search(r'\$\d+\.\d+', price.text).group()
        unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
    sale = unit_sale.text
    return float(price[1:]),sale


def change_revenue_country(driver, asin):
    
    driver.find_element(By.CLASS_NAME, "dropdown-country").click()
    select = driver.find_element(By.XPATH, '//*[@id="ProductSearchInput"]/kat-dropdown/kat-option[2]').click()
    driver.find_element(By.XPATH, '//*[@id="ProductSearchInput"]/kat-input').send_keys(asin)
    driver.find_element(By.XPATH, '//*[@id="ProductSearchInput"]/kat-button').click()

    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput")))
    # postcode_form = driver.find_element(By.ID, "GLUXZipUpdateInput").send_keys("73001") 
    # postcode_button = driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdate"]/span/input').click()
    # #time.sleep(2)
    # continue_button = driver.find_element(By.XPATH, '//*[@id="a-popover-1"]/div/div[2]/span/span').click()
    # # continue_button.click()
    # #time.sleep(2)


def calc_revenue(driver):
    driver.get('https://sellercentral.amazon.com/hz/fba/profitabilitycalculator/index?lang=en_US')
    html = driver.page_source
    response = BeautifulSoup(html,features="lxml")
    driver.find_element(By.CLASS_NAME, "spacing-top-small").click()


def get_price_revenue(driver):

    #time.sleep(2)
    # price = response.find('div', attrs = {'class':'product-detail-content'})
    driver.execute_script("window.scrollTo(0, 1000)")
    driver.save_screenshot('screenie.png')
    img = cv2.imread('screenie.png')
    img = img[1000:1070,500:666]
    cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    custom_config = r'--oem 3 --psm 6'
    price = pytesseract.image_to_string(img, config=custom_config)
    index_ca = price.find('CA')
    price_cleaned = price[index_ca:]
    return float(price_cleaned[3:])
    # print(response)
    # price = driver.find_element(By.XPATH, '//*[@id="ProgramCard"]/div[2]/div[2]/div/div[1]/div[3]')


def enable_extensions(driver):
    driver.get('https://members.helium10.com/user/signin')
    driver.switch_to.window(driver.window_handles[0])
    # First login try
    driver.find_element(By.ID, "loginform-email").send_keys('akucukoduk16@ku.edu.tr')
    driver.find_element(By.ID, "loginform-password").send_keys('Abdullah1.')
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    buttons = soup.find_all('button')
    # Assuming there's only one button, get the first one
    if buttons:
        print(buttons)
        button = buttons[0]
    #time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-secondary.btn-block')
    driver.execute_script("arguments[0].click();", button)
    # Error page
    time.sleep(3)
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')
    buttons = soup.find_all('a')
    if buttons:
        print(buttons)
        button = buttons[0]
    button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary.error-container__btn')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)
    print(driver.page_source)
    sys.exit()
    # Error page
    #time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary.error-container__btn')
    button.click()

    # Second try
    #time.sleep(3)
    driver.find_element(By.ID, "loginform-email").send_keys('akucukoduk16@ku.edu.tr')
    driver.find_element(By.ID, "loginform-password").send_keys('Abdullah1.')

    try:
        driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
    except:
        recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        solver = RecaptchaSolver(driver=driver)
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()

    #time.sleep(5)
    
    #time.sleep(5)

    return driver