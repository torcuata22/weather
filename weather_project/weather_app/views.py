import datetime
import requests
from django.shortcuts import render

# Create your views here.

def index(request):
    #Read the api key from he file
    API_KEY=open("API_KEY","r").read()
    #url for "NOW" info (from docs):
    current_weather_url="https://api.openweathermap.org/data/2.5/weather?q={}&appid={}" #{} is for dynamic data
    forecast_url="https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}$exclude=current,minutely,hourly,alerts&appid={}" #{} is for dynamic data
    #check kind of request
    #If it's a POST request:
    if request.method == "POST":
        city1 = request.POST['city1'] #mandatory
        city2 = request.get('city2',None) #try to get it, but if it's not there, it's fine
        weather_data1, daily_forecasts1 = fetch_weather_forecast(city1, API_KEY, current_weather_url, forecast_url)
        if city2:
            weather_data2, daily_forecasts2=fetch_weather_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None
        context = {
            "weather_data1":weather_data1,
            "daily_forecast1":daily_forecasts1,
            "weather_data2":weather_data2,
            "daily_forecast2":daily_forecasts2,
        }
        return render(request,"weather_app/index.html", context)

    #if it's a GET request:
    else:
        return render(request,"weather_app/index.html")
    

#Not an endpoint:
def fetch_weather_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city,api_key)).json()
    lat,lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat,lon,api_key)).json()

    weather_data = {
        "city":city,
        "temperature":round(response['main']['temp']-273.15, 2),
        "description":response["weather"][0]["description"],
        "icon":response['weather'][0]['icon'],
    }

    daily_forecasts = []
    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append({
            "day":datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
            "min_temp":round(daily_data['temp']['min'] - 273.15, 2),
            "max_temp":round(daily_data['temp']['max'] - 273.15, 2),
            "description":daily_data['weather'][0]['description'],
            "icon":daily_data['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts