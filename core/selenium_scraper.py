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
element_ids = {'state': 'ContentPlaceHolder1_ceSearchCtrl_lstEntityState', 'keyword':'ContentPlaceHolder1_ceSearchCtrl_txtKeyword', 'class':'ContentPlaceHolder1_ceSearchCtrl_ddlEntityClassification', 'filter_subname': 'ctl00_ContentPlaceHolder1_CoveredEntitySearchGrid_ctl00_ctl02_ctl02_Filter_SubName'}

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
        PATH = path+chromedriver
        self.driver = webdriver.Chrome(PATH)

    def scrape_all(self, parameters, search_terms):
        # Paremeters can be a combination of state, keyword, and/or class
        driver = self.driver
        driver.get(url)
        print("Page Title: ", driver.title)
        entity_list = []
        parent_list = []
        child_list = []

        search_by_id(parameters, element_ids, search_terms, driver)

        # Make the search and wait for results to load
        wait_by_id(grid_id, driver)
        time.sleep(1)
        page_count = count_pages(driver)

        # Flip the pages
        for i in range(1, page_count + 1):
            wait_by_class('rgAltRow', driver)
            time.sleep(1)
            try:
                row_count = count_rows(driver)
            except:
                print("Error with row count")
                row_count = 25
            read_data(row_count, entity_list, driver)
            next_page_element = wait_by_class('rgPageNext', driver) # Wait for the 'next page' element to load
            next_page_element.send_keys(Keys.RETURN) # Go to the next page

        driver.quit()
        return entity_list

    def split_data(self, entity_list, parent_list, child_list):
        print("Length of entity list:", len(entity_list))
        for ent in entity_list:
            if (ent.subname == None) or (ent.subname == '') or (ent.subname == ' '):
                parent_list.append(ent)
            else:
                child_list.append(ent)
        data_dict = {'parent': parent_list, 'child': child_list}
        return data_dict
