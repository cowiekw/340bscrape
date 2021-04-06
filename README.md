# 340bscrape
## A program to scrape data on hospital 340b covered entities

In this project, I use python, selenium webdriver, and SQlite3 to extract hospital data from a government website and store the information in a database.

The Health Resources and Services Adminstrations (HRSA), a department within the US government, maintains data on hospitals and their 340b status. 340b is a federal program, founded in the 1990s, that permits safety hospitals-- hospitals that serve disadvantaged populations-- to purchase drugs at a discounted price. Hospitals eligible to participate in 340b include hospitals serving a large percent of low-income patients, children's hospitals, and hospitals in rural areas, among others.

 The goal of the 340b program is to reduce the cost of drugs in safety net hospitals, reducing patient out-of-pocket expenses and improving the quality of care. However, the effectiveness of 340b program is debated. Though 340b does not cost taxpayers money, some opponents worry that the drug discounts are misused by hospitals. PhRMA, the advocacy group representing the pharmaceutical industry, [opposes](https://www.phrma.org/en/Advocacy/340B) the 340b program. AAMC, the American Associate of Medical Colleges, [supports](https://www.aamc.org/news-insights/340b) 340b.

Here, I use selenium webdriver, a web testing tool, to navigate the HRSA website.

| Scraping Library | Pros | Cons |
| -----|------| -----|
| Beautiful Soup| Beginner-friendly html parsing | Slower, operates on one url
| Selenium | Web testing, interacts with JavaScript elements | Less efficient than Scrapy
| Scrapy| Asynchronous web crawling on multiple websites | Steep learning curve

### entity.py
Defines the custom class "Entity". An entity has the following attributes:
* Id - A unique alphanumeric ID assigned by the Office of Pharmacy Affairs (OPA)
* Name
* Subname - specifies the subdivision
* Address
* City
* State

### helpers.py
Defines functions used to interact with the HRSA website and scrape data.

*search_by_id (parameters_list, element_ids, search_terms, driver)*
*  parameters_list:
 a list of search parameters such as['state', 'class'], (where class can be Hospital or Non-Hospital) or ['state', 'keyword']
* element_ids: a dictionary with search elements and their corresponding html ids. This allows you to locate the search fields.
* search terms: a dictionary with specific search terms for all possible parameters. The default is {'state': all, 'keyword': '', 'class': 'Hospitals'}

*wait_by_id (element_id, driver)*
* locates a web element by its id and waits for it to load

*wait_by_class(element_class, driver)*
* locates a web element by its class and waits for it to load

*read_data(row_count, entity_list, driver)*
* For every row of data...
 * Locates tabular data of interest based on xpaths
 * Stores the text from each data element in a dictionary
 * saves the data as an entity object and adds to a list of all entities

### selenium_scraper.py
*scrape_all (self, parameters, search_terms)*
* opens the url
* searches entities based on parameters provided
* waits for content to load and counts number of pages
* For each page..
  * waits for tabular data to load
  * reads the data into a list

*split_data(self, entity_list, parent_list, child_list)*
* entity_list: contains all the scraped entities
* parent_list, child_list: empty lists
* reads the data on entities and classifies each entity as a parent or child based on whether or not there is a subdivision name.

### sql_db.py
* Sets up a SQL connect and creates a database
* Creates 4 tables for a) all entities, b) parent entities, c) child entities, d) contract pharmacies

*store_data(self, entities_list, table_name)*
* Takes as input a list of entity objects and inserts each entity into the specified table.

<p> Notes: Child site- A clinic, department, or outpatient facility participating in the 340b program that is affiliated with a parent hospital <p>

## License
You are free to:
Share — copy and redistribute the material in any medium or format
Adapt — remix, transform, and build upon the material

Under the following terms:
Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
NonCommercial — You may not use the material for commercial purposes.
