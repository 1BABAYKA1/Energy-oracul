import requests
import csv

class WeatherDataFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        response = requests.get(self.url)
        response.encoding = 'utf-8-sig'
        return response.json()

class WeatherConditionsCSV:
    def __init__(self, data):
        self.data = data
        self.csv_filename = "files/weather_conditions.csv"

    def process_and_save(self):
        with open(self.csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['Code', 'Day_Text']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for item in self.data:
                code = item['code']
                for lang_data in item['languages']:
                    if lang_data['lang_name'] == 'Russian':
                        day_text = lang_data['day_text']

                        writer.writerow({'Code': code, 'Day_Text': day_text})

        print(f"Данные записаны в файл: {self.csv_filename}")

url = "https://www.weatherapi.com/docs/conditions.json"

data_fetcher = WeatherDataFetcher(url)
json_data = data_fetcher.fetch_data()

csv_writer = WeatherConditionsCSV(json_data)
csv_writer.process_and_save()
