import time
import os
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from core.entity import Entity

def search_by_id(parameters_list, element_ids, search_terms, driver):
    for key in parameters_list:
        search = driver.find_element_by_id(element_ids[key])
        search.send_keys(search_terms[key])
    search.send_keys(Keys.RETURN) # Execute the search

def search_all_hospitals(element_ids, driver): # Find states based ON the html element id
    search = driver.find_element_by_id(element_ids['class_id'])
    search.send_keys('Hospitals')
    search.send_keys(Keys.RETURN) # Execute the search

def search_state_keyword(element_ids, search_terms, driver): # Find states based ON the html element id
    search = driver.find_element_by_id(element_ids['state_id'])
    search.send_keys(search_terms['state'])
    # time.sleep(1)
    search = driver.find_element_by_id(element_ids['keyword_id'])
    search.send_keys(search_terms['keyword'])
    search.send_keys(Keys.RETURN) # Execute the search

def wait_by_id(element_id, driver):  # Wait for page contents to load
    try:
        your_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, element_id)))
    except StaleElementReferenceException as e:
        raise e

def wait_by_class(element_class, driver): # Wait for page links to load
    try:
        next_page_element = driver.find_element_by_class_name(element_class)
        return next_page_element
    except StaleElementReferenceException as e:
        print("Except")
        raise e

def count_rows(driver):
    rows = driver.find_elements_by_class_name('rgRow')
    alt_rows = driver.find_elements_by_class_name('rgAltRow')
    row_count = len(rows) + len(alt_rows)
    print("Rows, alts: ", len(rows), len(alt_rows))
    return row_count

# Determine the total number of pages
def count_pages(driver):
    try:
        xpath_page_count = '//*[@id="ctl00_ContentPlaceHolder1_CoveredEntitySearchGrid_ctl00_ctl02_ctl00_PageOfLabel"]'
        page_count = driver.find_element_by_xpath(xpath_page_count)
        page_count = page_count.text.split(' ')[1] # Split the text (for example: " of 35") by the space
        page_count = int(page_count)
        return page_count
    except:
        print("error: page count not found")

def read_data(row_count, entity_list, driver):
    for i in range(row_count):  # For every row of data
        # Make dictionary of relevant xpaths
        xpaths_dict = {}
        xpaths_dict['id'] = '//*[@id="ctl00_ContentPlaceHolder1_CoveredEntitySearchGrid_ctl00__'+str(i)+'"]/td[2]/a'
        xpaths_dict['name'] = '//*[@id="ctl00_ContentPlaceHolder1_CoveredEntitySearchGrid_ctl00__'+str(i)+'"]/td[5]'
        xpaths_dict['sub_name'] = '//*[@id="ctl00_ContentPlaceHolder1_CoveredEntitySearchGrid_ctl00__'+str(i)+'"]/td[4]'
        xpaths_dict['address'] = '//*[@id="ctl00_ContentPlaceHolder1_CoveredEntitySearchGrid_ctl00__'+str(i)+'"]/td[6]'
        xpaths_dict['city'] = '//*[@id="ctl00_ContentPlaceHolder1_CoveredEntitySearchGrid_ctl00__'+str(i)+'"]/td[7]'
        xpaths_dict['state'] = '//*[@id="ctl00_ContentPlaceHolder1_CoveredEntitySearchGrid_ctl00__'+str(i)+'"]/td[8]'
        ent = {} # Make dictionary for each row data
        for key in xpaths_dict:
            try:
                ent[key] = driver.find_element_by_xpath(xpaths_dict[key]).text
                #print(key, "FOUND")
            except:
                # print(key, "NOT FOUND")
                ent[key] = None

        # Append each entity into a list
        entity = Entity(ent['id'], ent['name'], ent['sub_name'],ent['address'], ent['city'], ent['state'])
        entity_list.append(entity)
        print(i, entity)
