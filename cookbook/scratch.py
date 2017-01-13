import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('ggplot') # plt.style.available to list styles

# get csv data
bikes = pd.read_csv('../data/bikes.csv', sep=";", encoding='latin1', parse_dates=['Date'], dayfirst=True, index_col='Date')
# plot one column
bikes['Berri 1'].plot()

# create one variable df
berri_bikes = bikes[['Berri 1']]
berri_bikes.index # the datetime index
berri_bikes.index.day # for the day
berri_bikes.index.weekday # for the weekday, 0 = Monday

# add new column to df
berri_bikes['weekday'] = berri_bikes.index.weekday_name

# add cyclists by weekday
weekday_counts = berri_bikes.groupby('weekday').aggregate(sum)
weekday_counts.sort('Berri 1', ascending=False)
weekday_counts.plot(kind='bar')

#======================================================================
# weather exercise -- web scraping
weather_2012_final = pd.read_csv('../data/weather_2012.csv', index_col='Date/Time')
weather_2012_final['Temp (C)'].plot(figsize=(20, 10))


# get data from the web
url_template = "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=5415&Year={year}&Month={month}&timeframe=1&submit=Download+Data"
url = url_template.format(month=3, year=2012)
weather_mar2012 = pd.read_csv(url, skiprows=16, index_col='Date/Time', parse_dates=True, encoding='latin1')
# remove degree symbols from column names
weather_mar2012.columns = [s.replace(u"ÃÂ°", '') for s in weather_mar2012.columns]
# plot a variable
weather_mar2012["Temp (C)"].plot(figsize=(15, 5))
# remove all columns that contain no data, just NaN
weather_mar2012 = weather_mar2012.dropna(axis=1, how='all')
# remove columns Year, Month, Day, Data Quality as are redundant or not helpful
weather_mar2012 = weather_mar2012.drop(['Year', 'Month', 'Day', 'Time', 'Data Quality'], axis=1)

# create new df with temp only
temperatures = weather_mar2012[['Temp (C)']]
# and add an hour column
temperatures['Hour'] = weather_mar2012.index.hour
# which is used to group, average, and plot temperatures
temperatures.groupby('Hour').aggregate(np.median).plot()

# function to get data for a particular month
def download_weather_month(year, month):
    if month == 1:
        year += 1
    url = url_template.format(year=year, month=month)
    weather_data = pd.read_csv(url, skiprows=16, index_col='Date/Time', parse_dates=True)
    weather_data = weather_data.dropna(axis=1)
    # only keep first three letters of column names
    weather_data.columns = [col[0:3] for col in weather_data.columns]
    weather_data = weather_data.drop(['Yea', 'Day', 'Mon', 'Tim', 'Dat'], axis=1)
    return weather_data

# get data for entire year
data_by_month = [download_weather_month(2012, i) for i in range(1, 13)]
# and concatenate them into one df
weather_2012 = pd.concat(data_by_month)
# save data to a file
weather_2012.to_csv('../data/weather_2012.csv')

#======================================================================

plt.rcParams['figure.figsize'] = (15, 3)
plt.rcParams['font.family'] = 'sans-serif'

# read data (not necessary though)
weather_2012 = pd.read_csv('../data/weather_2012.csv', parse_dates=True, index_col='Date/Time')
weather_description = weather_2012['Wea']

# resample data to monthly intervals, with how=method
temperature = weather_2012[['Tem']].resample('M', how=np.median)
is_snowing = weather_description.str.contains('Snow')
snowiness = is_snowing.astype(float).resample('M', how=np.mean)

# create new df with the two variables above
stats = pd.concat([temperature, snowiness], axis=1)
stats.plot(kind='bar', subplots=True, figsize=(15, 10))