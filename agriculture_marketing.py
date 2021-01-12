import json
import os
import sys
import argparse
import datetime
import time
from collections import namedtuple
from pprint import pprint

import pandas as pd

from bs4 import BeautifulSoup
from selenium.webdriver.support.select import Select

from scrape_helper import init_webdriver
from utils import create_csv, setup_logging

OptionTuple = namedtuple('option', field_names=['value', 'text', 'uri_arg'])


def notify(message):
    sys.stderr.write(message + '\n')


class AgmarknetScraper(object):
    base_url = 'https://agmarknet.gov.in'
    commodity_id = 'ddlCommodity'
    state_id = 'ddlState'
    state_codes_filename = 'StateDistricts.json'
    district_codes_filename = 'StateDistricts.json'
    market_codes_filename = 'DistrictMarkets.json'
    # Leaving commodities_list/states_list to empty list or None will run the script for all commodities/states
    commodities_list = ['Apple', 'Arhar Dal(Tur Dal)', 'Beans', 'Bengal Gram Dal (Chana Dal)', 'Bhindi(Ladies Finger)',
                        'Bitter gourd', 'Carrot', 'Chili Red', 'Coriander(Leaves)', 'Cotton', 'Dry Chillies',
                        'Ginger(Dry)', 'Ginger(Green)', 'Green Chilli', 'Groundnut', 'Potato', 'Spinach',
                        'Tamarind Fruit', 'Tamarind Seed', 'Tomato', 'Turmeric', 'Water Melon']
    states_list = ['Andhra Pradesh', 'Telangana', 'Maharashtra', 'Karnataka', 'Chattisgarh', 'Tamil Nadu',
                   'Uttar Pradesh', 'Madhya Pradesh']
    column_names = [
        'State', 'State Code', 'District Name', 'District Code', 'Market Name',
        'Market Code', 'Commodity', 'Variety', 'Grade', 'Min Price (Rs./Quintal)',
        'Max Price (Rs./Quintal)', 'Modal Price (Rs./Quintal)', 'Price Date'
    ]

    def __init__(self, days_before=7, verbose=True, healess_browser=True):
        self.logger = setup_logging(verbose=verbose, name='argmarknet')
        self.driver = init_webdriver(browser='chrome', headless=healess_browser)
        self.driver.implicitly_wait(10)
        self.errors_count = 0
        self.output = []
        self.start_date = self.stringify_date(days_before=days_before)
        self.end_date = self.stringify_date(days_before=0)
        self.output_filename = f'agmarknet_{self.start_date}_to_{self.end_date}'
        directory_self = os.path.dirname(os.path.abspath(__file__))
        self.data_directory = os.path.join(directory_self, 'data')
        self._code_mapping = None

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

    def parse_each_page(self, state_text):
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
                    elem['State'] = state_text
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
                        return self.parse_each_page(state_text)
                    else:
                        return

    def get_options(self, element_name, element_id, filtered_options=None):
        dropdown_element = self.driver.find_element_by_id(element_id)
        select = Select(dropdown_element)
        # print([option.text for option in select.options])
        options = []
        for option in select.options:
            text = option.text
            if '--Select--' not in text:
                if filtered_options and text not in filtered_options:
                    continue
                value = option.get_attribute('value')
                options.append(
                    OptionTuple(
                        value=value, text=text, uri_arg=self.convert_text_to_url_text(text)
                    )
                )

        assert options, f"No options found for {element_name}. Please check values and re-run with proper values"
        if filtered_options:
            assert len(options) == len(
                filtered_options), f"Some options in {element_name} did not match filtered_options. Please check names provided as options and re-run with proper values"
        return options

    def parse_json(self, jsonfilename, keyname='label', code_name='value'):
        result = {}
        jsonfile = os.path.join(self.data_directory, jsonfilename)
        with open(jsonfile, 'rb') as f:
            data = json.load(f)
            for each_sub_code, sub_data in data.items():
                for item in sub_data:
                    key = item[keyname].replace('\u200e', '')
                    value = item[code_name].replace('\u200e', '')
                    result[key] = value
        return result

    @property
    def code_mapping(self):
        if self._code_mapping is None:
            self._code_mapping = {
                'State': self.parse_json(self.state_codes_filename),
                'District Name': self.parse_json(self.district_codes_filename),
                'Market Name': self.parse_json(self.market_codes_filename),
            }
        return self._code_mapping

    def set_code_value_from_mapping(self, column_name, row):
        key = row.get(column_name)
        if not key:
            return f'Column "{column_name}" not found'
        sub_mapping = self.code_mapping.get(column_name)
        if sub_mapping:
            return sub_mapping.get(key, 'NA')
        return 'NA'

    def parse_all_pages(self, commodities, states):
        # parse listed commodities and all states
        for commodity in commodities:
            for state in states:
                url = self.generate_url(
                    commodity=commodity.uri_arg, commodity_id=commodity.value,
                    state=state.uri_arg, state_id=state.value
                )
                self.logger.info(f'Collecting data for {commodity.text} from {state.text} through {url}')
                self.driver.get(url)
                try:
                    self.parse_each_page(state_text=state.text)
                except Exception as e:
                    self.logger.error(e)
                    notify("exception raised; but still continuing with rest of the combinations")
                    self.errors_count += 1
                    if self.errors_count > 5:
                        notify("Script reported more than 5 errors; so script will stop processing")
                        raise

    def parse(self):
        # ---------------------------------------------------------------
        # get list of states and commodities
        # ---------------------------------------------------------------
        self.driver.get(self.base_url)
        commodities = self.get_options(element_name='commodity', element_id=self.commodity_id,
                                       filtered_options=self.commodities_list)
        states = self.get_options(element_name='state', element_id=self.state_id, filtered_options=self.states_list)
        self.logger.debug('Collected required commodities and states')
        # ---------------------------------------------------------------
        # parse all different combinations and pages
        # ---------------------------------------------------------------
        self.parse_all_pages(commodities, states)

    def process_date(self):
        df = pd.DataFrame(self.output)
        df.drop(['Sl no.'], axis=1, inplace=True)
        df['State Code'] = df.apply(lambda row: self.set_code_value_from_mapping('State', row), axis=1)
        df['Market Code'] = df.apply(lambda row: self.set_code_value_from_mapping('Market Name', row), axis=1)
        df['District Code'] = df.apply(lambda row: self.set_code_value_from_mapping('District Name', row), axis=1)
        df['Price Date'] = pd.to_datetime(df['Price Date']).dt.strftime('%Y-%d-%m')
        # set order of columns
        try:
            df = df[self.column_names]
        except KeyError as e:
            self.errors_count += 1
            notify(f"Unable to set columns order properly. Error: {e}")
        return df

    def write_data(self, dataframe):
        self.logger.info("Writing data into file")
        output_file = create_csv(filename=self.output_filename)
        dataframe.to_csv(output_file, index=True, index_label='Sl No.')
        print(f"Data with {len(dataframe)} rows written to {output_file}")

    def main(self):
        try:
            start_time = time.time()
            self.logger.info(f"Extracting data for following commodities {self.commodities_list}")
            self.logger.info(f"Extracting data for following states {self.states_list}")
            self.parse()
            if not self.output:
                print("No Data found for any combination")
                return
            df = self.process_date()
            self.write_data(df)
        finally:
            self.driver.quit()
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            print(f"Execution took {time_taken} seconds")


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--state', action='append', default=[])
    parser.add_argument('-c', '--commodity', action='append', default=[])
    parser.add_argument(
        '--test', action='store_true', help='Just test code with one commodity and one state'
    )
    parser.add_argument(
        "-d",
        "--days",
        default=7,
        type=int,
        help='start date will be calculated based on this value',
    )
    return parser.parse_args(args)


if __name__ == '__main__':
    # # MAKE SURE SCRIPT IS RAN WITH python 3.6
    interpreter_version_info = sys.version_info
    assert interpreter_version_info.major == 3 and interpreter_version_info.minor == 6, "Run script with python version 3.6"

    args = parse_args(sys.argv[1:])
    print(args)
    scraper = AgmarknetScraper(days_before=args.days, verbose=True, healess_browser=True)
    if args.state:
        scraper.states_list = args.state
    if args.commodity:
        scraper.commodities_list = args.commodity
    if args.test:
        scraper.states_list = ['Telangana']
        scraper.commodities_list = ['Tomato']

    # pprint(scraper.code_mapping)
    scraper.main()
    if scraper.errors_count:
        notify('Some errors encountered')
        sys.exit(1)
