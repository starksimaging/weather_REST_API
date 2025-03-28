import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CitySerializer
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
OPENWEATHER_API_KEY = 'b0621f5dd1db0bf33d89bea3fb48f71d'  # Replace with your actual API key

class WeatherView(APIView):
    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data['city']
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=imperial'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return Response({
                    'city': city,
                    'temperature': data['main']['temp'],
                    'weather': data['weather'][0]['description'],

                })
            else:
                return Response({'error': 'City not found'}, status= status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@csrf_exempt
def weather_form(request):
        weather = None
        error = None

        if request.method == 'POST':
            city = request.POST.get('city')
            if city:
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=imperial'
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    weather = {
                        'city': city,
                        'temperature': data['main']['temp'],
                        'description': data['weather'][0]['description'],
                    }
                else:
                    error = 'City not found'
        return render(request, 'weather/weather_form.html', {'weather': weather, 'error': error})


