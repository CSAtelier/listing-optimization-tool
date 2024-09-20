from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
driver = webdriver.Chrome(options=options)

# Replace with your extension ID and popup HTML page path
extension_id = "ebhjdojccenkgmoojgbpklmlmmkmamiid"
extension_popup_url = f"chrome-extension://{extension_id}/popup.html"

# # Navigate to the extension's popup page
driver.get(extension_popup_url)

# # Now interact with the elements of the extension's popup page
# username_field = driver.find_element_by_id("username")
# password_field = driver.find_element_by_id("password")
# login_button = driver.find_element_by_id("login")

# # Enter credentials
# username_field.send_keys("your_username")
# password_field.send_keys("your_password")

# # Click login
# login_button.click()