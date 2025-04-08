# api/weather.py

from flask import Blueprint, request, jsonify
from model.weather import WeatherModel

weather_api = Blueprint('weather_api', __name__)

@weather_api.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', default='San Diego')
    result = WeatherModel.fetch(city)

    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result)