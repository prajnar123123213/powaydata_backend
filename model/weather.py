# model/weather.py

import requests

API_KEY = '45efd2124b8b4350a9f165744250704'

class WeatherModel:
    @staticmethod
    def fetch(city):
        url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
        try:
            response = requests.get(url)
            data = response.json()
            return {
                'location': f"{data['location']['name']}, {data['location']['region']}",
                'temperature': f"{data['current']['temp_f']} °F",
                'condition': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon']
            }
        except Exception as e:
            return {'error': str(e)}

def initWeather():
    print("Weather model initialized (no database setup needed).")
