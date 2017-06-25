import os
import pdb
import sys
import re
import shutil
import pandas as pd
import subprocess
import glob
import datetime
from collections import Counter
from df2google import DF2GoogleSpreadSheet
from utils import setup_logging

pd.options.mode.chained_assignment = None
logger = setup_logging()

CWD = os.path.split(os.path.abspath(__file__))[0]
csv_path = os.path.join(CWD, 'csv')
datetime_today = datetime.datetime.now()
today = datetime_today.strftime('%d_%m_%Y')
today_time = datetime_today.strftime('%m-%d-%Y %H:%M')

logger.info("\n{}".format('*' * 50))
# sheet_name = datetime.datetime.now().strftime('Sheet_%m_%Y')
sheet_name = 'Current'
spread_sheet_id = '1kZvZn__U62ZMytci3je8cZ-TLNmRtdtuFI0avzqK75c'  # '1uMa11jIIYyKMj2o73fgdHzYI5IUNdPzZzu_pocwoUx0'
result_file_path = os.path.join(CWD, 'result', 'final_result.csv')
if sys.platform.startswith('win'):
    spread_sheet_id = '1uMa11jIIYyKMj2o73fgdHzYI5IUNdPzZzu_pocwoUx0'
    python_interpreter = sys.executable
else:
    python_interpreter = '/home/ec2-user/anaconda3/bin/python'
current_directory = os.path.split(os.path.realpath(__file__))[0]
shapiro_file = os.path.join(current_directory, 'shapiro.py')
brockandscott_file = os.path.join(current_directory, 'brockandscott.py')
hutchenslawfirm_file = os.path.join(current_directory, 'hutchenslawfirm.py')

HOME_DIRECTORY = os.path.expanduser('~')

# result_file_path = os.path.join('result', 'final_result.xlsx')
boa_url = "https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address="
zillow_url = "https://www.zillow.com/homes/"
maps_url = "https://www.google.com/maps/place/"
boa_substitute = lambda x: boa_url + str(x).replace(',', '').replace(' ', '+')

zillow_substitute = lambda x: zillow_url + str(x).replace(',', '').replace(' ', '_') + '_rb'

map_substitute = lambda x: maps_url + str(x).replace(',', '').replace(' ', '+')

remove_extra_spaces = lambda x: re.sub('\s+', ' ', str(x))


def remove_dir(csv_path):
    if os.path.exists(csv_path):
        shutil.rmtree(csv_path)


def copy_gdrive_private_file():
    drive_private = os.path.join(HOME_DIRECTORY, '.gdrive_private')
    if not os.path.exists(drive_private):
        src = os.path.join('private', '.gdrive_private')
        dst = drive_private
        shutil.copy(src, dst)
        logger.info("gdrive_private file placed in HOME directory")


def update_dfs(initial_df, updated_df, key):
    # initial_df = initial_df.sort_values('Source').reset_index().groupby('Num', group_keys=False).last()
    # updated_df = updated_df.sort_values('Source').reset_index().groupby('Num', group_keys=False).last()
    initial_df = initial_df.set_index(key)
    updated_df = updated_df.set_index(key)

    initial_df.update(updated_df) # ERROR
    initial_df.reset_index(inplace=True)
    initial_df['Updated Date'] = today_time
    return initial_df


def parse_bid_date(date):
    try:
        return ' '.join(re.compile('(\d+?/\d+?/\d+?)[\s-]*(\d+?:\d{2}).*').search(date).groups())
    except:
        return ' '.join(re.compile('(\d+?/\d+?/\d+)[\s-]*').search(date).groups())


