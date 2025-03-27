from django.urls import path
from .views import WeatherView
from .views import weather_form

urlpatterns = [
    path('get-weather/', WeatherView.as_view(), name='get-weather'),
    path('', weather_form, name='weather-form')
]