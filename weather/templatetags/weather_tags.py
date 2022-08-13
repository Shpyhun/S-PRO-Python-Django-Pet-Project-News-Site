from datetime import datetime

import requests
from django import template
from django.shortcuts import render

# register = template.Library()
#
#
# @register.inclusion_tag('weather/index.html')
# def get_weather(request):
#     url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + os.environ.get('WEATHERID')
#     city = 'London'
#     res = requests.get(url.format(city)).json()
#     city_info = {
#         'city': city,
#         'description': res['weather'][0]['description'],
#         'temp': res['main']['temp'],
#         'icon': res['weather'][0]['icon'],
#     }
#     day = datetime.date.today()
#     context = {
#         # 'day': day,
#         # 'title': 'Weather',
#         'info': city_info,
#
#     }
#     return render(request, context)
