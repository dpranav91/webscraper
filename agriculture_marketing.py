import datetime
import time
from collections import namedtuple

import pandas as pd

from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select

from scrape_helper import init_webdriver
from utils import create_csv, setup_logging

OptionTuple = namedtuple('option', field_names=['value', 'text', 'uri_arg'])


class AgmarknetScraper(object):
    base_url = 'https://agmarknet.gov.in'
    commodity_id = 'ddlCommodity'
    state_id = 'ddlState'
    commodities_list = ['Tomato', 'Green Gram (Moong)(Whole)', 'Garlic']
    states_list = ['Andhra Pradesh', 'Telangana', 'Maharashtra', 'Karnataka', 'Chattisgarh', 'Tamil Nadu', 'Uttar Pradesh', 'Madhya Pradesh']

    def __init__(self, days_before=7, verbose=True, healess_browser=True):
        self.logger = setup_logging(verbose=verbose, name='argmarknet')
        self.driver = init_webdriver(browser='chrome', headless=healess_browser)
        self.driver.implicitly_wait(10)
        self.output = []
        self.start_date = self.stringify_date(days_before=days_before)
        self.end_date = self.stringify_date(days_before=0)
        self.output_filename = f'agmarknet_{self.start_date}_to_{self.end_date}'

    def stringify_date(self, days_before):
        today = datetime.datetime.today()
        days_to_subtract = datetime.timedelta(days=days_before)
        start_date_obj = today - days_to_subtract
        return start_date_obj.strftime('%d-%b-%Y')

    @staticmethod
    def convert_text_to_url_text(text):
        return text.replace(' ', '+')

    def generate_url(self, commodity_id='78', commodity='Tomato', state='Telangana', state_id='TL'):
        """
        URL example: https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=78&Tx_State=TL&Tx_District=0&Tx_Market=0&DateFrom=15-Dec-2020&DateTo=09-Jan-2021&Fr_Date=15-Dec-2020&To_Date=09-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Tomato&Tx_StateHead=Telangana&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
        """
        start_date = self.start_date
        end_date = self.end_date
        uri = f'SearchCmmMkt.aspx?Tx_Commodity={commodity_id}&Tx_State={state_id}&Tx_District=0&Tx_Market=0&DateFrom={start_date}&DateTo={end_date}&Fr_Date={start_date}&To_Date={end_date}&Tx_Trend=0&Tx_CommodityHead={commodity}&Tx_StateHead={state}&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--'
        return f'{self.base_url}/{uri}'

    def parse_page(self):
        page_content = self.driver.page_source
        soup = BeautifulSoup(page_content, "html.parser")
        table = soup.find("table", {'class': 'tableagmark_new'})  # 'id': 'cphBody_GridPriceData'
        headers = []
        for row_index, row in enumerate(table.find_all('tr')):
            # set header
            # -------------
            if row_index == 0:
                for col in row.find_all('th'):
                    headers.append(col.get_text().strip())

            if headers:
                td_cols = row.find_all('td')
                if len(headers) == len(td_cols):
                    cols = []
                    for col in td_cols:
                        cols.append(col.get_text().strip())
                    elem = dict(zip(headers, cols))
                    self.output.append(elem)
                elif len(td_cols) >= 1:
                    if td_cols[0].text == 'No Data Found':
                        self.logger.debug("No tabular data available")
                        return
                    if 'src="../images/Next.png"' in str(row):
                        xpath = ".//table//table//input[@src='../images/Next.png']"
                        next_input_elem = self.driver.find_element_by_xpath(xpath=xpath)
                        next_input_elem.click()
                        time.sleep(5)  # TODO: find better ways of doing
                        return self.parse_page()
                    else:
                        return

    def get_options(self, element_id):
        dropdown_element = self.driver.find_element_by_id(element_id)
        select = Select(dropdown_element)
        # print([option.text for option in select.options])
        options = []
        for option in select.options:
            text = option.text
            if '--Select--' not in text:
                value = option.get_attribute('value')
                options.append(
                    OptionTuple(
                        value=value, text=text, uri_arg=self.convert_text_to_url_text(text)
                    )
                )
        return options

    def parse_all_pages(self):
        # parse base url page
        self.driver.get(self.base_url)
        commodities = self.get_options(element_id=self.commodity_id)
        self.logger.debug('Collected all options for commodities')
        states = self.get_options(element_id=self.state_id)
        self.logger.debug('Collected all options for states')

        # parse listed commodities and all states
        for commodity in commodities:
            if self.commodities_list and commodity.text not in self.commodities_list:
                continue
            for state in states:
                if self.states_list and state.text not in self.states_list:
                    continue
                url = self.generate_url(
                    commodity=commodity.uri_arg, commodity_id=commodity.value,
                    state=state.uri_arg, state_id=state.value
                )
                self.logger.info(f'Collecting data for {commodity.text} from {state.text} through {url}')
                self.driver.get(url)
                self.parse_page()

    def main(self):
        try:
            self.parse_all_pages()
            if not self.output:
                print("No Data found for any combination")
                return
            self.logger.info("Writing data into file")
            dataframe = pd.DataFrame(self.output)
            dataframe.drop(['Sl no.'], axis=1, inplace=True)
            output_file = create_csv(filename=self.output_filename)
            dataframe.to_csv(output_file, index=True, index_label='Sl No.')
            print(f"Data with {len(dataframe)} rows written to {output_file}")
        finally:
            self.driver.quit()


if __name__ == '__main__':
    a = time.time()
    scraper = AgmarknetScraper(days_before=7, verbose=True, healess_browser=True)
    scraper.main()
    b = time.time()
    print(f"Took {b - a} seconds")
