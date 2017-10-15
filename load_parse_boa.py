import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from scrape_helper import init_webdriver
from bs4 import BeautifulSoup


def load_boa(boa_url):
    '''
    Render and Load BOA URL and return html page source
    :param boa_url: (str) url of boa realestate
    :return: (str) html page source
    '''
    browser = init_webdriver(browser='phantomjs')
    # browser.set_page_load_timeout(40)

    try:
        browser.get(boa_url)
    except TimeoutException:
        return

    delay = 10  # seconds
    try:
        WebDriverWait(browser, delay).until(
            EC.presence_of_element_located((By.ID, 'facts-table')))

        # print("Page is ready!")
    except TimeoutException:
        # print("Loading took too much time!")
        pass
    finally:
        page_source = browser.page_source
        browser.close()
    return page_source  # browser.page_source


def parse_boa(html_page_source):
    '''
    This function parses and prepares a mapping of required attributes of BOA url

    Render boa(javascript webpage) using PyQt or Scrapy and pass to this function

    :param html_page_source: html source of
        https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address={ADDRESS}
    :return: attributes mapping for Estimate Range,
        Estimate, Avg. Sales Price and BedRooms from boa web page
    '''

    def soup_find_text(*args, **kwargs):
        '''
        get text if tag is found for respective soup find
        return empty string in case of None object
        '''
        tag = soup.find(args, kwargs)
        if tag:
            return tag.get_text()
        return None

    # // if html page source is None, return ERROR
    if html_page_source is None:
        return {'Error': "Unable to load page"}

    soup = BeautifulSoup(html_page_source, "lxml")

    attrs_map = {}

    # // check if there is any error
    error = soup_find_text('div', **{'class': 'error-title'})
    if error:
        return {'Error': error}

    # // Store result for Estimate Range, Estimate nd Avg. Sales Price from boa web page
    attrs_map['Estimate Range'] = soup_find_text('div', **{'class': 'value-large'})
    attrs_map['Estimate'] = soup_find_text('span', id='est-value')
    attrs_map['Avg. Sales Price'] = soup_find_text('span', id='comps-average')

    # // Store result like Number of BedRooms from facts_table
    # set default value for Bedrooms to None
    attrs_map['Bedrooms'] = None
    facts_table = soup.find('table', {'class': 'facts-table'})
    if facts_table:
        for row in facts_table.find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 2:
                key = cols[0].get_text()
                value = cols[1].get_text()
                attrs_map[key] = value
                # // for now info of Bedrooms is sufficient
                # // when more details are required, remove break
                break

    return attrs_map


def get_rent_attributes_from_boa(address):
    if not address.strip():
        return {'Error': "Empty Address"}
    boa_url = "https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address="
    boa_substitute = lambda x: boa_url + str(x).replace(',', '').replace(' ', '+')

    # extract url from address
    url = boa_substitute(address)

    # render boa url and parse it (return rent estimate attributes)
    html_page_source = load_boa(url)
    return parse_boa(html_page_source)


if __name__ == '__main__':
    from pprint import pprint

    a = time.time()
    # # Success URL
    # boa_url = r'https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address=7318+MIDDLEBURY+PL+CHARLOTTE+NC+28212'
    # # Error title URL
    # boa_url = r'https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address=4916+Laborde+Street+Charlotte+NC+28269'
    # html_page = load_boa(boa_url)
    # res = parse_boa(html_page)

    res = get_rent_attributes_from_boa('7318 MIDDLEBURY PL, CHARLOTTE, NC 28212')
    pprint(res)
    b = time.time()
    print(b - a)
