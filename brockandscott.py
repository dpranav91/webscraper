import re
import time
import os
import datetime
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrape_helper import Scraper

##########################################################################
# INPUT
##########################################################################
base_url = 'https://www.brockandscott.com/BrockSearch.aspx'
State = 'NC'
Country = 'Mecklenburg'
Date = datetime.datetime.now().strftime('%m/%d/%Y')

##########################################################################
# READ CONTENT FROM WEB PAGE
##########################################################################
chromedriver = os.path.join(os.getcwd(),'utilities','chromedriver.exe')
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get(base_url)

stateElement = driver.find_element_by_name("ddlState")
stateElement.send_keys(State)

countryElement = driver.find_element_by_name("ddlCounty")
countryElement.send_keys(Country)

dateElement = driver.find_element_by_name("txtFDate")
dateElement.send_keys(Date)

searchElement = driver.find_element_by_name("LinkButtonSearch")
searchElement.click()

# STORE PAGE SOURCE IN VARAIBLES
page_one = driver.page_source

try:
    driver.find_element_by_link_text('2').click()
    page_two = driver.page_source
except:
    page_two = None
driver.quit()

##########################################################################
# START PARSING
##########################################################################
# we initialise a bot that will have run the parsing functions
today = datetime.datetime.now().strftime('%d/%m/%Y')
brockandscoot = Scraper("brockandscoott", start_date=today, end_date=today)

def parse_table(html_page_source):
    soup = BeautifulSoup(html_page_source, "lxml")

    table = soup.find('table', id='grdSearch')
    headers = []
    for row_index, row in enumerate(table.find_all('tr')[1:]):
        # set header
        # -------------
        # print(row)
        header_tags = row.find_all('th')
        data_tags = row.find_all('td')
        if header_tags:

            for col in header_tags:
                headers.append(col.get_text().strip())
            brockandscoot.headers = headers
        elif headers and len(data_tags)==len(headers):
            # # table data
            # # --------------
            cols = []
            for col in data_tags:
                cols.append(col.get_text().strip())
            elem= dict(zip(headers, cols))
            yield elem

@brockandscoot.scrape(response=page_one)
def parse_page():
    return parse_table(page_one)

@brockandscoot.scrape(response=page_two)
def parse_page2():
    return parse_table(page_two)

parse_functions = [parse_page, parse_page2]

if __name__ == "__main__":
    brockandscoot.run(parse_functions)