import os
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

logger = setup_logging()

csv_path = os.path.join(os.getcwd(), 'csv')
today = datetime.datetime.now().strftime('%d_%m_%Y')
logger.info("\n{}".format(today))
sheet_name = datetime.datetime.now().strftime('Sheet_%m_%Y')
spread_sheet_id = '1uMa11jIIYyKMj2o73fgdHzYI5IUNdPzZzu_pocwoUx0'
result_file_path = os.path.join('result', 'final_result.csv')
if sys.platform.startswith('win'):
    python_interpreter = sys.executable
else:
    python_interpreter = '/home/ec2-user/anaconda3/bin/python'
current_directory = os.path.split(os.path.realpath(__file__))[0]
shapiro_file = os.path.join(current_directory, 'shapiro.py')
brockandscott_file = os.path.join(current_directory, 'brockandscott.py')
HOME_DIRECTORY = os.path.expanduser('~')


# result_file_path = os.path.join('result', 'final_result.xlsx')


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

def execute_scripts():
    cmd1 = ('{python} {shapiro} Mecklenburg NC'.format(python=python_interpreter, shapiro=shapiro_file))
    cmd2 = ('{python} {shapiro} Cabarrus NC'.format(python=python_interpreter, shapiro=shapiro_file))
    cmd3 = ('{python} {brockandscott} Mecklenburg NC'.format(python=python_interpreter, brockandscott=brockandscott_file))
    cmd4 = ('{python} {brockandscott} Cabarrus NC'.format(python=python_interpreter, brockandscott=brockandscott_file))

    for cmd in (cmd1, cmd2, cmd3, cmd4):
        logger.info("Executing `{}`".format(cmd))
        subprocess.call(cmd, shell=True)


if __name__ == '__main__':
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
    for filename, df in res.items():
        if filename.startswith('brockandscott'):
            brockandscott_dfs.append(df)
        if filename.startswith('shapiro'):
            shapiro_dfs.append(df)

    # Formatting brockandscott
    brockandscott = pd.concat(brockandscott_dfs)
    remove_extra_spaces = lambda x: re.sub('\s+', ' ', x)
    brockandscott['Address'] = brockandscott['Address'].apply(remove_extra_spaces)
    brockandscott['Source'] = 'brockandscott'
    columns_rename = {'Bid Amount': 'Price',
                      'Book Page': 'Misc-1',
                      'Case Number': 'Parcel Nu',
                      'County': 'county',
                      'Court SP#': 'Num',
                      'Sale Date & Time': 'Bid Date',
                      'State Code': 'State'}
    brockandscott.rename(columns=columns_rename, inplace=True)

    # Formatting Shapiro
    shapiro = pd.concat(shapiro_dfs)
    columns_rename_shapiro = {'Case #': 'Num',
                              'Open Bid': 'Price',
                              'Property Address': 'Address',
                              'Sale Date - Sale Time': 'Bid Date'}
    shapiro['county'], shapiro['State'] = shapiro['Property County'].str.split(', ').str
    shapiro['Source'] = 'shapiro'
    shapiro.rename(columns=columns_rename_shapiro, inplace=True)

    # INTERMEDIATE FILE TO CSV
    # brockandscott.to_csv(os.path.join('result','brockandscott.csv'))
    # shapiro.to_csv(os.path.join('result', 'shapiro.csv'))

    # RESULT
    result_df = pd.concat([brockandscott, shapiro])
    final_columns = ['county',
                     'Bid Date',
                     'Price',
                     'State',
                     'Num',
                     'Parcel Nu',
                     'Address',
                     'Misc-1',
                     'Source']

    # ADD EXTRA COLUMNS
    result_df = result_df[final_columns].fillna('NA')
    boa_substitute = lambda \
            x: "https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address=" + x.replace(',',
                                                                                                         '').replace(
        ' ', '+')
    zillow_substitute = lambda x: "https://www.zillow.com/homes/" + x.replace(',', '').replace(' ', '_') + '_rb'
    result_df['Group'] = ''
    result_df['Rating'] = ''
    result_df['BoA'] = result_df['Address'].apply(boa_substitute)
    result_df['Zillow'] = result_df['Address'].apply(zillow_substitute)
    result_df["Flag"] = "Yes"

    preserve_columns_order = result_df.columns.tolist()

    # DOWNLOAD EXISTING SPREADSHEET DATA
    logger.info("Trying to read data from GoogleSpreadSheet:{} sheet: {}".format(spread_sheet_id, sheet_name))
    df2google = DF2GoogleSpreadSheet(spreadsheet=spread_sheet_id, sheetname=sheet_name)
    init_df = df2google.download()
    # CONCATENATE NEW RESULT
    if init_df is not None:
        logger.info("Found data from SpreadSheet with {} records".format(len(init_df)))
        if 'Flag' not in init_df.columns:
            init_df['Flag'] = "No"
        intersection_records = set(result_df['Num']).intersection(set(init_df['Num']))
        new_records = set(result_df['Num']) - set(init_df['Num'])
        set_flag = lambda x: 'Yes' if x['Num'] in intersection_records or \
                                      x['Num'] in new_records else "No"  # x['Flag']
        new_records_df = result_df[result_df['Num'].isin(new_records)]
        result_df = pd.concat([init_df, new_records_df])
        result_df['Flag'] = result_df.apply(set_flag, axis=1)

    # SET INDEX
    result_df = result_df[preserve_columns_order]
    result_df = result_df.reset_index(drop=True)
    result_df.index += 1
    result_df.index.name = 'SN'

    # WRITE RESULT TO SPREADSHEET
    logger.info(
        "New result with {} records will be uploaded to SpreadSheet into Sheet:{}".format(len(result_df), sheet_name))
    df2google.upload(result_df)
    logger.info("Upload Successful")