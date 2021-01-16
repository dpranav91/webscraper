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
##### Reference: https://www.geeksforgeeks.org/using-mkvirtualenv-to-create-new-virtual-environment-python
> mkvirtualenv webscraper; setvirtualenvproject

#### install required packages
> ./update_requirements

## When Setup Is Already Created
#### activate virtual env that was created earlier using below command
> workon webscraper


## RUNNER
#### run agriculture_marketing to collect tabular data from agmarknet.gov.in
- For testing the script for the very first time and to make sure whether python setup is fine; 
run with --test arg. Script will be run with minimal combinations.
```
[vagrant@localhost webscraper]$ python agriculture_marketing.py --test
2021-01-16 14:05:33,268 - argmarknet[setup_logging:56] - DEBUG - starting up logging
2021-01-16 14:05:34,533 - argmarknet[main:277] - INFO - Extracting data for following commodities ['Tomato']
2021-01-16 14:05:34,534 - argmarknet[main:278] - INFO - Extracting data for following states ['Telangana']
...
```

- Default without any args:
    - By default script will collect data for states and commodities listed below:
        ```
        List of commodities_list shall be collected from `data/FilteredCommodities.json` ->
        commodities_list = ['Apple', 'Arhar Dal(Tur Dal)', 'Beans', 'Bengal Gram Dal', 'Bhindi(Ladies Finger)',
                            'Bitter gourd', 'Carrot', 'Chili Red', 'Coriander(Leaves)', 'Cotton', 'Dry Chillies',
                            'Ginger(Dry)', 'Ginger(Green)', 'Green Chilli', 'Groundnut', 'Potato', 'Spinach',
                            'Tamarind Fruit', 'Tamarind Seed', 'Tomato', 'Turmeric', 'Water Melon']
        
        List of states_list shall be collected from `data/FilteredStates.json` ->                        
        states_list = ['Andhra Pradesh', 'Telangana', 'Maharashtra', 'Karnataka', 'Chattisgarh', 'Tamil Nadu',
                       'Uttar Pradesh', 'Madhya Pradesh']
        ```
    - By default script with consider start date as 7 days prior to today's date.
```buildoutcfg
[vagrant@localhost webscraper]$ python agriculture_marketing.py
2021-01-16 14:11:54,184 - argmarknet[setup_logging:56] - DEBUG - starting up logging
2021-01-16 14:11:55,426 - argmarknet[main:277] - INFO - Extracting data for following commodities ['Apple', 'Arhar Dal(Tur Dal)', 'Beans', 'Bengal Gram Dal (Chana Dal)', 'Bhindi(Ladies Finger)', 'Bitter gourd', 'Carrot', 'Chili Red', 'Coriander(Leaves)', 'Cotton', 'Dry Chillies', 'Ginger(Dry)', 'Ginger(Green)', 'Green Chilli', 'Groundnut', 'Potato', 'Spinach', 'Tamarind Fruit', 'Tamarind Seed', 'Tomato', 'Turmeric', 'Water Melon']
2021-01-16 14:11:55,426 - argmarknet[main:278] - INFO - Extracting data for following states ['Andhra Pradesh', 'Telangana', 'Maharashtra', 'Karnataka', 'Chattisgarh', 'Tamil Nadu', 'Uttar Pradesh', 'Madhya Pradesh']
...
```

- To extract data for different number of days, run script as follows:
    > python agriculture_marketing.py -d 3 (This will collect data for past 3 days)

- To extract data for specific commodity or state run script as follows:
  > python agriculture_marketing.py --state "Andhra Pradesh" --state Telangana --commodity Tomato --commodity "Arhar Dal(Tur Dal)"
 
    ###### Here data will be collected for Tomato and Tur Dal for states AP and Telangana. 
    ###### Note: As shown above enclose state or commodity in double quotes when string contains spaces. 

- Output will be stored as csv file and created under webscraper/csv/ path. Filename will be agmarknet_{startdate}_to_{enddate}.


