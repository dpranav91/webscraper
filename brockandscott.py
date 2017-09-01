import re
import time
import sys
import os
import datetime
import selenium
from pytz import timezone
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrape_helper import Scraper, init_webdriver

##########################################################################
# INPUT
##########################################################################
base_url = 'https://www.brockandscott.com/BrockSearch.aspx'
Country = sys.argv[1] if len(sys.argv)>1 else 'Mecklenburg'#''Mecklenburg'# Cabarrus Mecklenburg
State = sys.argv[2] if len(sys.argv)>2 else 'NC'
tz = timezone('EST')
datetime_obj = datetime.datetime.now(tz)
Date = datetime_obj.strftime('%m/%d/%Y')

##########################################################################
# READ CONTENT FROM WEB PAGE
##########################################################################
driver = init_webdriver(browser='phantomjs')
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
today = datetime_obj.strftime('%d/%m/%Y')
brockandscoot = Scraper("brockandscott_{}".format(Country.lower()), start_date=today, end_date=today)

def parse_table(html_page_source):
    soup = BeautifulSoup(html_page_source, "lxml")

    table = soup.find('table', id='grdSearch')
    headers = []
    for row_index, row in enumerate(table.find_all('tr')):
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
    if page_two:
        return parse_table(page_two)

parse_functions = [parse_page]
if page_two:
    parse_functions.append(parse_page2)

if __name__ == "__main__":
    brockandscoot.run(parse_functions)