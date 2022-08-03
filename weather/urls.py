from django.urls import path

from weather.views import weather

urlpatterns = [
    path('', weather, name='weather'),
]
