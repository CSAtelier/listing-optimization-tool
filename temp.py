from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# # Set up Chrome options
chrome_options = Options()
extension_path = "/Users/ardagulersoy/Downloads/oay"
helium_path = "/Users/ardagulersoy/Desktop/Personal/listing-optimization-tool/extensions/helium10_extension.crx"


chrome_options.add_argument(f"--load-extension={extension_path}")
chrome_options.add_extension('extensions/helium10_extension.crx')
# Initialize the WebDriver

driver = webdriver.Chrome(options=chrome_options)

# # Open a page to test if the extension is loaded
driver.get("https://www.amazon.com/dp/B0CRX9CVJR/")

while True:

    try:

        revenue_button = driver.find_element(By.CLASS_NAME, "sc-bIqLuP leZmcY") 
        print(revenue_button)
    except:
        pass

#     # Do something with the element (e.g., print text or interact with it)
#     # print(div_element.text)
#     pass
# # Perform actions using Selenium as usual
# # driver.find_element_by_name("q").send_keys("Selenium Extension Test")

# # Close the browser
# driver.quit()


