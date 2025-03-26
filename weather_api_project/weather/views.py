import requests
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CitySerializer


# Create your views here.
OPENWEATHER_API_KEY = 'b0621f5dd1db0bf33d89bea3fb48f71d'  # Replace with your actual API key

class WeatherView(APIView):
    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data['city']
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric'
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