#### Sample console output
```
[vagrant@localhost webscraper]$ python agriculture_marketing.py --days 2 --state "Andhra Pradesh" --state Telangana --commodity Tomato --commodity "Arhar Dal(Tur Dal)"
2021-01-16 14:00:36,479 - argmarknet[setup_logging:56] - DEBUG - starting up logging
2021-01-16 14:00:38,747 - argmarknet[main:277] - INFO - Extracting data for following commodities ['Tomato', 'Arhar Dal(Tur Dal)']
2021-01-16 14:00:38,747 - argmarknet[main:278] - INFO - Extracting data for following states ['Andhra Pradesh', 'Telangana']
2021-01-16 14:00:56,421 - argmarknet[parse:241] - DEBUG - Collected required commodities and states
2021-01-16 14:00:56,422 - argmarknet[parse_all_pages:215] - INFO - Collecting data for Arhar Dal(Tur Dal) from Andhra Pradesh through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=260&Tx_State=AP&Tx_District=0&Tx_Market=0&DateFrom=14-Jan-2021&DateTo=16-Jan-2021&Fr_Date=14-Jan-2021&To_Date=16-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Arhar+Dal(Tur+Dal)&Tx_StateHead=Andhra+Pradesh&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-16 14:01:00,230 - argmarknet[parse_each_page:140] - DEBUG - No tabular data available
2021-01-16 14:01:00,230 - argmarknet[parse_all_pages:215] - INFO - Collecting data for Arhar Dal(Tur Dal) from Telangana through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=260&Tx_State=TL&Tx_District=0&Tx_Market=0&DateFrom=14-Jan-2021&DateTo=16-Jan-2021&Fr_Date=14-Jan-2021&To_Date=16-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Arhar+Dal(Tur+Dal)&Tx_StateHead=Telangana&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-16 14:01:04,576 - argmarknet[parse_each_page:140] - DEBUG - No tabular data available
2021-01-16 14:01:04,576 - argmarknet[parse_all_pages:215] - INFO - Collecting data for Tomato from Andhra Pradesh through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=78&Tx_State=AP&Tx_District=0&Tx_Market=0&DateFrom=14-Jan-2021&DateTo=16-Jan-2021&Fr_Date=14-Jan-2021&To_Date=16-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Tomato&Tx_StateHead=Andhra+Pradesh&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-16 14:01:08,339 - argmarknet[parse_all_pages:215] - INFO - Collecting data for Tomato from Telangana through https://agmarknet.gov.in/SearchCmmMkt.aspx?Tx_Commodity=78&Tx_State=TL&Tx_District=0&Tx_Market=0&DateFrom=14-Jan-2021&DateTo=16-Jan-2021&Fr_Date=14-Jan-2021&To_Date=16-Jan-2021&Tx_Trend=0&Tx_CommodityHead=Tomato&Tx_StateHead=Telangana&Tx_DistrictHead=--Select--&Tx_MarketHead=--Select--
2021-01-16 14:01:11,385 - argmarknet[write_data:269] - INFO - Writing data into file
Data with 15 rows written to /home/vagrant/webscraper/csv/agmarknet_14-Jan-2021_to_16-Jan-2021.csv
Execution took 32.79 seconds
```
#### Sample output file content
```
[vagrant@localhost webscraper]$ cat /home/vagrant/webscraper/csv/agmarknet_14-Jan-2021_to_16-Jan-2021.csv
Sl No.,State,State Code,District Name,District Code,Market Name,Market Code,Commodity,Variety,Grade,Min Price (Rs./Quintal),Max Price (Rs./Quintal),Modal Price (Rs./Quintal),Price Date
0,Andhra Pradesh,AP,Chittor,NA,Mulakalacheruvu,NA,Tomato,Local,FAQ,550,1200,800,2021-16-01
1,Andhra Pradesh,AP,Chittor,NA,Mulakalacheruvu,NA,Tomato,Local,FAQ,650,1300,950,2021-15-01
2,Andhra Pradesh,AP,Chittor,NA,Mulakalacheruvu,NA,Tomato,Local,FAQ,550,1200,850,2021-14-01
3,Andhra Pradesh,AP,Kurnool,APKOL,Pattikonda,NA,Tomato,Local,FAQ,500,1000,700,2021-16-01
4,Andhra Pradesh,AP,Kurnool,APKOL,Pattikonda,NA,Tomato,Local,FAQ,500,1000,700,2021-15-01
5,Andhra Pradesh,AP,Kurnool,APKOL,Pattikonda,NA,Tomato,Local,FAQ,500,1000,700,2021-14-01
6,Telangana,TS,Hyderabad,TSHYD,Bowenpally,TSBOW,Tomato,Deshi,FAQ,200,400,300,2021-16-01
7,Telangana,TS,Hyderabad,TSHYD,Bowenpally,TSBOW,Tomato,Deshi,FAQ,300,600,500,2021-15-01
8,Telangana,TS,Hyderabad,TSHYD,Bowenpally,TSBOW,Tomato,Deshi,FAQ,300,600,500,2021-14-01
9,Telangana,TS,Hyderabad,TSHYD,Gudimalkapur,NA,Tomato,Deshi,FAQ,200,600,400,2021-15-01
10,Telangana,TS,Hyderabad,TSHYD,Gudimalkapur,NA,Tomato,Deshi,FAQ,200,600,400,2021-14-01
11,Telangana,TS,Medak,TSMDK,Sangareddy,TSSAN,Tomato,Deshi,FAQ,600,800,700,2021-15-01
12,Telangana,TS,Medak,TSMDK,Sangareddy,TSSAN,Tomato,Deshi,FAQ,800,1000,900,2021-14-01
13,Telangana,TS,Mahbubnagar,NA,Shadnagar,NA,Tomato,Deshi,FAQ,500,800,600,2021-15-01
14,Telangana,TS,Mahbubnagar,NA,Shadnagar,NA,Tomato,Deshi,FAQ,600,1000,800,2021-14-01
```
