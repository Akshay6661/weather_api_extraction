import requests
import csv
import time
import schedule
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)


# Your OpenWeatherMap API key
API_KEY = "KEY"

# Base URL for the OpenWeatherMap API
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Function to get weather data
def get_weather_data():
    city_name = "London"  # Change city name as needed
    url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    logging.debug("Making API request...")

    if response.status_code == 200:
        logging.debug(f"Response Status: {response.status_code}")

        data = response.json()

        # Extract relevant data
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        temperature = main['temp']
        pressure = main['pressure']
        humidity = main['humidity']
        weather_description = weather['description']
        wind_speed = wind['speed']
        sys = data['name']
        
        # Prepare the data to be saved
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row = [timestamp, temperature, pressure, humidity, weather_description, wind_speed, sys]


        # Append the data to a CSV file
        with open("weather_data.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            # Write header if the file is empty
            if file.tell() == 0:
                writer.writerow(["Timestamp", "Temperature", "Pressure", "Humidity", "Weather", "Wind Speed", "City"])
            writer.writerow(row)

        print(f"Weather data for {city_name} has been saved to 'weather_data.csv'.")
    else:
        print("Error: Unable to fetch weather data")

# Schedule the task to run every 1 hour
schedule.every(1).minute.do(get_weather_data)

get_weather_data()


# Keep the script running
while True:
    schedule.run_pending()  # Run the scheduled tasks
    time.sleep(1)  # Sleep for a short time before checking again
