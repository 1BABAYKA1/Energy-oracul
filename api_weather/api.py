import requests

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

API_KEY = '4a29ee892ea14dd3869142054231308'
city = "Москва"

weather_obj = WeatherForecast(API_KEY)
weather_forecast = weather_obj.get_forecast(city)

for i in range(0, len(weather_forecast), 10):
    for j in range(10):
        index = i + j
        if index < len(weather_forecast):
            print(weather_forecast[index])
