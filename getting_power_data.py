from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(executable_path="/usr/local/bin/chromedriver")
with webdriver.Chrome(service=service) as driver:
    driver.get('https://npp.gov.in/monthlyGenerationReportsAct')
    # myLink = driver.find_element(By.CLASS_NAME, 'Zebra_DatePicker_Icon Zebra_DatePicker_Icon_Inside')
    # myLink.click()
    time.sleep(5)

