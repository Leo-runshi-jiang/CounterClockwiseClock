import speech_recognition as sr
import pyttsx3
from wit import Wit


access_token = "T2WAZPX3A4R5W47UNZEICGC4V4GJHBXX"
voiceID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"


def listen(time):
    r = sr.Recognizer()
    m = sr.Microphone()
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    print("I am listening, go ahead")
    try:
        with m as source: audio = r.listen(source, 3, 6)
        print("----Recognizing----")
        client = Wit(access_token)
        resp = client.speech(audio.get_wav_data(), {'Content-Type': 'audio/wav',"reference_time":time})
        print("finished recognizing")
        return(interpret_resp(resp))
    except Exception as e:
        return(e)

def interpret_resp(resp):
    #takes api responce and interprets it
    print('Yay, I got this response: ' + str(resp))
    print(f"you said: {resp['text']}")

    returndic = {}

    #record the text of the speech
    returndic["text"] = resp["text"]

    #go through each key and record their values, if value does not exist, record body
    #data structure changes for location, so account for difference
    for key in resp["entities"]:
        try:
            if key == "wit$location:location":
                city = resp["entities"][key][0]["body"]
                lon = resp["entities"][key][0]["resolved"]["values"][0]["coords"]["long"]
                lat = resp["entities"][key][0]["resolved"]["values"][0]["coords"]["lat"]
                returndic[key] = {"city": city, "lon":lon, "lat":lat}
                print(returndic[key])
            else:
                returndic[key] = resp["entities"][key][0]["value"]
        except KeyError:
            returndic[key] = "data not found"
            print("data not found")

    #returns a dictionary in the format of {'text':'whatever was said','entity1':'value of entity', 'entity2':'value of entity 2'
    return returndic

def say(text):
    v = pyttsx3.init()
    v.setProperty("rate", 160)
    v.setProperty("voice", voiceID)
    v.say(" " + text)
    v.runAndWait()


