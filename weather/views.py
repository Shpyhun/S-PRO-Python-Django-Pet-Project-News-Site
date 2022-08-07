import datetime
import os

import requests
from django.shortcuts import render
from django.views import View

from news.views import menu
from weather.models import City


class WeatherView(View):

    def get(self, request):
        url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + os.environ.get('WEATHERID')
        cities = City.objects.all()
        all_cities = []
        for city in cities:
            res = requests.get(url.format(city.name)).json()
            city_info = {
                'city': city.name,
                'description': res['weather'][0]['description'],
                'temp': res['main']['temp'],
                'icon': res['weather'][0]['icon'],
            }
            all_cities.append(city_info)
        day = datetime.date.today()
        context = {
            'menu': menu,
            'title': 'Weather',
            'all_info': all_cities,
            'day': day,
        }
        return render(request, 'weather/weather.html', context)
