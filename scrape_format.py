import os
import shutil
import pandas as pd
import subprocess
import glob
import datetime

csv_path = os.path.join(os.getcwd(), 'csv')
today = datetime.datetime.now().strftime('%d-%m-%Y')
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

    print(os.path.join(csv_path, '*' + today + '*'))
    result_files = glob.glob(os.path.join(csv_path, '*'))
    print(result_files)

    res=dict()
    for result in result_files:
        variable = os.path.splitext(os.path.basename(result))[0]
        res[variable] = pd.read_csv(result)
    print(res)

    brockandscott_dfs = []
    shapiro_dfs = []
    for filename, df in res.items():
        if filename.startswith('brockandscoott'):
            brockandscott_dfs.append(df)
        if filename.startswith('shapiro'):
            shapiro_dfs.append(df)

    brockandscott = pd.concat(brockandscott_dfs)
    shapiro = pd.concat(shapiro_dfs)
    brockandscott.to_csv(os.path.join('csv','brockandscott.csv'))
    shapiro.to_csv(os.path.join('csv', 'shapiro.csv'))
    res = brockandscott.merge(shapiro, left_on='Address', right_on='Property Address', how='outer')
    res.to_csv(os.path.join('csv', 'final_result.csv'))