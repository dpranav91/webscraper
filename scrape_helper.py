# -*- coding: utf-8 -*-
import requests
import time
import os
import sys
from selenium import webdriver

from utils import (save_to_csv,
                   setup_logging,
                   convert_to_filenameable,
                   create_csv)


DELAY = 1
scraper_logging = "stdout"  # the other is "file"
current_directory = os.path.split(os.path.realpath(__file__))[0]

def init_webdriver(browser='chrome'):
    if browser=='chrome':
        chromedriver = os.path.join(current_directory,'utilities','chromedriver.exe')
        # print(os.environ["webdriver.chrome.driver"])
        os.environ["webdriver.chrome.driver"] = chromedriver
        driver = webdriver.Chrome(chromedriver)
    else:
        phantomdriver = os.path.join(current_directory,'utilities','phantomjs.exe')
        if sys.platform.startswith('win'):
            driver = webdriver.PhantomJS(phantomdriver)
        else:
            driver = webdriver.PhantomJS()
        driver.set_window_size(1120, 550)
    return driver

class Scraper:
    """
    Base class for scrapers. All bots must inherit from this class

    Parameters:
    -----------
    start_date: str
        string will be a date in mm/dd/yyyy format
    end_date: str
        a valid date in mm/dd/yyyy format
    headers: List[str]
        a list of headers that should be in the csv file
    response: requests.response
        a response object. This is kept so that the previous response can be
        used in the current request as well
    delay: int
        number of seconds that you want the crawler to be delayed by
        This is so that the bot is not flagged and blacklisted.

    Examples:
    ---------
        You can use it as a simple class

        >>> mybot = Scraper("mybot", start_date="2/1/2017", end_date="2/1/2017")

        Or as a context manager

        >>> with Scraper("mybot",
        ...              start_date="2/1/2017",
        ...              end_date="2/1/2017") as mybot:
        ...     # write the code here

    """

    def __enter__(self):
        """the enter method for the context manager"""
        return self

    def __exit__(self, *_args):
        """the exit method for the context manager"""
        pass

    def __init__(self, name, start_date=None, end_date=None,
                 headers=None, response=None, delay=DELAY, log=None,
                 proxies=None, bot_last_status=None,
                 requests=requests, *args, **kwargs):
        # the name of the package is used to resolve resources from inside the
        # package or the folder the module is contained in the resolve.
        self.name = name

        # start date and end date is needed so that the parser is able to have a
        # set time limit within which the bot will parse the data in the pages.
        # This is also needed for giving the determining the name of the csv
        # files and the log files where the respective information will go.
        self.start_date = start_date
        self.end_date = end_date

        # This will need to be defined by the user, as he would have already
        # seen the page and would have a clear picture about the headers that
        # should be there in the csv file
        # self.headers = UserAgentRotator().generate_header()
        self.headers = header = {
            "Connection": "close",
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"
        }

        # The class that is used for response objects. In the present scenario
        # this is a response object of the requests class.
        self.response = response

        # a filename will need to be decided that will define the file names
        # that will be there
        filename = self.name

        # log handler is set, where the file name is based on the starting date
        # and the name of the bot as given by the user. if the logging flag is
        # set to stdout, log file is not initialised and the stdout is to
        # stdout.
        log_date = convert_to_filenameable(self.start_date)
        self.log = log

        filename = "{filename}_{log_date}".format(filename=filename,
                                                  log_date=log_date)
        if scraper_logging == "stdout":
            log_file = None
        elif scraper_logging == "file":
            log_file = "log/{filename}.log".format(filename=filename)
        else:
            raise ValueError("please set correct logging flag for"
                             "scraper_logging")
        if log_date:
            self.log = setup_logging(log_file)
        else:
            raise ValueError("cannot create log file, "
                             "log date is not resolved. "
                             "log_date: {log_date}".format(log_date=log_date))

        # a delay of `DELAY` seconds will be set for the bot. This is 1 second
        # by default. You can change this by changing the delay parameter.
        self.delay = delay

        # an instance will have a default proxy that
        # will be fixed for the particular instance and will act as a random
        # agent for the bot
        if not proxies:
            self.proxies = None #ProxyRotator().proxies
        else:
            self.proxies = proxies

        # create a csv file if it does not exist. Also check if there is a csv
        # file that already exists.
        self.csvfile = create_csv(filename)

        # will have a definition for bot last status to keep a track of the last
        # status of the bot. This will be a dictionary
        self.bot_last_status = bot_last_status

        # dependency injection for requests
        self.requests = requests

    def scrape(self, url=None, params=None, cookies=None, **kwargs):
        """
        A decorator that is used to register a scrape function for a
        given URL.

             @webscraper_pack.scrape(url, params)
             def parse_page():
                 data = webscraper_pack.response.text
                 return data

        Parameters:
        -----------
        url: str
            the URL rule as string
        params: dict(str: str)
            a dict object containing the parameters to be given to requests for
            the next post request.
        """
        def decorator(f):
            # we will make use of the request lib here
            # this is taken a design choice as the urls we want to use are more
            # of server side rendering with less or almost no js
            if url:
                self.response = self.requests_response(url, params, cookies)

            return f
        return decorator

    def requests_response(self, url,
                          params=None, cookies=None):
        """Returns the response object. It will either do a post based on
        whether there are params and cookies passed or not, or will do a simple
        get request. This is the implementation of scrape as a method.

        :param url: the URL rule as string
        :param params: a dict object containing the parameters to be given to
                       requests for the next post request.

        """
        log_first_part = "sending request to {url}".format(url=url)
        if params and cookies:
            log_sec_part = "with {params} and {cookies}".format(params=params,
                                                                cookies=cookies)
            self.log.debug(" ".join([log_first_part, log_sec_part]))
            time.sleep(self.delay)
            return self.requests.post(url,
                                      params=params,
                                      cookies=cookies,
                                      headers=self.headers,
                                      proxies=self.proxies)
        else:
            self.log.debug(log_first_part)
            time.sleep(self.delay)
            return self.requests.get(url, headers=self.headers,
                                     proxies=self.proxies)

    def _save_records_to_csv(self, records):
        """
        This will take the records and save it to a csv file

        Parameters:
        -----------'
        records: List[dict]

        Returns:
        -------
        path: str
            This will return the path of the csv file where the records has been
            saved
        """
        if records:
            try:
                path = save_to_csv(self.headers, self.csvfile, records)
                # this is a function that has a side effect
                # that is it stores the records to a file
                # so we return a json to say that the file is saved and the path
                # is this. Also additional information are given like the
                # headers and the date. This is mainly to save the information
                # to a log file later we will assert to check if this is the
                # same csv file was used to write the data
                assert self.csvfile == path

                self.log.debug("csv file {path}".format(path=path))
                return path
            except TypeError:
                information = "cannot save to csv as start date is not set"
                self.log.debug(information)
                raise ValueError(information)
            except AttributeError as e:
                p = "the return value of the functions has to be an iterable"
                self.log.debug(p)
                raise ValueError(p)

    def _execute(self, fn):
        try:
            records = fn()
            return records
        except AttributeError:
            # this has to be laced with meaningful exceptions
            information = " ".join(["the function ",
                                    "{fn_name}".format(fn_name=fn.__name__),
                                    "has a return value that is wrong.",
                                    "It should be dict ",
                                    "please check"])
            self.log.debug(information)
            raise ValueError(information)

    def run(self, fn_list):
        """Run the parsing functions that are defined by the user

        Parameters:
        -----------
        fn_list: List[function]
            a list of functions. The sequence will be in which the user wants to
            execute it.

        Returns:
        --------
        return_values: None

        Examples:
        ---------
        >>> fn_list = [parse1, parse2, parse3]
        >>> mybot.run(fn_list)
        """
        records = map(self._execute, fn_list)

        # remove the null values, clean the data
        records = [x for x in records if x is not None]

        for record in records:
            self._save_records_to_csv(list(record))

        self.bot_last_status = {"path": self.csvfile, "date": self.start_date,
                                "headers": self.headers}
        self.log.debug(self.bot_last_status)
