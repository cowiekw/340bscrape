# Objective: Creat a both to search and extract data from the HRSA 340b covered entities page
# Date Updated: 04/03/2021

# Import packages for web scraping
import sys
import requests
from time import sleep
from core.selenium_scraper import SeleniumScraper
from core.sql_db import SQLPipeline

url = "https://340bopais.hrsa.gov/coveredentitysearch"
search_terms = {'state': all, 'keyword': '', 'class': 'Hospitals'}
search_terms['state'] = 'Alaska'
parameters = ['state', 'class']
entities = []

# PATH = "/Users/katecowie/Documents/Spring2021/kanterlab/340bot/chromedriver.exe"

scraper = SeleniumScraper()
scraper.setup_chrome_browser()

# Read the data on all 340b covered entities and store in a list, where each item is of the class entity
entities = scraper.scrape_all(parameters, search_terms)

# Create a SQL database with three tables
SQL = SQLPipeline()

try:
    SQL.create_connection(erase_first=True)
    SQL.create_table()
    SQL.store_data(entities, 'entity')

except Exception as ex:
    print("Exception:", ex)
finally:
    SQL.save_changes()

print("Number of entities:", len(entities))
