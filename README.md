# webscraper
Scrape website with requests, selenium and beautiful soup

# FIRST TIME SETUP
# -------------------
## clone repo
> git clone https://github.com/dpranav91/webscraper.git

## checkout to different branch (if branch is not merged to master)
> git checkout agriculture-marketing

## change directory
> cd webscraper

## Create virtual env if virtual env is not created yet (this is for first time setup) 
### NOTE: Use python3.6
> mkvirtualenv webscraper
> setvirtualenvproject

## install required packages
> ./update_requirements

# IF SETUP IS ALREADY CREATED
# -----------------------------
## activate virtual env that was created earlier using below command
> workon webscraper


# RUNNER
## Run agriculture_marketing to collect tabular data from agmarknet.gov.in
> python agriculture_marketing.py

- By default script with consider start date as 7 days prior to today's date. In case you want to fetch data for different number of days, pass the value as an argument to agriculture_marketing.py.
Eg.: python agriculture_marketing.py 3 (This will collect data for only 3 days)

- Output will be stored as csv file and created under webscraper/csv/ path. Filename will be agmarknet_{startdate}_to_{enddate}.
Eg. from console output: Data with 7 rows written to /home/vagrant/webscraper/csv/agmarknet_08-Jan-2021_to_11-Jan-2021.csv 
