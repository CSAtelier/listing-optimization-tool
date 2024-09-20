from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://chrome.google.com/webstore/detail/dynamic-assessment-plugin/fnapgcgphlfhecijolobjodbbnjjpdga')
browser.maximize_window()
browser.implicitly_wait(15)
browser.find_element_by_css_selector("[aria-label='Add to Chrome']").click()