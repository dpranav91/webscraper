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

- By default script with consider start date as 7 days prior to today's date. 
- To extract data for different number of days, run script as follows:
    > python agriculture_marketing.py -d 3 (This will collect data for past 3 days)

- By default script will collect data for states and commodities listed below:
    ```
    commodities_list = ['Apple', 'Arhar Dal(Tur Dal)', 'Beans', 'Bengal Gram Dal', 'Bhindi(Ladies Finger)',
                        'Bitter gourd', 'Carrot', 'Chili Red', 'Coriander(Leaves)', 'Cotton', 'Dry Chillies',
                        'Ginger(Dry)', 'Ginger(Green)', 'Green Chilli', 'Groundnut', 'Potato', 'Spinach',
                        'Tamarind Fruit', 'Tamarind Seed', 'Tomato', 'Turmeric', 'Water Melon']
                            
    states_list = ['Andhra Pradesh', 'Telangana', 'Maharashtra', 'Karnataka', 'Chattisgarh', 'Tamil Nadu',
                   'Uttar Pradesh', 'Madhya Pradesh']
    ```
- To extract data for specific commodity or state run script as follows:
  > python agriculture_marketing.py --state "Andhra Pradesh" --state Telangana --commodity Tomato --commodity "Arhar Dal(Tur Dal)"
 
    ###### Here data will be collected for Tomato and Tur Dal for states AP and Telangana. 
    ###### Note: As shown above enclose state or commodity in double quotes when string contains spaces. 

- Output will be stored as csv file and created under webscraper/csv/ path. Filename will be agmarknet_{startdate}_to_{enddate}.


#### Sample console output
```
[vagrant@localhost webscraper]$ python agriculture_marketing.py --days 2 --state "Andhra Pradesh" --state Telangana --commodity Tomato --commodity "Arhar Dal(Tur Dal)"
2021-01-11 10:48:46,678 - argmarknet[setup_logging:56] - DEBUG - starting up logging
2021-01-11 10:48:46,829 - argmarknet[main:138] - INFO - Extracting data for following commodities ['Tomato', 'Arhar Dal(Tur Dal)']
2021-01-11 10:48:46,829 - argmarknet[main:139] - INFO - Extracting data for following states ['Andhra Pradesh', 'Telangana']
2021-01-11 10:49:04,863 - argmarknet[main:147] - DEBUG - Collected required commodities and states
2021-01-11 10:49:04,864 - argmarknet[parse_all_pages:123] - INFO - Collecting data for Arhar Dal(Tur Dal) from Andhra Pradesh through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=260&Tx_State=AP&Tx_District=0&Tx_Market=0&DateFrom=09-Jan-2021&DateTo=11-Jan-2021&Fr_Date=09-Jan-2021&To_Date=11-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Arhar+Dal(Tur+Dal)&Tx_StateHead=Andhra+Pradesh&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-11 10:49:09,670 - argmarknet[parse_page:81] - DEBUG - No tabular data available
2021-01-11 10:49:09,670 - argmarknet[parse_all_pages:123] - INFO - Collecting data for Arhar Dal(Tur Dal) from Telangana through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=260&Tx_State=TL&Tx_District=0&Tx_Market=0&DateFrom=09-Jan-2021&DateTo=11-Jan-2021&Fr_Date=09-Jan-2021&To_Date=11-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Arhar+Dal(Tur+Dal)&Tx_StateHead=Telangana&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-11 10:49:13,172 - argmarknet[parse_page:81] - DEBUG - No tabular data available
2021-01-11 10:49:13,172 - argmarknet[parse_all_pages:123] - INFO - Collecting data for Tomato from Andhra Pradesh through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=78&Tx_State=AP&Tx_District=0&Tx_Market=0&DateFrom=09-Jan-2021&DateTo=11-Jan-2021&Fr_Date=09-Jan-2021&To_Date=11-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Tomato&Tx_StateHead=Andhra+Pradesh&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-11 10:49:16,291 - argmarknet[parse_all_pages:123] - INFO - Collecting data for Tomato from Telangana through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=78&Tx_State=TL&Tx_District=0&Tx_Market=0&DateFrom=09-Jan-2021&DateTo=11-Jan-2021&Fr_Date=09-Jan-2021&To_Date=11-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Tomato&Tx_StateHead=Telangana&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-11 10:49:20,076 - argmarknet[main:159] - INFO - Writing data into file
Data with 21 rows written to /home/vagrant/webscraper/csv/agmarknet_09-Jan-2021_to_11-Jan-2021.csv
Execution took 34.35 seconds
```
#### Sample output file content
```
[vagrant@localhost webscraper]$ cat /home/vagrant/webscraper/csv/agmarknet_09-Jan-2021_to_11-Jan-2021.csv
Sl No.,District Name,Market Name,Commodity,Variety,Grade,Min Price (Rs./Quintal),Max Price (Rs./Quintal),Modal Price (Rs./Quintal),Price Date
0,Chittor,Kalikiri,Tomato,Local,FAQ,600,1060,800,11 Jan 2021
1,Chittor,Kalikiri,Tomato,Local,FAQ,600,1000,860,10 Jan 2021
2,Chittor,Mulakalacheruvu,Tomato,Local,FAQ,550,1200,800,11 Jan 2021
3,Chittor,Mulakalacheruvu,Tomato,Local,FAQ,500,1100,800,10 Jan 2021
4,Chittor,Mulakalacheruvu,Tomato,Local,FAQ,600,1300,900,09 Jan 2021
5,Kurnool,Pattikonda,Tomato,Local,FAQ,120,640,388,11 Jan 2021
6,Kurnool,Pattikonda,Tomato,Local,FAQ,120,600,360,10 Jan 2021
7,Kurnool,Pattikonda,Tomato,Local,FAQ,232,1140,684,09 Jan 2021
8,Chittor,Vayalapadu,Tomato,Local,FAQ,400,1320,880,11 Jan 2021
9,Chittor,Vayalapadu,Tomato,Local,FAQ,800,2800,1800,09 Jan 2021
10,Hyderabad,Bowenpally,Tomato,Deshi,FAQ,400,800,600,11 Jan 2021
11,Hyderabad,Bowenpally,Tomato,Deshi,FAQ,400,800,600,10 Jan 2021
12,Hyderabad,Bowenpally,Tomato,Deshi,FAQ,400,800,700,09 Jan 2021
13,Hyderabad,Gudimalkapur,Tomato,Deshi,FAQ,200,600,400,09 Jan 2021
14,Hyderabad,L B Nagar,Tomato,Deshi,FAQ,300,400,350,11 Jan 2021
15,Hyderabad,L B Nagar,Tomato,Deshi,FAQ,400,800,600,09 Jan 2021
16,Medak,Sangareddy,Tomato,Deshi,FAQ,800,1000,900,11 Jan 2021
17,Medak,Sangareddy,Tomato,Deshi,FAQ,800,1000,900,10 Jan 2021
18,Medak,Sangareddy,Tomato,Deshi,FAQ,800,1000,900,09 Jan 2021
19,Mahbubnagar,Shadnagar,Tomato,Deshi,FAQ,800,1000,900,10 Jan 2021
20,Mahbubnagar,Shadnagar,Tomato,Deshi,FAQ,800,1000,900,09 Jan 2021
```