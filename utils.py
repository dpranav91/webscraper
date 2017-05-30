import os
import argparse
import logging
import sys
from csv import DictWriter

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


def get_standard_arg_parser(program_name):
    '''
    This function set-ups a parser for command line arguments
    '''
    parser = argparse.ArgumentParser(prog='PROG')

    parser.add_argument('-f', '--from-date', default='01/01/2016',
                        help='input from date for scraping (MM/DD/YYYY)')
    parser.add_argument('-t', '--to-date', default='12/31/2016',
                        help='input to date for scraping (MM/DD/YYYY)')
    parser.add_argument('-n', '--num-of-threads', default=1, type=int,
                        help='number of threads to be used')
    parser.add_argument('-l', '--logfile', default=None,
                        help='output file path for logging')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='verbose output')

    return parser


def setup_logging(logfile=None, verbose=False):
    '''
    This function sets up the logger used by webscraper_pack depending on the
    setting provided by the user.
    '''
    standard_log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s[%(funcName)s:"
        "%(lineno)s] - %(levelname)s - %(message)s")
    if logfile:
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(standard_log_formatter)
    root = logging.getLogger()
    root.addHandler(handler)
    # root.addHandler(handler)
    level = logging.INFO
    if verbose:
        level = logging.DEBUG
    root.setLevel(level)
    # root.setLevel(level)
    root.debug("starting up logging")
    return root


def setup_date_range(start_date, end_date):
    '''
    This function setups the dates provided by the user and provides
    the datetime range

    Parameters:
    -----------
    start_date: str
        start date in a normal format
    end_date: str
        end date in a normal everyday format

    Returns:
    --------
    tuple(datetime, datetime)
        Will give a tuple of two datetime objects
        with the startdate and enddate

    Examples:
    ---------
        >>> setup_date_range(start_date="1/1/2017", end_date="1/2/2017")
        (datetime.date(2017, 1, 1), datetime.date(2017, 1, 2))
        >>> setup_date_range(start_date="Jan 1, 2017", end_date="Jan 2. 2017")
        (datetime.date(2017, 1, 1), datetime.date(2017, 1, 2))
        >>> setup_date_range(start_date="Jan 1, 2017", end_date="Jan 2, 2017")
        (datetime.date(2017, 1, 1), datetime.date(2017, 1, 2))
    '''
    if start_date:
        start_date = parse_date(start_date)
    else:
        tmp_date = datetime.now().date()
        start_date = tmp_date-timedelta(days=30)

    if end_date:
        end_date = parse_date(end_date)
    else:
        end_date = datetime.now().date()

    if start_date > end_date:
        start_date, end_date = end_date, start_date

    return start_date, end_date


def parse_date(date, to_string=False):
    '''
    This function parses a given date in strings

    Parameters
    ----------
    date: str
        normal date formats used in documents
    to_string: bool
        flag to give output in date format or string

    Returns:
    --------
    datetime object or string
        depending on the to_string flag is passed or not.

    Examples:
    ---------
        >>> parse_date("1/1/2017")
        datetime.date(2017, 1, 1)
        >>> parse_date("Jan 1, 2017")
        datetime.date(2017, 1, 1)
        >>> parse_date("1/1/2017", to_string=True)
        '01_01_2017'
    '''
    if to_string:
        return '{:%m_%d_%Y}'.format(parse(date).date())
    else:
        return parse(date).date()


def file_is_empty(path):
    '''
    This function checks if a file is empty
    '''
    return os.stat(path).st_size == 0


def create_csv(filename):
    '''
    This function checks if the csv containing permits is already existing

    To Do: remove the touch based linux functions and replace them with the
    os module that is more battle tested. Look into the best practices and
    thoroughly test it.

    Parameters
    ----------
    filename: str
    '''
    filename = '{filename}.csv'.format(filename=filename)
    directory = os.path.join(os.getcwd(),'csv')
    new_dir_made = False

    if not os.path.isdir(directory):
        os.makedirs(directory)
        new_dir_made = True

    path = os.path.join(directory,filename)
    # we will create a csv file and truncate also truncate the file if it
    # already exists
    with open(path, "w") as f:
        f.truncate()

    return path



def save_to_csv(headers, filename, record):
    '''
    This function saves a record by appending it to a csv file
    It takes both a batch list file as well as generator.
    '''
    with open(filename, 'a') as csvfile:
        writer = DictWriter(csvfile, fieldnames=headers)
        if file_is_empty(path=filename):
            writer.writeheader()
        writer.writerows(record)

    return filename


def convert_to_filenameable(invalid_str: str):
    try:
        valid_string = invalid_str.replace("/", "_")
    except AttributeError:
        # valid string is kept None because the next line in Scraper class
        # checks if the string is returned
        valid_string = None
    return valid_string
