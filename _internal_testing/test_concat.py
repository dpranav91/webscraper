import pandas as pd
import datetime

datetime_today = datetime.datetime.now()
today = datetime_today.strftime('%d_%m_%Y')
today_time = datetime_today.strftime('%d-%m-%Y %H:%M:%S')

init_df = pd.DataFrame([{'Num':'10', 'b':'20', 'c':'30', 'Rating':'A', 'Inserted Date':'mrg'},
                        {'Num': '11', 'b': '21', 'c': '31', 'Rating':'D', 'Inserted Date':'mrg'},
                        {'Num': '13', 'b': '23', 'c': '33', 'Rating': 'C', 'Inserted Date': 'af'}])
# init_df = init_df.set_index('a')
print(init_df)

result_df =  pd.DataFrame([{'Num': '11', 'b': '2334', 'c': '33', 'new_col':'heha'},
                           {'Num': '10', 'b': 'mod', 'c': '31'},
                           {'Num': '12', 'b': '22', 'c': '32'}])
# new_df = new_df.set_index(['a'])
# new_index = sorted(new_df.index)
# new_df = new_df.reindex(new_index)
# result_df['Inserted Date'] = today_time
result_df['Updated Date'] = today_time
print(result_df)


# a=pd.concat([new_df, init_df])
# print(a)

# b=pd.merge(new_df, init_df, how='inner', on='a')

def update_dfs(initial_df, updated_df, key):

    initial_df = initial_df.set_index(key)
    updated_df = updated_df.set_index(key)
    initial_df.update(updated_df)
    initial_df.reset_index(inplace=True)
    initial_df['Updated Date'] = today_time
    return initial_df

# print()
# res = update_dfs(init_df, result_df, 'a')
#
# print(res)
#
#
# a=pd.concat([result_df, res])
# print(a)

if __name__=='__main__':
    if 'Flag' not in init_df.columns:
        init_df['Flag'] = "No"
    intersection_records = set(result_df['Num']).intersection(set(init_df['Num']))
    new_records = set(result_df['Num']) - set(init_df['Num'])
    set_flag = lambda x: 'Yes' if x['Num'] in intersection_records or \
                                  x['Num'] in new_records else "No"  # x['Flag']
    new_records_df = result_df[result_df['Num'].isin(new_records)]
    new_records_df['Inserted Date'] = today_time

    # UPDATING INITIAL DF with updated data
    init_df = update_dfs(init_df, result_df, 'Num')
    result_df = pd.concat([init_df, new_records_df])
    result_df['Flag'] = result_df.apply(set_flag, axis=1)
    print('\nRESULT\n', result_df)


