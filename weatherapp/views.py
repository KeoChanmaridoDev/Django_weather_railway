from django.shortcuts import render, redirect
import requests
from .models import City
from django.contrib import messages
# Create your views here.
def home(request):


    #Define Api and base URL for openweather
    api_key = '6e4cb3ffa3e72ab954b69b78cd9bb5d8'
    url= 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'


    # Check if the request is a POST(When add new city)
    if request.method == 'POST':
       city_name = request.POST.get('city') # City app from the form
       # Fetch weather data from  the city from API
       response = requests.get(url.format(city_name, api_key)).json()
       # Check If the city exits in the API
       if response['cod'] == 200:
          if not City.objects.filter(name = city_name).exists():
              # Save the newCity to database
              City.objects.create(name= city_name)
              messages.success(request, f'{city_name} has been  add succesfully')
          else:
              messages.info(request, f'{city_name} alrady exists')
       else:
           messages.error(request, f'City {city_name} does not exist')

       return redirect('home')
    weather_data = []
    # Fetch Data weather for all 
    try:
      cities = City.objects.all() # Get all the City from the database
      for city in cities:
        response = requests.get(url.format(city.name, api_key)).json()
        data = response
        if data['cod'] == 200:
            weather = {
                'city': city.name,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
            }
            weather_data.append(weather)
        else:
            City.objects.filter(name=city.name).delete()
    except requests.RequestException as e:
        print("Error can't find the city name")

    context = {'weather_data': weather_data}
    return render(request, 'weather.html', context)
