import pandas as pd

def sort_pd(key=None,reverse=False,cmp=None):
    def sorter(series):
        series_list = list(series)
        return [series_list.index(i)
           for i in sorted(series_list,key=key,reverse=reverse)]
    return sorter

df = pd.DataFrame([
    [1, 2, '06/06/17 14:00:00'],
    [5, 6, '06/14/17  12:00PM'],
    [3, 4, '07/13/17  11:00AM'],
    [2, 45, '6/12/17 - 10:00 AMCancelled Until 8/14/17']],
  columns=['a','b','m'])
print(df)
import re
def parse_bid_date(date):
    return ' '.join(re.compile('(\d+?/\d+?/\d+?)[\s-]*(\d+?:\d{2}).*').search(date).groups())

try:
    df['Date']=df['m'].apply(parse_bid_date)
    df['Date']=(pd.to_datetime(df['Date']))
    df = df.sort_values('Date')
except:
    print("Unable to sort by Bid Date")
    pass
print(df)