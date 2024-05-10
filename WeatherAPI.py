import requests
import datetime
import time
def get_weather_data(location, country = "CA"):
    #function that fetches weather data from the open weather api
    #and returns basic info such as tempurature, weather, and rain/snow amount as well as the json file
    #location is a city, time is assumed to be now, and needs to be put in a string of "yyyy-mm-dd"
    api_key = "62c31e7df36a63f3d0dce16c2291be3a"

    #first get the coordinates of the city
    location_data = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={location},{country}&limit=3&appid={api_key}")

    #store the lon lat and province/state obtained
    lon, lat, state = location_data.json()[0]["lon"], location_data.json()[0]["lat"], location_data.json()[0]["state"]

    #since there are 2 types of calls, we can separate by date = "now"
    #when date = "now" we can do a more precise data fetch
    weather_data = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&exclude=hourly&appid={api_key}")
    temp = weather_data["current"]["temp"]
    weather = weather_data[""]

get_weather_data("hamilton","2024-05-10")