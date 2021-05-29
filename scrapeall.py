# Objective: Creat a bot to search and extract data from the HRSA 340b covered entities page
# Date Updated: 05/28/2021

# Import packages for web scraping
import sys
import requests
from time import sleep
from core.selenium_scraper import SeleniumScraper
from core.sql_db import SQLPipeline
from core.scrapestate import scrape_state

# Set up SQL connection
SQL = SQLPipeline()

try:
    SQL.create_connection(erase_first=True)
    SQL.create_table() # Create a SQL database with three tables
except Exception as ex:
    print("Exception:", ex)
finally:
    SQL.save_changes()

# state_list = ["Alaska", "District of Columbia"]
state_list = ["Alaska", "Alabama", "Arkansas","Arizona", "California", "Colorado", "Connecticut", "District of Columbia", "Delaware", "Florida", "Georgia", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

for state in state_list:
    scrape_state(state)
