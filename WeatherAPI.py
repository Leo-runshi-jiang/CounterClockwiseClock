import requests
import json
import time

city = "hamilton" #global var storing what city we are in
def get_weather_data(location, country = "CA"):
    #function that fetches weather data from the open weather api, this function is not called in main, only conditionally
    #by other functions
    #It contacts the open weather api and writes results into the weather_data.json file

    api_key = "62c31e7df36a63f3d0dce16c2291be3a"

    #first get the coordinates of the city
    location_data = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={location},{country}&limit=3&appid={api_key}")

    #store the lon lat and province/state obtained
    lon, lat, state = location_data.json()[0]["lon"], location_data.json()[0]["lat"], location_data.json()[0]["state"]

    #fetch weather data hourly, it is a list of dictionaries where index = hours after request
    weather_data = requests.get(f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&units=metric&exclude=minutely,alerts&appid={api_key}").json()

    #saves data as json file
    with open('weather_data.json', 'w') as f:
        json.dump(weather_data, f)

    print(f"------DATA UPDATED ------\n on {time.time()}")

#check if weatherdata.txt has been created, if not, create and update it.
def json_file_setup():
    try:
        #when the file exists
        with open('weather_data.json') as file:
            weather_data = json.load(file)
            current_unix_time = time.time()
            last_update_time = weather_data["current"]["dt"]

            #if the file was not updated in a hour, update it
            if current_unix_time - last_update_time >= 3600:
                get_weather_data(city)
                print("weather data was updated since last update was more than an hour ago ")
                print(f"last update was on {last_update_time}, it is now {current_unix_time}")
            else:
                print("the data was updated recently, no need for updates")
    except:
        #when it does not exist, update it
        get_weather_data(city)
        print("created new file for weather data json on start up")
def show_weather_data():
    # function which displays the weather data by reading json file
    #MUST BE UPDATED DAILY
    with open('weather_data.json') as f:
        weather_data = json.load(f)
        unix_time = int(time.time())
        last_update_time = weather_data["current"]["dt"]

        # extract useful entries from json data, first check how many days/ hours its been since last update
        hours_since_update = (unix_time - last_update_time) // 3600
        current_temp = weather_data['hourly'][hours_since_update]["temp"]
        current_feels_like = weather_data['hourly'][hours_since_update]["feels_like"]
        current_weather = weather_data['hourly'][hours_since_update]["weather"][0]["description"]
        daily_summary = weather_data['daily'][0]["summary"]
        daily_temp_max = weather_data['daily'][0]["temp"]["max"]
        daily_temp_min = weather_data['daily'][0]["temp"]["min"]

        print(f"The current temperature in {city} is {current_temp} °C, feels like {current_feels_like} °C. The weather is {current_weather}")
        print(f"{daily_summary}, with a max of {daily_temp_max} °C, and a min of {daily_temp_min} °C")

        return f"The current temperature in {city} is {current_temp} °C, feels like {current_feels_like} °C. The weather is {current_weather}\n{daily_summary}, with a max of {daily_temp_max} °C, and a min of {daily_temp_min} °C"


def main():
    json_file_setup()
    show_weather_data()

while True:
    main()
    time.sleep(10)