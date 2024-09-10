#!/bin/bash
export DEBIAN_FRONTEND=noninteractive
# Step 1: Update all packages
sudo apt update
sudo apt upgrade -y

# Step 2: Download and install the Google Chrome stable package
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt -f install -y  # Fix dependencies, if necessary

# Step 3: Check installed Google Chrome version
google-chrome --version

# Step 4: Install Selenium and webdriver-manager
sudo apt install python3-pip -y  # Ensure pip is installed
pip3 install selenium webdriver-manager

# Step 5: Create a hello_world Python script to test Chrome with Selenium
cat <<EOF >test_headless.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument('--headless')  # Run headless to avoid needing a GUI
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://www.python.org")
    print("Title of the page is:", driver.title)
finally:
    driver.quit()
EOF

# Step 6: Run test.py and check Google Chrome is available
python3 test_headless.py

echo "Setup is complete. Enjoy Selenium with Chrome on Ubuntu!"

# Step 7: Lets test headfull mode

sudo apt install -y xvfb x11-xkb-utils xfonts-100dpi xfonts-75dpi xfonts-scalable xfonts-cyrillic x11-apps

cat << 'EOF' > test_headful.py
#!/usr/bin/env python3
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

EOF


sudo chmod +x test_headful.py

./test_headful.py


