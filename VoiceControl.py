import speech_recognition as sr
import pyttsx3
import playsound
from gtts import gTTS
import json
from wit import Wit

access_token = "T2WAZPX3A4R5W47UNZEICGC4V4GJHBXX"
voiceID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
def listen():
    r = sr.Recognizer()
    m = sr.Microphone()
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    print("I am listening, go ahead")
    try:
        with m as source: audio = r.listen(source, 3, 6)
        print("----Recognizing----")
        client = Wit(access_token)
        resp = client.speech(audio.get_wav_data(), {'Content-Type': 'audio/wav'})
        return(interpret(resp))
    except:
        #return("error")
        pass

def interpret(resp):
    #takes api responce and interprets it
    print('Yay, I got this response: ' + str(resp))
    print(f"you said: {resp['text']}")

    returndic = {}

    returndic["text"] = resp["text"]

    for key in resp["entities"]:
        returndic[key] = resp["entities"][key][0]["body"]

    #returns a dictionary in the format of {'text':'whatever was said','entity1':'value of entity', 'entity2':'value of entity 2'
    return returndic



def say(text):
    v = pyttsx3.init()
    v.setProperty("rate", 160)
    v.setProperty("voice", voiceID)
    v.say(" " + text)
    v.runAndWait()

def text_to_speech(text):
    #since always cuts off first sylible, b is added as place holder
    mytext = "A " + text
    language = 'en'
    myobj = gTTS(text=mytext, lang=language, slow=False)
    myobj.save("speech.mp3")
    playsound.playsound("speech.mp3")

