import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tempfile
import os

def setup_headful_display():
    """ Set up virtual display for running headful Chrome. """
    # Find a free display number
    display_number = 1
    lock_file = f"/tmp/.X{display_number}-lock"
    while os.path.exists(lock_file):
        display_number += 1
        lock_file = f"/tmp/.X{display_number}-lock"
    
    subprocess.Popen(['Xvfb', f':{display_number}'])
    return f':{display_number}'

display = setup_headful_display()

options = Options()
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument(f'--display={display}')  # Use the virtual display

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://www.python.org")
    print("Title of the page is:", driver.title)
finally:
    driver.quit()
