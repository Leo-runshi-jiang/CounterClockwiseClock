import time
from playsound import playsound

# all the alarms are stored in a txt file in the form of a dictionary

#the format goes {
#this module creates, writes to, read, and edits the alarm file
#as well as sound the alarm
def set_alarm(alarm_time_unix, filename="alarm.json"):
    #Sets an alarm by writing the specified Unix time to the file.
    try:
        with open(filename, "w") as file:
            file.write(str(alarm_time_unix))
        print(f"Alarm set for Unix time: {alarm_time_unix}")
    except Exception as e:
        print(f"An error occurred while setting the alarm: {e}")

def ring_alarm():
    playsound("alarm_sound.mp3")

#ring_alarm()