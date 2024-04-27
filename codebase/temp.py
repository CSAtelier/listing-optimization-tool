from amazoncaptcha import AmazonCaptcha
from selenium import webdriver

driver = webdriver.Chrome() # This is a simplified example
driver.get('https://www.amazon.com/errors/validateCaptcha')

captcha = AmazonCaptcha.fromdriver(driver)
solution = captcha.solve()
print(solution)