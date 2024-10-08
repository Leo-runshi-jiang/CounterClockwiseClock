import requests
import json
import time
from dotenv import load_dotenv
import os
from datetime import datetime


def get_coords(location):

    load_dotenv()
    api_key = os.getenv("open_weather_api_key")

    # first get the coordinates of the city
    location_data = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=2&appid={api_key}")

    # store the lon lat and province/state obtained
    lon, lat, state = location_data.json()[0]["lon"], location_data.json()[0]["lat"], location_data.json()[0]["state"]

    return {"lon": lon, "lat": lat, "state": state}


def get_weather_data(city,lon,lat):
    #function that fetches weather data from the open weather api, this function is not called in main, only conditionally
    #by other functions
    #It contacts the open weather api and writes results into the weather_data.json file

    load_dotenv()
    api_key = os.getenv("open_weather_api_key")

    #not needed anymore since wit provides coordinats
    #coords = get_coords(location)
    #lat, lon, state = coords["lat"], coords["lon"], coords["state"]

    #fetch weather data hourly, it is a list of dictionaries where index = hours after request
    weather_data = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,alerts&appid={api_key}").json()

    #saves data as json file
    with open(f'weather_data_{city}.json', 'w') as f:
        json.dump(weather_data, f)

    print(f"------DATA UPDATED ------\n on {time.time()}")

#check if weatherdata.txt has been created, if not, create and update it.
def json_file_update(city,lon,lat):
    try:
        #when the file exists
        with open(f'weather_data_{city}.json') as file:
            weather_data = json.load(file)
            current_unix_time = time.time()
            last_update_time = weather_data["current"]["dt"]

            #if the file was not updated in a hour, update it
            if current_unix_time - last_update_time >= 7200:
                get_weather_data(city,lon,lat)
                print(f"weather data of {city} was updated since last update was more than two hours ago ")
                print(f"last update was on {last_update_time}, it is now {current_unix_time}")
            else:
                print(f"the data for {city} was updated recently, no need for updates")
    except:
        #when it does not exist, update it
        get_weather_data(city,lon,lat)
        print("created new file for weather data json on start up")
def show_weather_data(city = "hamilton", lat = 43.2501106262207, lon = -79.8496322631836, time = int(time.time()), mode = "hourly"):
    #updates json data first
    json_file_update(city,lon,lat)
    # function which displays the weather data by reading json file
    #MUST BE UPDATED DAILY
    with open(f'weather_data_{city}.json') as f:
        #try:
        #convert times into datetime object
        current_time = datetime.now()
        target_time = datetime.fromtimestamp(time)

        # extract useful entries from json data, first check how many days/ hours its been since last update
        weather_data = json.load(f)

        current_time = current_time.replace(minute=0, second=0, microsecond=0)
        target_time =  target_time.replace(minute=0, second=0, microsecond=0)
        hours_since_update = (target_time - current_time).seconds//3600

        current_time = current_time.replace(hour=0)
        target_time = target_time.replace(hour=0)
        days_since_update = (target_time - current_time).days

        print(f"data requested for {time}, its been {hours_since_update} hours ({days_since_update} days), the file was updated {weather_data['current']['dt']}")
        daily_summary = weather_data['daily'][days_since_update]["summary"]
        daily_temp_max = weather_data['daily'][days_since_update]["temp"]["max"]
        daily_temp_min = weather_data['daily'][days_since_update]["temp"]["min"]

        if mode == "hourly":

            current_temp = weather_data['hourly'][hours_since_update]["temp"]
            current_feels_like = weather_data['hourly'][hours_since_update]["feels_like"]
            current_weather = weather_data['hourly'][hours_since_update]["weather"][0]["description"]

            print(f"The temperature in {city} is {current_temp} °C, feels like {current_feels_like} °C. There will be {current_weather}")
            print(f"{daily_summary}, with a max of {daily_temp_max} °C, and a min of {daily_temp_min} °C")

            return f"The temperature in {city} is {current_temp} °C, feels like {current_feels_like} °C. There will be {current_weather}\n{daily_summary}, with a max of {daily_temp_max} °C, and a min of {daily_temp_min} °C"
        elif mode == "daily":
            print(f"{daily_summary}, with a max of {daily_temp_max} °C, and a min of {daily_temp_min} °C")
            return f"{daily_summary}, with a max of {daily_temp_max} °C, and a min of {daily_temp_min} °C"
        '''
        except Exception as e:
            returnstr = f"sorry, I can only know the exact weather of the next {len(weather_data['hourly'])} hours or the daily weather of the next {len(weather_data['daily'])} days"
            print(returnstr)
            print(e)
            return returnstr'''