def execute_scripts():
    commands = []
    # SHAPIRO
    commands.append(
        '{python} {shapiro} Mecklenburg NC upcoming_sales'.format(python=python_interpreter, shapiro=shapiro_file))
    commands.append(
        '{python} {shapiro} Cabarrus NC upcoming_sales'.format(python=python_interpreter, shapiro=shapiro_file))

    # SHAPIRO (SALES_HELD)
    commands.append(
        '{python} {shapiro} Mecklenburg NC sales_held'.format(python=python_interpreter, shapiro=shapiro_file))
    commands.append('{python} {shapiro} Cabarrus NC sales_held'.format(python=python_interpreter, shapiro=shapiro_file))

    # BROCKANDSCOTT
    commands.append(
        '{python} {brockandscott} Mecklenburg NC'.format(python=python_interpreter, brockandscott=brockandscott_file))
    commands.append(
        '{python} {brockandscott} Cabarrus NC'.format(python=python_interpreter, brockandscott=brockandscott_file))
    # HUTCHENSLAWFIRM
    commands.append(
        '{python} {hutchenslawfirm} Cabarrus'.format(python=python_interpreter, hutchenslawfirm=hutchenslawfirm_file))
    commands.append(
        '{python} {hutchenslawfirm} Mecklenburg'.format(python=python_interpreter,
                                                        hutchenslawfirm=hutchenslawfirm_file))
    for cmd in commands:
        logger.info("Executing `{}`".format(cmd))
        subprocess.call(cmd, shell=True)


def prepare_new_records_for_concatenation(init_df, current_run_data_df):
    init_df['Num'] = init_df['Num'].str.replace(' ', '')
    logger.info("Found data from SpreadSheet with {} records".format(len(init_df)))
    if 'Flag' not in init_df.columns:
        init_df['Flag'] = "No"
    intersection_records = set(current_run_data_df['Num']).intersection(set(init_df['Num']))
    new_records = set(current_run_data_df['Num']) - set(init_df['Num'])
    set_flag = lambda x: 'Yes' if x['Num'] in intersection_records or \
                                  x['Num'] in new_records else "No"  # x['Flag']

    # ------------------------------------------
    # SETUP NEW RECORDS DF
    # ------------------------------------------
    new_records_df = current_run_data_df[current_run_data_df['Num'].isin(new_records)]
    # ADD EXTRA COLUMNS
    new_records_df['Inserted Date'] = today_time
    new_records_df['Updated Date'] = today_time
    # result_df = result_df[final_columns].fillna('NA')
    # new_records_df['Group'] = ''
    # new_records_df['Rating'] = ''
    new_records_df['BoA'] = new_records_df['Address'].apply(boa_substitute)
    new_records_df['Zillow'] = new_records_df['Address'].apply(zillow_substitute)
    new_records_df['Location'] = new_records_df['Address'].apply(map_substitute)
    new_records_df["Flag"] = "Yes"

    # Add empty values to missing columns
    missing_columns_from_result_df = set(init_df.columns) - set(new_records_df.columns)
    for col in missing_columns_from_result_df:
        new_records_df[col] = ''

    # UPDATING INITIAL DF with updated data
    init_df = update_dfs(init_df, current_run_data_df, 'Num')
    result_df = pd.concat([init_df, new_records_df])
    result_df['Flag'] = result_df.apply(set_flag, axis=1)
    return result_df


def reformat_shapiro_salesheld(shapiro_salesheld_dfs):
    shapiro_salesheld = pd.concat(shapiro_salesheld_dfs)
    shapiro_salesheld.fillna("", inplace=True)
    shapiro_salesheld = shapiro_salesheld[shapiro_salesheld['Property County'] != 'NO MATCHES FOUND']
    # split Property County to two different columns
    shapiro_salesheld['county'], shapiro_salesheld['State'] = shapiro_salesheld['Property County'].str.split(', ').str
    shapiro_salesheld['Source'] = 'shapiro-salesheld'
    shapiro_salesheld['Upset Info'] = shapiro_salesheld['Last Upset'] + ';' + shapiro_salesheld['Sucessful Bidder']

    # rename columns
    columns_rename_shapiro = {'Case #': 'Num',
                              'High Bid': 'Price',
                              'Property Address': 'Address',
                              'Sale Date': 'Bid Date',
                              }
    shapiro_salesheld.rename(columns=columns_rename_shapiro, inplace=True)
    shapiro_salesheld['Num'] = shapiro_salesheld['Num'].str.replace(' ', '')
    return shapiro_salesheld


