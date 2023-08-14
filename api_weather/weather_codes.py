import requests
import csv

url = "https://www.weatherapi.com/docs/conditions.json"
response = requests.get(url)
response.encoding = 'utf-8-sig'
data = response.json()


csv_filename = "api_weather/weather_conditions.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['Code', 'Day_Text']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for item in data:
        code = item['code']
        for lang_data in item['languages']:
            if lang_data['lang_name'] == 'Russian':
                day_text = lang_data['day_text']
                writer.writerow({'Code': code, 'Day_Text': day_text})

print(f"Данные на русском языке записаны в файл: {csv_filename}")