import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from load_data_to_sheet import write_table_to_google_sheets
import time

def extract_league_data(url):
    browser = webdriver.Chrome()
    wait = WebDriverWait(browser, timeout=15)
    browser.execute_script("window.open('', '_blank');")
    browser.switch_to.window(browser.window_handles[1])
    browser.get(url)

    try:
        # Wait for the element to be visible
        indicator = wait.until(EC.visibility_of_element_located((By.ID, 'breadcrumb-nav')))
        element = indicator.find_element(By.ID, "tournaments")
        return element.get_attribute('value')
    except Exception as ex:
        print("An error occurred:")
        print(ex)
        print("Page source:")
        print(browser.page_source)
    finally:
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
        