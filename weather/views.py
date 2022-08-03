import datetime

import requests
from django.shortcuts import render

from news.views import menu
from weather.models import City


def weather(request):
    api_key = '6867a217a4843aa95e5a3195b528843c'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key
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


