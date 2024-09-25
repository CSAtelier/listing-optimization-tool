from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium_recaptcha_solver import RecaptchaSolver
import json
import time
import re
import requests
import pytesseract
import sys
from config import *
from config_types import DeploymentEnvEnum
from matplotlib import pyplot as plt
import cv2

def captcha_handle(response,driver):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "field-keywords")))
    img = response.find_all("img")[0]["src"]
    captcha = AmazonCaptcha.fromlink(img)
    solution = captcha.solve()
    driver.find_element(By.NAME, "field-keywords").send_keys(solution) 
    driver.find_element(By.CLASS_NAME, "a-button-text").click()


def change_location_us(driver):
    time.sleep(kDelay+5)
    driver.find_element(By.ID, "nav-global-location-popover-link").click()
    time.sleep(kDelay+5)
    postcode_form = driver.find_element(By.ID, "GLUXZipUpdateInput").send_keys("73001") 
    time.sleep(kDelay+5)
    postcode_button = driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdate"]/span/input').click()
    time.sleep(kDelay+5)
    continue_button = driver.find_element(By.XPATH, '//*[@id="a-popover-1"]/div/div[2]/span/span').click()
    print(continue_button)
    time.sleep(kDelay+5)

def get_revenue(driver,price):
            js_code = """
            // Log start of the process
            console.log("Starting the search for 'Revenue Calculator' div...");

        
            // Step 1: Get the shadow host
            let shadowHost = document.querySelector('#h10-bsr-graph');
            console.log("Shadow host found:", shadowHost);

            // Step 2: Access the first shadow root
            let firstShadowRoot = shadowHost.querySelector('div').shadowRoot;
            console.log("First shadow root accessed:", firstShadowRoot);

            // Step 3: Access the second shadow root inside the first one
            let secondShadowRoot = firstShadowRoot.querySelector('#h10-style-container').shadowRoot;
            console.log("Second shadow root accessed:", secondShadowRoot);

            // Step 4: Get all the divs inside the second shadow root
            let divs = secondShadowRoot.querySelectorAll('div');
            console.log("Divs found in second shadow root:", divs);

            // Step 5: Search for the target div with the text 'Revenue Calculator'
            let targetDiv = Array.from(divs).find(div => div.textContent.trim() === 'Revenue Calculator');
            
            if (targetDiv) {
                console.log("'Revenue Calculator' div found:", targetDiv);

                // Step 6: Log and click the target div
                targetDiv.click();
                console.log("Click action performed on 'Revenue Calculator' div.");
                return true;

            } else {
                console.warn("'Revenue Calculator' div not found.");
                return false;

            }
            
            """
    

            # Execute the JavaScript code
            click_successful = driver.execute_script(js_code)

            time.sleep(3)
            if click_successful:
                # Wait for the input field to be present and interactable
                try:
                    # Define the JavaScript to locate the input field of type number
                    wait_for_input_js = f"""
                        

                        // Step 1: Get the shadow host
                        let shadowHost = document.querySelector('#h10-bsr-graph');
                        console.log("Shadow host found:", shadowHost);

                        // Step 2: Access the first shadow root
                        let firstShadowRoot = shadowHost.querySelector('div').shadowRoot;
                        console.log("First shadow root accessed:", firstShadowRoot);

                        // Step 3: Access the second shadow root inside the first one
                        let secondShadowRoot = firstShadowRoot.querySelector('#h10-style-container').shadowRoot;
                        console.log("Second shadow root accessed:", secondShadowRoot);
                        let inputs = secondShadowRoot.querySelectorAll('input');
                        let fba_selling_price = inputs[3];   

                        // fba_selling_price.value = '{price}';  // Replace with the desired value for 'fba_selling_price'

                        // Trigger input event to ensure the values are updated
                        // fba_selling_price.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        
                        let spans = secondShadowRoot.querySelectorAll('span'); // Select all span elements
                        let dollarSignSpans = Array.from(spans).filter(span => span.textContent.includes('$'));
                        console.log(dollarSignSpans);
                        fba_net = dollarSignSpans[3].textContent.trim()
                        console.log(fba_net);
                        return fba_net;

                        
                    """

                    fba_net = driver.execute_script(wait_for_input_js)
                    time.sleep(1)
                    return fba_net
                    

                except Exception as e:
                    print("Error while handling the input field:", e)
            else:
                print("Target div not clicked or not found.")

            # Check if the click was successful
            if click_successful:
                print("Target div clicked successfully.")
            else:
                print("Target div not found or click failed.")

            time.sleep(2)



