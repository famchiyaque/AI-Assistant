import pyttsx3
import wikipedia

voice = pyttsx3.init()

#voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"

#voice.setProperty('voice', voice_id)

query = input("Search something with wikipedia: ")
result = wikipedia.summary(query, sentences = 1)
print(result)

voice.say(result)
voice.runAndWait()