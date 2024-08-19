import VoiceControl as vc
import WeatherAPI as wapi
import Alarm as al
import time
from datetime import datetime

def unix_to_iso(unix_time):
    return str(datetime.fromtimestamp(unix_time).isoformat())

def ext_iso_to_unix(ext_iso_time):
    basic_iso_time = ext_iso_time[:-6].replace('-', '').replace(':', '')
    return int(datetime.fromisoformat(basic_iso_time).timestamp())

def detect_request_for_daily_weather(iso_ext_time):
    #function that determines if the request is for daily data as opposed to hourly data
    if iso_ext_time[11:23] == "00:00:00.000":
        return True
    else:
        return False

def process_commands(APIresp):
    #weather related requests
    if "weather:weather" in APIresp:
        #create a dictionary of keyword arguments that need to be passed
        weather_argument_dic = {}
        if "wit$datetime:datetime" in APIresp:
            #if there is a specific time, convert to unix and add to dictionary
            iso_ext_time = APIresp["wit$datetime:datetime"]
            target_time = ext_iso_to_unix(iso_ext_time)
            weather_argument_dic["time"] = target_time

            if detect_request_for_daily_weather(iso_ext_time):
                #change from hourly to daily
                weather_argument_dic["mode"] = "daily"

        if "wit$location:location" in APIresp:
            #if there is a specific location specify
            weather_argument_dic["city"] = APIresp["wit$location:location"]["city"]
            weather_argument_dic["lon"] = APIresp["wit$location:location"]["lon"]
            weather_argument_dic["lat"] = APIresp["wit$location:location"]["lat"]

        #code that runs after all keyword arguments have been determined
        print(weather_argument_dic)
        vc.say(wapi.show_weather_data(**weather_argument_dic))

    #alarm related commands
    if "alarm:alarm" in APIresp:
        if "create:create" in APIresp:
            alarm_set_time = ext_iso_to_unix(APIresp["wit$datetime:datetime"])
            al.set_alarm(alarm_set_time)

def main():
    iso_time = str(unix_to_iso(time.time()))

    #calls to wit api to interpret speech, needs to give it iso time so the api can handle the dates and time
    APIresp = vc.listen(iso_time)
    #calls the correct functions depending on api responce
    process_commands(APIresp)

main()