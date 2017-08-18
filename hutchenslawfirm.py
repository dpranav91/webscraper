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
base_url = 'https://sales.hutchenslawfirm.com/NCfcSalesList.aspx'
Country = sys.argv[1] if len(sys.argv)>1 else 'Cabarrus'#''Mecklenburg'# Cabarrus Mecklenburg
# State = sys.argv[2] if len(sys.argv)>2 else 'NC'
tz = timezone('EST')
datetime_obj = datetime.datetime.now(tz)
Date = datetime_obj.strftime('%m/%d/%Y')

##########################################################################
# READ CONTENT FROM WEB PAGE
##########################################################################
driver = init_webdriver(browser='phantomjs')
driver.get(base_url)

countryElement = driver.find_element_by_name("SearchTextBox")
countryElement.send_keys(Country)

searchElement = driver.find_element_by_name("SearchButton")
searchElement.click()

page_one = driver.page_source
# STORE PAGE SOURCE IN VARAIBLES
# page_one = open('text.html').read()
# print(page_one)

##########################################################################
# START PARSING
##########################################################################
# we initialise a bot that will have run the parsing functions
today = datetime_obj.strftime('%d/%m/%Y')
hutchenslawfirm = Scraper("hutchenslawfirm_{}".format(Country.lower()), start_date=today, end_date=today)


def parse_table(html_page_source):
    soup = BeautifulSoup(html_page_source, "lxml")

    table = soup.find('table', id='SalesListGrid_ctl01')
    # set header
    # -------------
    headers = [th.get_text() for th in table.find('thead').find_all('th')]
    hutchenslawfirm.headers = headers
    for row_index, row in enumerate(table.find('tbody').find_all('tr')):
        data_tags = row.find_all('td')
        # table data
        # --------------
        cols = []
        for col in data_tags:
            cols.append(col.get_text().strip())
        elem = dict(zip(headers, cols))
        yield elem


@hutchenslawfirm.scrape(response=page_one)
def parse_page():
    return parse_table(page_one)


# @hutchenslawfirm.scrape(response=page_two)
# def parse_page2():
#     if page_two:
#         return parse_table(page_two)

parse_functions = [parse_page]
# if page_two:
#     parse_functions.append(parse_page2)

if __name__ == "__main__":
    hutchenslawfirm.run(parse_functions)