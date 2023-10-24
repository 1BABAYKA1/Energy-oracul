import pandas as pd
import csv
import requests
from datetime import datetime
from api import WeekendAnalyzer as WF

class DataProcessor:
    def __init__(self, latitude, longitude, start_date):
        self.user_data = self.load_data()
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        
        self.end_date = end_date
        self.base_url = f"https://archive-api.open-meteo.com/v1/archive?latitude={self.latitude}&longitude={self.longitude}&start_date={self.start_date}&end_date={self.end_date}&hourly=temperature_2m,precipitation,cloudcover,weathercode&timezone=Europe%2FMoscow&format=csv"
        
    def load_data(self):
        if self.input_file.endswith('.csv'):
            return pd.read_csv(self.input_file, delimiter=';')
        else:
            raise ValueError("ERROR 1.")
    
    def get_weather_data(self):
        response = requests.get(self.base_url)
        csv_text = response.text
        csv_lines = csv_text.splitlines()

        csv_lines_iter = iter(csv_lines)
        for _ in range(4):
            next(csv_lines_iter)

        weather_data = []
        
        for line in csv_lines_iter:
            parts = line.split(',')

            if len(parts) >= 5 and not all(part == 'NaN' for part in parts[1:]):
                temperature = parts[1]
                precipitation = parts[2]
                if float(precipitation) > 0:
                    precipitation = 1
                else:
                    precipitation = 0
                cloudcover = parts[3]
                if float(cloudcover) > 30:
                    cloudcover = 0
                else:
                    cloudcover = 1

                weather_data.append({
                    'temp': temperature,
                    'осадки': precipitation,
                    'ясно': cloudcover
                })
        
        return weather_data
    
    def write_to_csv(self, forecast, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['temp', 'осадки', 'ясно']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()

            for data in forecast:
                writer.writerow(data)
        data1 = pd.read_csv('files/input.csv', delimiter=';')
        data2 = pd.read_csv(filename, delimiter=';')
        print(data2)
        merged_data = pd.concat([data1, data2], axis=1)
        merged_data[['day', 'month', 'year']] = merged_data['date'].str.split('.', expand=True)
        merged_data = merged_data.drop(['date'], axis=1)
        merged_data = merged_data.dropna()
        merged_data.to_csv(f'{filename}', index=False, sep=';')

try:
    with open('files/input.csv', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        weather_data = list(reader)
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = datetime.now()
        
    processor = DataProcessor('files/input.csv', "52.52", "13.41", start_date, end_date)
    processor.load_data()
    weather_forecast = processor.get_weather_data()
    processor.write_to_csv(weather_forecast, 'files/weather_forecast.csv')
    
    pr = WF('files/weather_forecast.csv', 'files/weather_forecast.csv')
    pr.analyze_test()
except Exception as e:
    print(e)
    print(f"Ошибка: {e}")
