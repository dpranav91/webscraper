import os
import re
import shutil
import pandas as pd
import subprocess
import glob
import datetime
from collections import Counter

csv_path = os.path.join(os.getcwd(), 'csv')
# result_file_path = os.path.join('result', 'final_result.csv')
result_xlsx_path = os.path.join('result', 'final_result.xlsx')


def remove_dir(csv_path):
    if os.path.exists(csv_path):
        shutil.rmtree(csv_path)


def execute_scripts():
    commands = []
    commands.append('python shapiro.py Mecklenburg NC')
    commands.append('python shapiro.py Cabarrus NC')
    commands.append('python brockandscott.py Mecklenburg NC')
    commands.append('python brockandscott.py Cabarrus NC')

    for cmd in commands:
        subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    # execute_scripts()


    today = datetime.datetime.now().strftime('%d_%m_%Y')
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
                     'Misc-1']

    # ADD EXTRA COLUMNS
    result_df = result_df[final_columns].fillna('NA')
    boa_substitute = lambda \
        x: "https://realestatecenter.bankofamerica.com/tools/marketvalue4.aspx?address=" + x.replace(',', '').replace(
        ' ', '+')
    zillow_substitute = lambda x: "https://www.zillow.com/homes/" + x.replace(',', '').replace(' ', '_') + '_rb'
    result_df['Group'] = ''
    result_df['Rating'] = ''
    result_df['BoA'] = result_df['Address'].apply(boa_substitute)
    result_df['Zillow'] = result_df['Address'].apply(zillow_substitute)
    result_df["Flag"] = "Yes"

    preserve_columns_order = result_df.columns.tolist()

    # CONCATENATE NEW RESULT
    if os.path.exists(result_xlsx_path):
        try:
            init_df = pd.read_excel(result_xlsx_path)
        except:
            pass
        else:
            if 'Flag' not in init_df.columns:
                init_df['Flag'] = "No"
            intersection_records = set(result_df['Num']).intersection(set(init_df['Num']))
            new_records = set(result_df['Num']) - set(init_df['Num'])
            set_flag = lambda x: 'Yes' if x['Num'] in intersection_records or \
                                          x['Num'] in new_records else "No"#x['Flag']
            new_records_df = result_df[result_df['Num'].isin(new_records)]
            result_df = pd.concat([init_df, new_records_df])
            result_df['Flag'] = result_df.apply(set_flag,axis=1)

    # SET INDEX
    result_df = result_df[preserve_columns_order]
    result_df = result_df.reset_index(drop=True)
    result_df.index += 1
    result_df.index.name = 'SN'

    # WRITE RESULT TO CSV
    result_df.to_excel(result_xlsx_path)
