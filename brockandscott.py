import re
import time
import sys
import os
import datetime
import selenium
import requests
from pytz import timezone
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from scrape_helper import Scraper, init_webdriver

##########################################################################
# INPUT
##########################################################################
base_url = 'https://www.brockandscott.com/foreclosure-sales/' \
           '?_sft_foreclosure_state={}&_sft_foreclosure_county={}&_sfm_saledate={}+{}&sf_paged={{}}'
County = sys.argv[1] if len(sys.argv) > 1 else 'Mecklenburg'  # ''Mecklenburg'# Cabarrus Mecklenburg
State = sys.argv[2] if len(sys.argv) > 2 else 'NC'
tz = timezone('EST')
datetime_obj = datetime.datetime.now(tz)
Date = '20171018'  # datetime_obj.strftime('%Y%m%d')

##########################################################################
# READ CONTENT FROM WEB PAGE
##########################################################################
driver = init_webdriver(browser='phantomjs')

base_url = base_url.format(State.lower(), County.lower(), Date, Date)
base_url = 'https://www.brockandscott.com/foreclosure-sales/?sf_paged={}'
base_url = 'https://www.brockandscott.com/foreclosure-sales/?_sfm_saledate=20171018+20171025&sf_paged={}'
driver.get(base_url)

# STORE PAGE SOURCE IN VARAIBLES
page_one = driver.page_source

try:
    driver.find_element_by_link_text('2').click()
    page_two = driver.page_source
except:
    page_two = None
driver.quit()


def requests_response(url, params=None, cookies=None):
    """Returns the response object. It will either do a post based on
    whether there are params and cookies passed or not, or will do a simple
    get request. This is the implementation of scrape as a method.

    :param url: the URL rule as string
    :param params: a dict object containing the parameters to be given to
                   requests for the next post request.

    """
    log_first_part = "sending request to {url}".format(url=url)
    if params and cookies:
        time.sleep(1)
        return requests.post(url,
                             params=params,
                             cookies=cookies)
    else:
        time.sleep(1)
        return requests.get(url)


##########################################################################
# START PARSING
##########################################################################
# we initialise a bot that will have run the parsing functions
today = datetime_obj.strftime('%d/%m/%Y')
brockandscoot = Scraper("brockandscott_{}".format(County.lower()), start_date=today, end_date=today)

HEADERS = None


def parse_page_main(soup):
    global HEADERS
    for row in soup.find_all('div', {'class': 'continfo'}):
        if HEADERS is None:
            HEADERS = [i.getText().strip(':') for i in row.find_all('p') if i.has_attr('style')]
            brockandscoot.headers = HEADERS

        values = [re.compile('\s+').sub(' ', i.getText().strip())
                  for i in row.find_all('p') if not i.has_attr('style')]

        yield dict(zip(HEADERS, values))


records_generators_list = []
page_number = 1
page_limit = 15
while page_number < page_limit:
    # print(base_url.format(page_number))
    response = requests_response(url=base_url.format(page_number))
    response_text = response.text

    soup = BeautifulSoup(response_text, "html.parser")
    page_title = soup.find('h1', {'class': 'page-title'})
    if page_title and page_title.getText() == 'Nothing Found':
        break

    if soup.find('div', {'class': 'continfo'}) is None:
        break

    records = parse_page_main(soup)
    records_generators_list.append(records)
    page_number += 1

if __name__ == "__main__":
    brockandscoot.multiple_records_to_csv(records_generators_list)
