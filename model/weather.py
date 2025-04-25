import requests
from datetime import datetime

API_KEY = '348a953dd59446df8ba62332252504'  # Replace this with your actual API key from WeatherAPI

class WeatherModel:
    @staticmethod
    def fetch(city):
        # Step 1: Make a request to WeatherAPI for the 7-day forecast
        url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=7"
        response = requests.get(url)
        data = response.json()

        # Check if the request was successful
        if 'error' in data:
            return {'error': data['error']['message']}

        # Step 2: Extract the 7-day forecast data
        forecast_data = data['forecast']['forecastday']
        forecast = []

        for day in forecast_data:
            date = day['date']
            day_data = {
                'date': date,
                'temperature': {
                    'high': day['day']['maxtemp_f'],
                    'low': day['day']['mintemp_f']
                },
                'condition': day['day']['condition']['text'],
                'icon': day['day']['condition']['icon']
            }
            forecast.append(day_data)

        return {'forecast': forecast}