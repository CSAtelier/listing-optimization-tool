from seleniumwire import webdriver  # Import from seleniumwire instead of selenium

# Set up Selenium Wire
chrome_options = webdriver.ChromeOptions()

# Initialize the driver
driver = webdriver.Chrome(options=chrome_options)

# Open the desired URL
driver.get("https://www.amazon.com/NEW-ENGLAND-CHEESEMAKING-Organic-Vegetable/dp/B00DHHOQSA")

# Capture network traffic
for request in driver.requests:
    if request.response:
        request_url = request.url
        response_status = request.response.status_code
        print(f"URL: {request_url}, Status Code: {response_status}")

# Quit the browser
driver.quit()
