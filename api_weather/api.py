import requests
import os
from dotenv import load_dotenv
import csv

load_dotenv()

class WeatherForecast:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.weatherapi.com/v1/forecast.json"
    
    def get_forecast(self, city):
        params = {
            "key": self.api_key,
            "q": city,
            "days": "10",
            "lang": 'ru'
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()
        forecast = data['forecast']['forecastday']

        return [
            [day['date'], hour['time'].split()[1], hour['temp_c'], hour['condition']['text'], hour['condition']['code']]
            for day in forecast
            for hour in day['hour']
        ]

    def write_to_csv(self, forecast):
        csv_filename = "files/weather_forecast.csv"
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Date', 'Time', 'Temperature (°C)', 'Condition', 'Condition Code']
            writer = csv.writer(csv_file)
            writer.writerow(fieldnames)
            for data in forecast:
                writer.writerow(data)

        print(f"Прогноз погоды записан в файл: {csv_filename}")

if __name__ == "__main__":
    api_key = os.getenv("API_KEY")
    city = "Москва"
    weather_obj = WeatherForecast(api_key)
    weather_forecast = weather_obj.get_forecast(city)
    weather_obj.write_to_csv(weather_forecast)