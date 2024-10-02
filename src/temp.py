from selenium import webdriver
import time



options = webdriver.ChromeOptions()

extension_path = "/Users/ardagulersoy/Desktop/Personal/listing-optimization-tool/extensions/oay"
options.add_extension('/Users/ardagulersoy/Desktop/Personal/listing-optimization-tool/extensions/helium10_extension.crx')
options.add_argument(f"--load-extension={extension_path}") 

# Use Selenium Wire WebDriver
driver = webdriver.Chrome(options=options)

driver.get('https://www.amazon.com/Great-Stuff-99112876-Dispenser-Sealants/dp/B07JD35J14?th=1')
html_content = driver.page_source
with open('/Users/ardagulersoy/Desktop/Personal/listing-optimization-tool/trash/page.html', 'w', encoding='utf-8') as file:
    file.write(html_content)