def get_price_us(response,driver):
    if kEnableHelium == True:
        try:
            time.sleep(2)
            sale = 0
            price = response.find('span', attrs = {'class':'a-offscreen'})
            unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            sale = unit_sale.text
            revenue = get_revenue(driver,price=price[-1:])




        except Exception as error:
            print(error)
            sale = 0
            price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
            sale = unit_sale.text
            revenue = get_revenue(driver)




    else:
        try:
            
            price = response.find('span', attrs = {'class':'a-offscreen'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            revenue = 0.0
            sale = 0.0

        except:
            
            price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            revenue = 0.0
            sale = 0.0

    try:
        index = revenue.find('$')
        revenue = revenue[index+1:]
        if "," in sale:
            sale = sale.replace(",", ".")
        if sale == 'N/A':
            sale = 0
    except:
        pass
    return float(price[1:]), float(sale), float(revenue)


def change_location_ca(driver):
    
    driver.find_element(By.ID, "nav-global-location-popover-link").click()
    # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "GLUXZipUpdateInput_0")))
    # postcode_form0 = driver.find_element(By.ID, "GLUXZipUpdateInput_0").send_keys("M5V") 
    # postcode_form1 = driver.find_element(By.ID, "GLUXZipUpdateInput_1").send_keys("3L9") 
    # postcode_button = driver.find_element(By.XPATH, '//*[@id="GLUXZipUpdate"]/span/input').click()
    # #time.sleep(2)
    # continue_button = driver.find_element(By.XPATH, '//*[@id="a-popover-3"]/div/div[2]/span').click()


def get_price_ca(response,driver):
    if kEnableHelium == True:
        try:
            sale = 0
            price = response.find('span', attrs = {'class':'a-offscreen'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
            sale = unit_sale.text
            revenue = get_revenue(driver,price=price[-1:])
        except:
            sale = 0
            price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            unit_sale = response.find('div', attrs = {'class':'sc-ipbtP bpzecP'})
            sale = unit_sale.text
            revenue = get_revenue(driver,price=price[-1:])
    else:
        try:
            
            price = response.find('span', attrs = {'class':'a-offscreen'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            revenue = 0.0
            sale = 0.0
        except:
            sale = 0
            price = response.find('span', attrs = {'class':'a-price aok-align-center reinventPricePriceToPayMargin priceToPay'})
            price = re.search(r'\$\d+\.\d+', price.text).group()
            revenue = 0.0
            sale = 0.0
    
    try:
        index = revenue.find('$')
        revenue = revenue[index+1:]
        if "," in sale:
            sale = sale.replace(",", ".")
        if sale == 'N/A':
            sale = 0
    except:
        pass

    return float(price[1:]), float(sale), float(revenue)


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

    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)") 
    time.sleep(2)
    driver.save_screenshot('screenie3.png')
    img = cv2.imread("screenie3.png", cv2.IMREAD_COLOR)
    img = img[kRevenueCrop[0]:kRevenueCrop[1],kRevenueCrop[2]:kRevenueCrop[3]]
    # img = img[1080:1115,620:800]

    # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    custom_config = r'--oem 3 --psm 6'
    # plt.imshow(img)
    # plt.show()
    price = pytesseract.image_to_string(img, config=custom_config)
    # try:
    #     price = price.replace("CA$", "").strip()
    #     print(price)
    # except:
    #     price = 0
    #     print(price)
    dollar_index = price.find('$')
    price = price[dollar_index + 1:].strip()
    return price

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
        button = buttons[0]
    button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary.error-container__btn')
    driver.execute_script("arguments[0].click();", button)
    time.sleep(3)
    sys.exit()
    # Error page
    #time.sleep(3)
    button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary.error-container__btn')
    button.click()

    if kDeploymentEnvEnum == DeploymentEnvEnum.LOCAL:

        driver.get('https://members.helium10.com/user/signin')
        driver.delete_all_cookies()  
        cookies_file_path = '/home/ubuntu/cookies.json'
        with open(cookies_file_path, 'r') as file:
            cookies = json.load(file)
        # Set the cookies in the browser
        for cookie in cookies:
            # Remove the domain key if it causes issues, as some cookies may not have a domain
            if 'sameSite' in cookie:
                cookie['sameSite'] = 'Lax'
            driver.add_cookie(cookie)
        time.sleep(kDelay+1)
        driver.get('https://members.helium10.com/user/signin')
        driver.switch_to.window(driver.window_handles[0])
        # First login try
        """
        driver.find_element(By.ID, "loginform-email").send_keys('akucukoduk16@ku.edu.tr')
        driver.find_element(By.ID, "loginform-password").send_keys('Abdullah1.')
        time.sleep(kDelay)
        driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
        time.sleep(kDelay*3)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        button = driver.find_element(By.CSS_SELECTOR, 'a.btn.btn-primary.error-container__btn')
        button.click()
        time.sleep(kDelay)
        driver.find_element(By.ID, "loginform-email").send_keys('akucukoduk16@ku.edu.tr')
        driver.find_element(By.ID, "loginform-password").send_keys('Abdullah1.')
        solver = RecaptchaSolver(driver=driver)
        recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
        solver.click_recaptcha_v2(iframe=recaptcha_iframe)
        driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()
        time.sleep(kDelay*5)
        driver.delete_all_cookies()  
        """
        time.sleep(kDelay*5)
    else:
        pass

    return driver
