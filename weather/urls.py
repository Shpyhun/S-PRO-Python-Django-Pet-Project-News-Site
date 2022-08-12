from django.urls import path

from weather.views import WeatherView, WeatherHomeView

urlpatterns = [
    path('weather/index',  WeatherHomeView.as_view(), name='weather_index'),
    path('weather/', WeatherView.as_view(), name='weather'),
]