def reformat_shapiro(shapiro_dfs):
    shapiro = pd.concat(shapiro_dfs)
    shapiro.fillna("", inplace=True)
    shapiro = shapiro[shapiro['Property County'] != 'NO MATCHES FOUND']
    # split Property County to two different columns
    shapiro['county'], shapiro['State'] = shapiro['Property County'].str.split(', ').str
    shapiro['Source'] = 'shapiro'
    # rename columns
    columns_rename_shapiro = {'Case #': 'Num',
                              'Open Bid': 'Price',
                              'Property Address': 'Address',
                              'Sale Date - Sale Time': 'Bid Date'}
    shapiro.rename(columns=columns_rename_shapiro, inplace=True)
    shapiro['Num'] = shapiro['Num'].str.replace(' ', '')
    return shapiro


def reformat_brockandscott(brockandscott_dfs):
    brockandscott = pd.concat(brockandscott_dfs)
    brockandscott.fillna("", inplace=True)
    # remove extra spaces from Address
    brockandscott['Address'] = brockandscott['Address'].apply(remove_extra_spaces)
    brockandscott['Source'] = 'brockandscott'
    # rename columns
    columns_rename = {'Bid Amount': 'Price',
                      'Book Page': 'Misc-1',
                      'Case Number': 'Parcel Nu',
                      'County': 'county',
                      'Court SP#': 'Num',
                      'Sale Date & Time': 'Bid Date',
                      'State Code': 'State'}
    brockandscott.rename(columns=columns_rename, inplace=True)
    brockandscott['Num'] = brockandscott['Num'].str.replace(' ', '')
    return brockandscott

# TODO: remove `No records to display` records
def reformat_hutchenslawfirm(hutchenslawfirm_dfs):
    # Formatting Hutchenslawfirm
    hutchenslawfirm = pd.concat(hutchenslawfirm_dfs)
    hutchenslawfirm.fillna("", inplace=True)
    hutchenslawfirm['Source'] = 'hutchens'
    hutchenslawfirm['county'], hutchenslawfirm['State'] = hutchenslawfirm['County'].str.split(', ').str
    columns_rename = {'SP#': 'Num',
                      # 'County': 'county',
                      'Sale Date': 'Bid Date',
                      'Deed of Trust Book/Page': 'Misc-1',
                      'Bid Amount': 'Price'}
    hutchenslawfirm['Address'] = hutchenslawfirm['Property Address'] + ' ' + hutchenslawfirm['Property CSZ']
    hutchenslawfirm.rename(columns=columns_rename, inplace=True)
    hutchenslawfirm['Num'] = hutchenslawfirm['Num'].str.replace(' ', '')
    return hutchenslawfirm

