import re
import time
import sys
import datetime
from bs4 import BeautifulSoup
from scrape_helper import Scraper


today = datetime.datetime.now().strftime('%d/%m/%Y')
# print(sys.argv)
base_url = 'https://www.shapiro-ingle.com/sales.aspx?SubmitBtn=Search&sort=sale_date&db={db}&county={country}&state={state}'
COUNTY = sys.argv[1] if len(sys.argv) > 1 else 'Mecklenburg'# Cabarrus, Mecklenburg
STATE = sys.argv[2] if len(sys.argv)>2 else 'NC'
DB = sys.argv[3] if len(sys.argv)>3 else 'upcoming_sales' # sales_held, upcoming_sales

# we initialise a bot santa that will have run the parsing functions
scraper_prefix = 'shapiro' if DB == 'upcoming_sales' else 'shapiro-salesheld'
scraper_name = "{}_{}".format(scraper_prefix, COUNTY.lower())
shapiro = Scraper(scraper_name, start_date=today, end_date=today)

shapiro_args = {}
# FIRST PAGE
shapiro_args['page1'] = {}
shapiro_args['page1']['url'] = base_url.format(country=COUNTY, state=STATE, db=DB)
shapiro_args['page1']['params'] = None
# below write the parsing functions for the data in the webpages for each web
# page
@shapiro.scrape(shapiro_args["page1"]["url"])
def parse_page1():
    soup = BeautifulSoup(shapiro.response.text, "html.parser")

    table = soup.select("table")
    assert len(table) == 1, "No tabular data found. Unexpected page!"
    table = table[0]
    for row_index, row in enumerate(table.find_all('tr')):
        # set header
        # -------------
        if row_index==0:
            headers = []
            for col in row.find_all('td'):
                headers.append(col.get_text().strip())
            shapiro.headers = headers

        else:
            # # table data
            # # --------------
            cols = []
            for col in row.find_all('td'):
                cols.append(col.get_text().strip())
            elem= dict(zip(shapiro.headers, cols))
            yield elem

# put the functions in a list where the sequence should be in the order that you
# want the bot to crawl through the pages
parse_functions = [parse_page1]

if __name__ == "__main__":
    shapiro.run(parse_functions)
