import requests
import sqlite3
import pandas as pd
import time
import matplotlib.pyplot as plt
from collections import Counter
import time

# OpenWeatherMap API Key
API_KEY = 'your-api-key'

# Cities for which we will monitor the weather
cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

def create_database():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    
    # Create a table to store daily weather summaries
    c.execute('''CREATE TABLE IF NOT EXISTS daily_summary
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT NOT NULL,
                  city TEXT NOT NULL,
                  avg_temp REAL NOT NULL,
                  max_temp REAL NOT NULL,
                  min_temp REAL NOT NULL,
                  dominant_condition TEXT NOT NULL,
                  UNIQUE(date, city))''')
    
    conn.commit()
    conn.close()

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}'
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching weather data for {city}: {response.status_code}")
        print(response.json())  # Print the full response to understand the issue
        return None  # Return None if there is an issue with the API response
    
    data = response.json()
    
    # Debug: Print the raw response to check the structure
    print(f"Weather data for {city}: {data}")
    
    return data


def kelvin_to_celsius(kelvin_temp):
    return kelvin_temp - 273.15

def process_weather_data(weather_data, city):
    if weather_data is None:
        print(f"Failed to retrieve weather data for {city}")
        return None

    # Extract required data from the weather response
    try:
        temp = kelvin_to_celsius(weather_data['main']['temp'])
        feels_like = kelvin_to_celsius(weather_data['main']['feels_like'])
        condition = weather_data['weather'][0]['main']
        timestamp = weather_data['dt']
        
        # Extract date from timestamp (in Unix format)
        date = pd.to_datetime(timestamp, unit='s').date()
        
        return {
            "date": date,
            "city": city,
            "temp": temp,
            "feels_like": feels_like,
            "condition": condition
        }
    except KeyError as e:
        print(f"Error processing data for {city}: {e}")
        return None

def store_daily_summary(daily_summary):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    
    # Insert or update weather data in the database
    c.execute('''INSERT OR REPLACE INTO daily_summary (date, city, avg_temp, max_temp, min_temp, dominant_condition)
                 VALUES (?, ?, ?, ?, ?, ?)''', 
              (daily_summary['date'], daily_summary['city'], daily_summary['avg_temp'], 
               daily_summary['max_temp'], daily_summary['min_temp'], daily_summary['dominant_condition']))
    
    conn.commit()
    conn.close()

def calculate_daily_summary(weather_data_list):
    avg_temp = sum([data['temp'] for data in weather_data_list]) / len(weather_data_list)
    max_temp = max([data['temp'] for data in weather_data_list])
    min_temp = min([data['temp'] for data in weather_data_list])
    
    conditions = [data['condition'] for data in weather_data_list]
    dominant_condition = Counter(conditions).most_common(1)[0][0]
    
    return {
        'date': weather_data_list[0]['date'],
        'city': weather_data_list[0]['city'],
        'avg_temp': avg_temp,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'dominant_condition': dominant_condition
    }

def check_alerts(current_temp, threshold=35):
    if current_temp > threshold:
        print(f"Alert! Temperature exceeded {threshold}°C.")

def plot_daily_summary():
    conn = sqlite3.connect('weather_data.db')
    df = pd.read_sql_query("SELECT * FROM daily_summary", conn)
    conn.close()
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['date'], df['avg_temp'], label='Average Temperature')
    plt.plot(df['date'], df['max_temp'], label='Max Temperature')
    plt.plot(df['date'], df['min_temp'], label='Min Temperature')
    
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Daily Weather Summary')
    plt.legend()
    plt.show()

def main():
    create_database()  # Ensure the database and table are created at the start
    
    while True:
        daily_weather_data = []
        
        for city in cities:
            weather_data = get_weather_data(city)
            processed_data = process_weather_data(weather_data, city)
            
            # Only append to daily_weather_data if processed_data is not None
            if processed_data:
                daily_weather_data.append(processed_data)
        
        # If we have valid weather data, calculate and store the daily summary
        if daily_weather_data:
            daily_summary = calculate_daily_summary(daily_weather_data)
            store_daily_summary(daily_summary)
            
            for data in daily_weather_data:
                check_alerts(data['temp'])
        
        time.sleep(100)  # Fetch weather data every 5 minutes
        plot_daily_summary()


if __name__ == '__main__':
    main()
