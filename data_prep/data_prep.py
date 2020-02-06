def preview_raw_data():
  import pandas as pd
  
  station_data = pd.read_csv('station_data.csv')
  trip_data = pd.read_csv('trip_data.csv')
  weather_data = pd.read_csv('weather_data.csv')

  print('Station data')
  display(station_data.head())
  display(station_data.describe())
  print('Trip data')
  display(trip_data.head())
  display(trip_data.describe())
  print('Weather data')
  display(weather_data.head())
  display(weather_data.describe())

def get_net_rate_matrix(trip_data):
  # Number of trips ended per station per each timestamp hour
  end_indexed = trip_data.set_index('End Date')
  grouper = end_indexed.groupby([pd.Grouper(freq='1H'), 'End Station'])
  end_result = grouper['Trip ID'].count().unstack('End Station').fillna(0)
  
  # Number of trips started per station per timestamp hour
  start_indexed = trip_data.set_index('Start Date')
  rouper = start_indexed.groupby([pd.Grouper(freq='1H'), 'Start Station'])
  start_result = grouper['Trip ID'].count().unstack('Start Station').fillna(0)

  # Trips ended - Strips started = Net Rate
  net_rates_by_station = end_result - start_result
  net_rates_by_station.fillna(0, inplace=True)
  net_rates_by_station.plot(figsize=(20,10))
  net_rates_by_station.index.name = 'Datetime'
  net_rates_by_station.columns.name = 'Station ID'

  return net_rates_by_station

def generate_dataset():
  station_data = pd.read_csv('station_data.csv')
  trip_data = pd.read_csv('trip_data.csv')
  weather_data = pd.read_csv('weather_data.csv')

  station_data['Id'] = station_data['Id'].astype(str)

  trip_data['Start Date'] = pd.to_datetime(trip_data['Start Date'])
  trip_data['End Date'] = pd.to_datetime(trip_data['End Date'])
  trip_data['Start Station'] = trip_data['Start Station'].astype(str)
  trip_data['End Station'] = trip_data['End Station'].astype(str)

  weather_data['Date'] = pd.to_datetime(weather_data['Date'])
  weather_data['Date'] = weather_data['Date'].apply(lambda x : x.date())
  weather_data['Events'] = weather_data['Events'].fillna('None')

  def zip_to_city(zip_code):
      switcher = {
          94107: 'San Francisco',
          94063: 'Redwood City',
          94301: 'Palo Alto',
          94041: 'Mountain View',
          95113: 'San Jose'
      }
      return switcher.get(zip_code)
  weather_data['City'] = list((map(zip_to_city, weather_data['Zip'])))
  weather_data = weather_data.drop(['Zip'], axis=1)