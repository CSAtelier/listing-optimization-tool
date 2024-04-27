from amazoncaptcha import AmazonCaptcha
from selenium.webdriver.common.by import By

def asin_to_url(asin_list):
    url_list = []
    for asin in asin_list:
        url_list.append(f"https://www.amazon.com/dp/{asin}")
    return url_list

def captcha_handle(response):

    captcha = AmazonCaptcha.fromdriver(response)
    solution = captcha.solve()
    print(solution)
    response.find_element(By.NAME, "field-keywords").send_keys(solution) 
    response.find_element(By.CLASS_NAME, "a-button-text").click()

def change_locationg(response):
    
    response.find_element(By.ID, "nav-global-location-popover-link").click()
    