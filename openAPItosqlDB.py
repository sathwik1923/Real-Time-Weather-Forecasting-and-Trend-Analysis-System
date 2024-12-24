import requests
import mysql.connector
from datetime import datetime
import schedule
import time
import json
from db import db_params;
# API details
API_KEY = 'API_KEY'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'

# City list
cities = [
    'Visakhapatnam', 'Vijayawada', 'Guntur', 'Nellore', 'Kurnool', 'Kakinada',
    'Rajamahendravaram', 'Kadapa', 'Mangalagiri', 'Tirupati', 'Anantapuram',
    'Ongole', 'Vizianagaram', 'Eluru', 'Proddatur', 'Nandyal', 'Adoni', 'Madanapalle',
    'Machilipatnam', 'Tenali', 'Chittoor', 'Hindupur', 'Srikakulam', 'Bhimavaram',
    'Tadepalligudem', 'Guntakal', 'Dharmavaram', 'Gudivada', 'Narasaraopet', 'Kadiri',
    'Tadipatri', 'Chilakaluripet'
]

# Database connection parameters

def get_weather_data(city):
    request_url = f"{BASE_URL}q={city}&appid={API_KEY}"
    response = requests.get(request_url)
    if response.status_code == 200:
        data = response.json()
        return {
            'city': city,
            'json_data': data,
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'pressure': data['main']['pressure'],
            'humidity': data['main']['humidity'],
            'sea_level': data['main'].get('sea_level'),
            'grnd_level': data['main'].get('grnd_level'),
            'visibility': data.get('visibility'),
            'wind_speed': data['wind']['speed'],
            'wind_deg': data['wind']['deg'],
            'cloudiness': data['clouds']['all'],
            'weather_main': data['weather'][0]['main'],
            'weather_description': data['weather'][0]['description'],
            'timestamp': data['dt']
        }
    else:
        return None

def collect_weather_data(cities):
    weather_data = []
    for city in cities:
        data = get_weather_data(city)
        if data:
            weather_data.append(data)
    return weather_data

def insert_weather_data(weather_json):
    try:
        # Connect to MySQL
        conn = mysql.connector.connect(**db_params)
        cursor = conn.cursor()

        # Insert raw JSON data
        insert_raw_query = "INSERT INTO raw_weather_data (json_data) VALUES (%s);"
        cursor.execute(insert_raw_query, (json.dumps(weather_json['json_data']),))
        raw_data_id = cursor.lastrowid

        # Insert or update weather station information
        insert_station_query = """
        INSERT INTO weather_stations (name, country, latitude, longitude, location)
        VALUES (%s, %s, %s, %s, ST_GeomFromText(%s, 4326))
        ON DUPLICATE KEY UPDATE country = VALUES(country);
        """
        cursor.execute(insert_station_query, (weather_json['city'], weather_json['json_data']['sys']['country'],
                                              weather_json['json_data']['coord']['lat'], weather_json['json_data']['coord']['lon'],
                                              f'POINT({weather_json["json_data"]["coord"]["lon"]} {weather_json["json_data"]["coord"]["lat"]})'))
        cursor.execute("SELECT station_id FROM weather_stations WHERE name = %s", (weather_json['city'],))
        station_id = cursor.fetchone()[0]

        # Insert weather data
        insert_weather_data_query = """
        INSERT INTO weather_data (station_id, timestamp, temperature, feels_like, temp_min, temp_max, pressure, humidity,
                                  sea_level, grnd_level, visibility, wind_speed, wind_deg, cloudiness, weather_main, weather_description)
        VALUES (%s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(insert_weather_data_query, (station_id, weather_json['timestamp'], weather_json['temperature'],
                                                   weather_json['feels_like'], weather_json['temp_min'], weather_json['temp_max'],
                                                   weather_json['pressure'], weather_json['humidity'], weather_json['sea_level'],
                                                   weather_json['grnd_level'], weather_json['visibility'], weather_json['wind_speed'],
                                                   weather_json['wind_deg'], weather_json['cloudiness'], weather_json['weather_main'],
                                                   weather_json['weather_description']))

        # Commit transaction
        conn.commit()

    except Exception as error:
        print(f"Error: {error}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def job():
    data = collect_weather_data(cities)
    for entry in data:
        insert_weather_data(entry)
    print(f"Data collected and stored at {datetime.now()}")

if __name__ == "__main__":
    job()
    # Schedule the job to run every hour
    schedule.every().hour.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
