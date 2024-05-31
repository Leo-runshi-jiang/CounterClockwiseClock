import VoiceControl as vc
import WeatherAPI as wapi
import time
from datetime import datetime

def unix_to_iso(unix_time):
    return str(datetime.fromtimestamp(unix_time).isoformat())
def main():
    if "weather:weather" in vc.listen():
        vc.say(wapi.show_weather_data(time = unix_to_iso(time.time())))

print(unix_to_iso(time.time()))
#main()