import numpy as np

# making dataframe ready for medal_tally option
def medal_tally(df) :
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    medal_tally = medal_tally.groupby('region').sum()[["Gold","Silver","Bronze"]].reset_index()
    medal_tally['total'] = medal_tally["Gold"] + medal_tally["Bronze"] + medal_tally["Silver"]

    return medal_tally

# function to make dropdowns work
def fetch_medal_tally(df,year, country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0  # by-default flag
    if year == 'overall' and country == 'overall':
        temp_df = medal_df

    if year == 'overall' and country != 'overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    if year != 'overall' and country == 'overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != 'overall' and country != 'overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x

# option in the dropdown bar in the sidebar for filtering particular year or country
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'overall')

    return years, country

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col ])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time.rename(columns={'Year': 'Edition', 'count': col }, inplace=True)
    return nations_over_time


def most_successful(df,Sport):
    temp_df = df.dropna(subset=['Medal'])

    if Sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == Sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name', how='left')[['Name','Sport','region','count']].drop_duplicates('Name')
    x = x.rename(columns={'count':'Medals'})
    return x

def yearwise_country_medaltally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df










