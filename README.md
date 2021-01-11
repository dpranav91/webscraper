# Agriculture Marketing:
## First Time Setup
#### clone repo
> git clone https://github.com/dpranav91/webscraper.git

#### checkout to different branch (if branch is not merged to master)
> git checkout agriculture-marketing

#### change directory
> cd webscraper

#### create virtual env if virtual env is not created yet (this is for first time setup) 
##### NOTE: Use python3.6
> mkvirtualenv webscraper
> setvirtualenvproject

#### install required packages
> ./update_requirements

## When Setup Is Already Created
#### activate virtual env that was created earlier using below command
> workon webscraper


## RUNNER
#### run agriculture_marketing to collect tabular data from agmarknet.gov.in
> python agriculture_marketing.py

- By default script with consider start date as 7 days prior to today's date. In case you want to fetch data for different number of days, pass the value as an argument to agriculture_marketing.py.
Eg.: python agriculture_marketing.py 3 (This will collect data for only 3 days)

- Output will be stored as csv file and created under webscraper/csv/ path. Filename will be agmarknet_{startdate}_to_{enddate}.

- Sample console output
```
[vagrant@localhost webscraper]$ python agriculture_marketing.py 3
2021-01-11 08:09:30,275 - argmarknet[setup_logging:56] - DEBUG - starting up logging
2021-01-11 08:09:43,238 - argmarknet[main:138] - DEBUG - Collected required commodities and states
2021-01-11 08:09:43,238 - argmarknet[parse_all_pages:117] - INFO - Collecting data for Apple from Andhra Pradesh through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=17&Tx_State=AP&Tx_District=0&Tx_Market=0&DateFrom=08-Jan-2021&DateTo=11-Jan-2021&Fr_Date=08-Jan-2021&To_Date=11-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Apple&Tx_StateHead=Andhra+Pradesh&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-11 08:09:47,137 - argmarknet[parse_page:80] - DEBUG - No tabular data available
2021-01-11 08:09:47,137 - argmarknet[parse_all_pages:117] - INFO - Collecting data for Apple from Chattisgarh through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=17&Tx_State=CG&Tx_District=0&Tx_Market=0&DateFrom=08-Jan-2021&DateTo=11-Jan-2021&Fr_Date=08-Jan-2021&To_Date=11-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Apple&Tx_StateHead=Chattisgarh&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-11 08:09:50,964 - argmarknet[parse_all_pages:117] - INFO - Collecting data for Arhar Dal(Tur Dal) from Andhra Pradesh through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=260&Tx_State=AP&Tx_District=0&Tx_Market=0&DateFrom=08-Jan-2021&DateTo=11-Jan-2021&Fr_Date=08-Jan-2021&To_Date=11-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Arhar+Dal(Tur+Dal)&Tx_StateHead=Andhra+Pradesh&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-11 08:09:53,124 - argmarknet[parse_page:80] - DEBUG - No tabular data available
2021-01-11 08:09:53,124 - argmarknet[parse_all_pages:117] - INFO - Collecting data for Arhar Dal(Tur Dal) from Chattisgarh through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=260&Tx_State=CG&Tx_District=0&Tx_Market=0&DateFrom=08-Jan-2021&DateTo=11-Jan-2021&Fr_Date=08-Jan-2021&To_Date=11-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Arhar+Dal(Tur+Dal)&Tx_StateHead=Chattisgarh&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-11 08:09:56,129 - argmarknet[parse_page:80] - DEBUG - No tabular data available
2021-01-11 08:09:56,129 - argmarknet[main:150] - INFO - Writing data into file
Data with 7 rows written to /home/vagrant/webscraper/csv/agmarknet_08-Jan-2021_to_11-Jan-2021.csv
Execution took 24.77232003211975 seconds
```
- Sample output file content
```
[vagrant@localhost webscraper]$ cat /home/vagrant/webscraper/csv/agmarknet_08-Jan-2021_to_11-Jan-2021.csv
Sl No.,District Name,Market Name,Commodity,Variety,Grade,Min Price (Rs./Quintal),Max Price (Rs./Quintal),Modal Price (Rs./Quintal),Price Date
0,Durg,Durg,Apple,Apple,Medium,8000,10000,9000,10 Jan 2021
1,Durg,Durg,Apple,Apple,Medium,10000,12000,11000,09 Jan 2021
2,Durg,Durg,Apple,Apple,Medium,8000,12000,10000,08 Jan 2021
3,Rajnandgaon,Rajnandgaon,Apple,Apple,Medium,6400,6400,6400,09 Jan 2021
4,Rajnandgaon,Rajnandgaon,Apple,Apple,Medium,7200,7200,7200,08 Jan 2021
5,Bilaspur,Tiphra,Apple,Apple,Large,8000,8000,8000,09 Jan 2021
6,Bilaspur,Tiphra,Apple,Apple,Large,8200,8200,8200,08 Jan 2021
```