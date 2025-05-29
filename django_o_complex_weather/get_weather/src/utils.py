import requests
from fake_useragent import UserAgent


class Weather:

    def __init__(self, city_name):
        self.city_name = city_name
        self.get_weather_in_city()

    def get_coordinates(self):
        url = 'https://nominatim.openstreetmap.org/search'
        headers = {
            "User-Agent": UserAgent().random
        }
        params = {
            'q': self.city_name,
            'format': 'json',
            'limit': 1,
        }
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()

            if data := response.json():
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return lat, lon

        except Exception:
            return False


    def request_weather(self, lat, lon):
        result = {'city': self.city_name}

        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Europe/Moscow"
        )
        try:
            response = requests.get(url)
            response.raise_for_status()

            if data := response.json():
                daily = data.get('daily', {})
                result['time'] = daily.get('time', [])[0]
                result['min_temp'] = daily.get('temperature_2m_min', [])[0]
                result['max_temp'] = daily.get('temperature_2m_max', [])[0]
                return result

        except Exception:
            return False


    def get_weather_in_city(self):
        try:
            if coords := self.get_coordinates():
                if weather := self.request_weather(*coords):
                    return weather
                else:
                    return {'error': 'no connect'}
            else:
                return {'error': 'no city'}

        except Exception:
            return {'error': 'no connect'}
