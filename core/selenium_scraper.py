import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.helpers import wait_by_id, wait_by_class, search_by_id, count_rows, count_pages, read_data

url = "https://340bopais.hrsa.gov/coveredentitysearch"
grid_id = "ctl00_ContentPlaceHolder1_CoveredEntitySearchGrid"
element_ids = {'state_id': 'ContentPlaceHolder1_ceSearchCtrl_lstEntityState', 'keyword_id':'ContentPlaceHolder1_ceSearchCtrl_txtKeyword'}

class SeleniumScraper():
    def __init__(self):
        self.driver = None
        self.url = ''
        self.entities = []
        self.xpaths = {}

    def setup_chrome_browser(self):
        if os.name == 'posix' or os.name == 'nt': # if running on a mac or windows
            chromedriver ='/chromedriver.exe'

        path = os.path.dirname(os.path.abspath(__file__))
        print("Path", path)
        PATH = path+chromedriver
        self.driver = webdriver.Chrome(PATH)

    def scrape_all(self, search_terms):
        entity_list = []
        driver = self.driver
        driver.get(url)
        print("Page Title: ", driver.title)

        # Make the search and wait for results to load
        search_by_id(element_ids, search_terms, driver)
        wait_by_id(grid_id, driver)
        page_count = count_pages(driver)

        # Flip the pages
        for i in range(1, page_count + 1):
            print("Page: ", i)
            wait_by_class('rgAltRow', driver)
            time.sleep(1)
            try:
                row_count = count_rows(driver)
            except:
                print("Error with row count")
                row_count = 20
            print("Row count: ", row_count)
            read_data(row_count, entity_list, driver)
            next_page_element = wait_by_class('rgPageNext', driver) # Wait for the 'next page' element to load
            next_page_element.send_keys(Keys.RETURN) # Go to the next page

        return entity_list
