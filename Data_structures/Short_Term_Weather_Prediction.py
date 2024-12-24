import psycopg2
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime
from db import db_params

def fetch_weather_data():
    try:
        conn = psycopg2.connect(**db_params)
        # query = """
        # SELECT timestamp, temperature FROM weather_data
        # WHERE station_id = %s
        # ORDER BY timestamp ASC;
        # """
        query="""
        SELECT timestamp, temperature FROM weather_data
        where station_id IN ( SELECT station_id from weather_stations where name=%s)
        ORDER BY timestamp ASC;
        """

        station_id = str(input("Enter the city name : ")) # Example station ID
        df = pd.read_sql_query(query, conn, params=(station_id,))
        return df
    except Exception as error:
        print(f"Error: {error}")
        return None
    finally:
        if conn:
            conn.close()

def predict_temperature():
    df = fetch_weather_data()
    if df is not None and not df.empty:
        # Prepare data
        df['timestamp_ordinal'] = df['timestamp'].apply(lambda x: x.toordinal())
        X = df['timestamp_ordinal'].values.reshape(-1, 1)
        y = df['temperature'].values

        # Train linear regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict temperature for the next day
        next_day = datetime.date.today() + datetime.timedelta(days=1)
        next_day_ordinal = np.array([[next_day.toordinal()]])
        predicted_temp = model.predict(next_day_ordinal)
        in_celsius=predicted_temp[0] - 273.15 
        # print(f"Predicted temperature for {next_day}: {predicted_temp[0]} °C")
        # not using .2f is accurate 
        # print(f"Predicted temperature for {next_day}: {in_celsius} °C")
        print(f"Predicted temperature for {next_day}: {in_celsius:.2f} °C")

predict_temperature()
