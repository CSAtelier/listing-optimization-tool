from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

def captcha_handle(response,driver):
    img = response.find_all("img")[0]["src"]
    captcha = AmazonCaptcha.fromlink(img)
    solution = captcha.solve()
    driver.find_element(By.NAME, "field-keywords").send_keys(solution) 
    driver.find_element(By.CLASS_NAME, "a-button-text").click()


def change_location_us(driver):
    
    driver.find_element(By.ID, "nav-global-location-popover-link").click()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput")))
    postcode_form = driver.find_element(By.ID, "GLUXZipUpdateInput").send_keys("73001") 
    postcode_button = driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdate"]/span/input').click()
    time.sleep(2)
    continue_button = driver.find_element(By.XPATH, '//*[@id="a-popover-1"]/div/div[2]/span/span').click()
    # continue_button.click()
    time.sleep(2)


def get_price_us(response):
    try:
        price = response.find('span', attrs = {'class':'a-offscreen'})
        price = re.search(r'\$\d+\.\d+', price.text).group()
    except:
        price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
        price = re.search(r'\$\d+\.\d+', price.text).group()
        
    return float(price[1:])


def change_location_ca(driver):
    
    driver.find_element(By.ID, "nav-global-location-popover-link").click()
    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput_0")))
    # postcode_form0 = driver.find_element(By.ID, "GLUXZipUpdateInput_0").send_keys("M5V") 
    # postcode_form1 = driver.find_element(By.ID, "GLUXZipUpdateInput_1").send_keys("3L9") 
    # postcode_button = driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdate"]/span/input').click()
    # time.sleep(2)
    # continue_button = driver.find_element(By.XPATH, '//*[@id="a-popover-3"]/div/div[2]/span').click()


def get_price_ca(response):
    try:
        price = response.find('span', attrs = {'class':'a-offscreen'})
        price = re.search(r'\$\d+\.\d+', price.text).group()
    except:
        price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
        price = re.search(r'\$\d+\.\d+', price.text).group()
    return float(price[1:])