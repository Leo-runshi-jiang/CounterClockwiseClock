import time
from playsound import playsound
import json

# all the alarms are stored in a txt file in the form of a dictionary

#the format goes {
#this module creates, writes to, read, and edits the alarm file
#as well as sound the alarm
def json_navigate(data, path):
    #this function navigates to part of the data dictionary variable
    #following the path variable which is a list of keys
    current_level = data
    for key in path:
        if key in current_level:
            current_level = current_level[key]
        else:
            raise KeyError(f"Key path '{'.'.join(path)}' not found in the alarm json file.")
    return current_level


def set_alarm(path,alarm_time):
    #Sets an alarm by updating json file storing alarm info
    #alarm_type_path stores the path to the json entry that should be added
    #alarm time is the string that should be added
    #note: the json file is set such that the lowest level is always a list
    try:
        with open("alarm.json", "r") as f:
            alarm_data = json.load(f)

        #append alarm_time to the list located by path
        new_data = json_navigate(alarm_data, path).append(alarm_time)
        
    except Exception as e:
        print(f"An error occurred while setting the alarm: {e}")

def ring_alarm():
    playsound("alarm_sound.mp3")

#ring_alarm()
set_alarm(["weekly","monday"],"08:00")