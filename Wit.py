import json
from wit import Wit

access_token = "CHMLCK5BEHTIYOWJQCLLNMBOI52INW6S"

client = Wit(access_token)
resp = None
with open('What_is_the_weather.wav', 'rb') as f:
  resp = client.speech(f, {'Content-Type': 'audio/wav'})
print('Yay, got Wit.ai response: ' + str(resp))