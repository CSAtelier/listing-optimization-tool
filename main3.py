import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def setup_browser():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    return driver

def parser_one():
    driver = setup_browser()
    try:
        driver.get("https://www.example.com")
        print("Parser One Title: ", driver.title)
        # Add your parsing logic here
    finally:
        driver.quit()

def parser_two():
    driver = setup_browser()
    try:
        driver.get("https://www.example.org")
        print("Parser Two Title: ", driver.title)
        # Add your parsing logic here
    finally:
        driver.quit()

def main():
    thread1 = threading.Thread(target=parser_one)
    thread2 = threading.Thread(target=parser_two)
    
    thread1.start()
    thread2.start()
    
    thread1.join()
    thread2.join()
    
    print("Both parsers have finished execution.")

if __name__ == "__main__":
    main()
