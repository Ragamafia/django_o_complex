from django.shortcuts import render

from get_weather.src.utils import Weather


def index_page(request):
    return render(request, 'index.html')

def get_weather(request):
    if request.method == 'POST':
        if city_name := request.POST.get('city'):
            if data := Weather(city_name).get_weather_in_city():

                if 'error' not in data:
                    return render(request, 'weather.html', data)
                elif 'no city' in data.values():
                    return render(request, 'no_city.html')
                elif 'no connect' in data.values():
                    return render(request, 'unavailable.html')