# TODO: DELETE `NO MATCHES FOUND` records
def main():
    execute_scripts()

    copy_gdrive_private_file()
    # today = '06_05_2017'
    result_files = glob.glob(os.path.join(csv_path, '*'))
    result_files = [i for i in result_files if re.search('_' + today, i)]
    if not result_files:
        raise Exception("No Files found for {}".format(today))
    res = dict()
    for result in result_files:
        variable = os.path.splitext(os.path.basename(result))[0]
        res[variable] = pd.read_csv(result)

    # OBTAIN shapiro related files into one df and brockandscott into one
    brockandscott_dfs = []
    shapiro_dfs = []
    shapiro_salesheld_dfs = []

    hutchenslawfirm_dfs = []
    for filename, result_df in res.items():
        if filename.startswith('brockandscott'):
            brockandscott_dfs.append(result_df)
        elif filename.startswith('shapiro-salesheld'):
            shapiro_salesheld_dfs.append(result_df)
        elif filename.startswith('shapiro'):
            shapiro_dfs.append(result_df)
        elif filename.startswith('hutchenslawfirm'):
            hutchenslawfirm_dfs.append(result_df)

    # ------------------------------------------------------
    # Formatting brockandscott
    # ------------------------------------------------------
    brockandscott = reformat_brockandscott(brockandscott_dfs)

    # ------------------------------------------------------
    # Formatting Shapiro
    # ------------------------------------------------------
    shapiro = reformat_shapiro(shapiro_dfs)
    shapiro_salesheld = reformat_shapiro_salesheld(shapiro_salesheld_dfs)

    # ------------------------------------------------------
    # Formatting Hutchenslawfirm
    # ------------------------------------------------------
    hutchenslawfirm = reformat_hutchenslawfirm(hutchenslawfirm_dfs)

    # ------------------------------------------------------
    # INTERMEDIATE FILE TO CSV
    # ------------------------------------------------------
    # brockandscott.to_csv(os.path.join('result','brockandscott.csv'))
    # shapiro.to_csv(os.path.join('result', 'shapiro.csv'))

    # ------------------------------------------------------
    # Concat Brockandscot and Shapiro current execution result
    # ------------------------------------------------------
    current_run_data_df = pd.concat([brockandscott, shapiro, shapiro_salesheld, hutchenslawfirm])
    current_run_data_df.fillna("", inplace=True)
    preserve_columns_order = ['county', 'Bid Date', 'BidDate_Formatted',
                              'Price',
                              'State', 'Num', 'Parcel Nu',
                              'Address', 'Misc-1', 'Source',
                              'Group', 'Rating', 'BoA',
                              'Zillow', 'Location', 'Inserted Date',
                              'Updated Date', 'Flag'
                              ]

    # ------------------------------------------------------
    # DOWNLOAD EXISTING SPREADSHEET DATA
    # ------------------------------------------------------
    logger.info("Trying to read data from GoogleSpreadSheet:{} sheet: {}".format(spread_sheet_id, sheet_name))
    try:
        df2google = DF2GoogleSpreadSheet(spreadsheet=spread_sheet_id, sheetname=sheet_name)
        init_df = df2google.download()
    except Exception as e:
        raise Exception("Unable to download spreadsheet: {}".format(e))

    # ------------------------------------------------------
    # If No data from Google spreadsheet, create empty dataframe
    # ------------------------------------------------------
    if init_df is None:
        init_df = pd.DataFrame(columns=preserve_columns_order)
        logger and logger.error("No data obtained from Google spreadsheet")

    # ------------------------------------------------------
    # Move existing data to new sheet if new month starts
    # ------------------------------------------------------
    if datetime_today.day == 1 and datetime_today.hour < 1:
        new_sheet_name = 'Sheet_{}_{}'.format(datetime_today.month - 1, datetime_today.year)
        logger.info(
            "New Month Started, moving existing data to new Sheet:{} and emptying existing data".format(new_sheet_name))
        df2google.upload(init_df, new_sheet_name)
        init_df = pd.DataFrame(columns=preserve_columns_order)

    # ------------------------------------------------------
    # Concatenate New Data and Existing Data
    # ------------------------------------------------------
    result_df = prepare_new_records_for_concatenation(init_df, current_run_data_df)

    # SET INDEX
    try:
        result_df['BidDate_Formatted'] = result_df['Bid Date'].apply(parse_bid_date)
        result_df['BidDate_Formatted'] = pd.to_datetime(result_df['BidDate_Formatted'])
        result_df = result_df.sort_values('BidDate_Formatted')
    except:
        logger.info("Unable to sort by Bid Date")

    # SET INDEX
    result_df.reset_index(drop=True, inplace=True)
    result_df.index += 1
    # result_df.index.name = 'SN'
    result_df['SN'] = result_df.index

    # ------------------------------------------------------
    # SET COLUMN ORDER
    # ------------------------------------------------------
    add_quotes_to_data = lambda x: "'{}".format(str(x).strip('"').strip("'"))
    for col in ['Bid Date', 'Updated Date', 'Inserted Date', 'BidDate_Formatted']:
        result_df[col] = result_df[col].apply(add_quotes_to_data)

    result_df = result_df[preserve_columns_order]
    result_df.fillna("", inplace=True)

    # print(result_df)
    # assert 1 == 2
    # ------------------------------------------------------
    # WRITE RESULT TO SPREADSHEET
    # ------------------------------------------------------
    logger.info(
        "New result with {} records will be uploaded to SpreadSheet into Sheet:{}".format(len(result_df), sheet_name))
    df2google.upload(result_df, sheet_name)
    logger.info("Upload Successful")


if __name__ == '__main__':
    main()
