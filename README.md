# Real-Time Weather Monitoring System
This project is a real-time data processing system for monitoring weather conditions in several Indian metropolitan cities. The system fetches data from the OpenWeatherMap API at regular intervals, processes it to provide daily rollups and aggregates, and stores it in a SQLite database. Alerts can be triggered when certain user-configurable thresholds are breached.

## Features
- **Weather Data Collection**: Retrieves real-time weather data for cities (Delhi, Mumbai, Chennai, Bangalore, Kolkata, Hyderabad) using the OpenWeatherMap API.
- **Daily Summaries**: Stores daily weather summaries including:
- - Average temperature
- - Maximum temperature
- - Minimum temperature
- - Dominant weather condition
- **Threshold Alerts**: Supports user-configurable alerts for conditions such as:
- - Temperature exceeding a certain threshold
- - Specific weather conditions like heavy rain or high heat
- **Data Storage**: All collected weather data and summaries are stored in a SQLite database.
- **Visualization**: Displays historical trends, daily summaries, and alerts (can be extended).
## Technologies Used
- **Python**: Main programming language
- **SQLite**: Database to store weather summaries
- **SQLAlchemy**: ORM to simplify database operations
- **Requests**: For fetching data from OpenWeatherMap API
- **OpenWeatherMap API**: To fetch real-time weather data
## Setup Instructions
### Prerequisites
- Python 3.8+
-pip package manager
- OpenWeatherMap API key: You will need to sign up for a free API key at OpenWeatherMap.
## Install Required Libraries
Clone the repository:
```bash
git clone https://github.com/Aryan-Verma-999/Weather-Monitoring.git
cd Weather-Monitoring
```
Install dependencies:

```bash
pip install -r requirements.txt
```
Set up the SQLite database:

```bash
python create_db.py
```
This will create a file weather_data.db and set up the necessary tables.

Configuration
API Key: Update the API key in the code with your OpenWeatherMap key.

```python
API_KEY = 'your_api_key_here'
```
City List: You can modify the cities you want to monitor in the cities list in the code:

```python
Copy code
cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
```
Alert Thresholds: Define your custom thresholds for temperature or specific weather conditions in the check_alerts() function.

Running the Application
Once you have set up everything, you can start the system using the following command:

```bash
Copy code
python main.py
```
The script will:

- Fetch real-time weather data every 5 minutes (you can adjust this interval in the code).
- Process and store the daily weather summaries.
- Trigger alerts if thresholds are breached.
- Accessing the Data
To check the stored data, you can query the SQLite database weather_data.db. Use tools like DB Browser for SQLite or directly query the database using Python:

```python
Copy code
import sqlite3

conn = sqlite3.connect('weather_data.db')
c = conn.cursor()
c.execute('SELECT * FROM daily_summary')
print(c.fetchall())
conn.close()
```
## Testing
Test cases can be added to verify:

1. API connectivity and data retrieval
2. Data parsing and temperature conversion
3. Daily summary calculations
4. Alert triggering on threshold breaches
You can modify the test data or simulate different conditions using mock API responses.

## Future Enhancements
- **Weather Forecasting**: Extend the system to handle weather forecasts and generate predicted summaries.
- **Visualization Dashboard**: Integrate with tools like Plotly or Matplotlib to create a visualization dashboard for the weather data.
- **Advanced Alerts**: Add email or SMS alerting systems for users.
