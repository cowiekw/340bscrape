# Objective: Creat a bot to search and extract data from the HRSA 340b covered entities page
# Date Updated: 05/28/2021

# Import packages for web scraping
import sys
import requests
from time import sleep
from core.selenium_scraper import SeleniumScraper
from core.sql_db import SQLPipeline

url = "https://340bopais.hrsa.gov/coveredentitysearch"
search_terms = {'state': 'all', 'class': 'Hospitals'}

parameters = ['state','class']

# Create empty lists to store scraped data in
entities = []
parents = []
children = []

scraper = SeleniumScraper()
scraper.setup_chrome_browser()

# Read the data on all 340b covered entities and store in a list, where each item is of the class entity
entities = scraper.scrape_all(parameters, search_terms)

data_dict = scraper.split_data(entities, parents, children)
parents = data_dict['parent']
children = data_dict['child']

# Set up SQL connection
SQL = SQLPipeline()

try:
    SQL.create_connection(erase_first=True)

    # Create a SQL database with three tables
    # SQL.create_table()

    # Insert covered entity data into each table
    SQL.store_data(entities, 'entity')
    SQL.store_data(parents, 'parent')
    SQL.store_data(children, 'child')

except Exception as ex:
    print("Exception:", ex)
finally:
    SQL.save_changes()

print("Number of entities:", len(entities))
print("Number of parents:", len(parents))
print("Number of children:", len(children))
