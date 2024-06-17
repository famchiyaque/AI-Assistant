from datetime import datetime
from logging.config import listen
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import pyaudio
import time
import pygame
import os
from ctypes import *
from contextlib import contextmanager
import requests

# speech engine initialization
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id) # 0 = male, 1 = female
activationword = 'milo'

# Choose your default browser
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register("chrome", None, webbrowser.BackgroundBrowser(chrome_path))

# API key from wolframalpha
appId = "3JUG5V-TEXR92KJ54"
wolframClient = wolframalpha.Client(appId)

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    try: 
        asound = cdll.LoadLibrary('libasound.so')
        asound.snd_lib_error_set_handler(c_error_handler)
        yield
        asound.snd_lib_error_set_handler(None)
    except:
        yield
        print('')

def speak(text, rate = 150): #rate can be varied of how fast ai speaks
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def parseCommand():
    with noalsaerr():
        listener = sr.Recognizer()
        speak("Listening for a command")

        with sr.Microphone() as source:
            listener.adjust_for_ambient_noise(source, duration= 0.2)
            listener.pause_threshold = 3
            input_speech = listener.listen(source, timeout = 4, phrase_time_limit=10)

        try: 
            print("Recognizing speech... ")
            query = listener.recognize_google(input_speech)
            print(f"The input speech was: {query}" )
    
        except Exception as exception:
            speak("I did not quite catch that")
            print(exception)

            return 'None'
    
        return query

def wiki_search(query = ''):
    searchResults = wikipedia.search(query)
    if not searchResults:
        print("No wikipedia results")
        return "No results recieved"
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary      

# my own added API, search for city information by name
URL = "https://city-by-api-ninjas.p.rapidapi.com/v1/city"

def search_city(city):
    querystring = {"name":city,"country":"US","limit":"1"}
    headers = {
	    "X-RapidAPI-Key": "b86afe5666msh410c2ed2d3d8a1fp150b79jsnfcad51eb0f9d",
	    "X-RapidAPI-Host": "city-by-api-ninjas.p.rapidapi.com"
    }
    response = requests.get(URL, headers=headers, params=querystring)
    print(response.json())
    return response

def list_or_dict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']


def search_wolframalpha(query = ''):
    response = wolframClient.query(query)

    # @success: Wolfram was able to resolve the query
    # @numpods: Number of results returned
    # pod: list of results. Can also contain subpods
     
    if response['@success'] == 'false':
        return "Could not compute"
    
    # query resolved
    else:
        result = ' '
        # Question
        pod0 = response['pod'][0]

        pod1 = response['pod'][1]
        # may contain the answer, pod with highest confidence value
        # if it's primary or has the title of result or definition, then it's the official result
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            # Get the result
            result = list_or_dict(pod1['subpod'])
            # remove bracketed section
            return result.split('(')[0]
        else:
            question = list_or_dict(pod0['subpod'])
            return question.split('(')[0]
            # search wikipedia instead
            speak('Computation failed, querying universal databank')
            return wiki_search(question)



# Main Loop
if __name__ == '__main__':
    speak("What's up doc?", 150)

    while True:
        query = parseCommand().lower().split()
        print("You said: ", end=" ")

        if query[0] == activationword:
            query.pop(0)

        # List Commands
        if query[0] == 'say':
            if 'hello' in query:
                speak("Greetings, all.")
            else:
                query.pop(0) # remove 'say'
                speech = ' '.join(query)
                speak(speech)

            # Open a website
            if query[0] == 'go' and query[1] == 'to':
                speak("Opening...")
                query = ' '.join(query[2:])
                webbrowser.get("chrome").open_new(query)

            # Search Wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak("Let's check the web")
                time.sleep(2)
                speak(wiki_search(query))
            
            # WolframAlpha
            if query[0] == 'wolfram' or query[0] == 'compute':
                query = ' '.join(query[1:])
                speak('Computing')
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak("Unable to compute")
                    speak("Maybe there's something wrong with your API key")

            # record all results
            if query[0] == 'log':
                speak('Ready to record your note')
                newNote = parseCommand().lower()
                now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(newNote)
                speak("Note written")

            if query[0] == 'exit':
                speak("Goodbye")
                break
            
            if query[0] == 'listen':
                speak("I know right. Get that man some boof")
                break

            if query[0] == 'city':
                speak("Let's see...")
                city = query[1]
                try:
                    result = search_city(city)
                    speak(result)
                except:
                    speak("Failed")
            
            #if query[0] == 'insight':
             #   query.pop(0) # remove insight
              #  query = ' '.join(query)
               # speech = query_openai(query)
                #speak("Ok")
                #speak(speech)