from datetime import datetime
from logging.config import listen
import speech_recognition as sr
import pyttsx3
import webbrowser
import pyaudio
import time
# import pygame
import os
from ctypes import *
# from contextlib import contextmanager
# from selenium import webdriver
from playsound import playsound
from functions.elevenlabs import gen_voice_response
# from functions.spotify_player import spotify_player
from functions.wiki import wiki_search
from functions.wolfram import search_wolframalpha
from functions.greetings import get_greeting
from functions.spotify_apis import spotify_api, get_spot_instance, start_spotify
from functions.volume import mod_volume
from functions.kanyerest import get_kanye_quote
from functions.browser_call import open_platform

# speech engine initialization
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[0].id) # 0 = male, 1 = female
activationword = 'jackson'

lastCall = datetime.now().timestamp() * 1000
session = True
bad_listens = 0

spot_access_token = ''
spot_expire_date = 0

# Choose your default browser
browser_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
webbrowser.register("edge", None, webbrowser.BackgroundBrowser(browser_path))

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

def speak(text, rate = 150): #rate can be varied of how fast ai speaks
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()


def parseCommand(lastCall):
    # global bad_listens
    # print("current bad listens: ", bad_listens)
    # if bad_listens >= 5:
    #     return ['exit']

    global session
    if (session == True):
        print("session is true")
        newTime = datetime.now().timestamp() * 1000
        if newTime - lastCall > 120000:
            print("120 seconds have passed since lastCall, session now false and sleeper mode")
            session = False
            playsound('./audio/jackSon_off.mp3')

    listener = sr.Recognizer()
    # speak("Listening for a command")

    with sr.Microphone() as source:
        print("adjuting for ambient noise")
        listener.adjust_for_ambient_noise(source, duration= 3)
        listener.pause_threshold = 2
        listener.energy_threshold = 300
        print("listening for a command")
        input_speech = listener.listen(source, timeout = None, phrase_time_limit = None)

    try: 
        print("Recognizing speech... ")
        query = listener.recognize_google(input_speech).lower().split()
        print(f"The input speech was: {query}" )
    
    except Exception as exception:
        # speak("I did not quite catch that")
        print("I did not quite catch that")
        print(exception)
        print("returning None to main function")
        bad_listens += 1
        return None
    
    # global lastCall

    bad_listens = 0
    
    newCall = datetime.now().timestamp() * 1000
    
    print("new call minus last call is ", newCall - lastCall)
    if newCall - lastCall <= 120000:
        print("newCall has been made within 120 seconds, sending query")
        lastCall = newCall
        session = True
        return query
    elif activationword in query:
        lastCall = newCall
        if session == False:
            print("session was false, and activation word was in query, powering on")
            session = True
            playsound('./audio/jackSon_on.mp3')
        return query
    else:
        return None
    
# Main Loop
if __name__ == '__main__':
    playsound("./audio/" + get_greeting())

    while True:
        query = parseCommand(lastCall)
        # query = input("What's the command? \n").lower().split()
        print("You said: ", query)
        # playsound('./audio/jackSon_on.mp4')

        if query == None:
            time.sleep(5)
            continue

        if activationword in query:
            indexes = []
            for word in query:
                indexes.append(query.index(word))
                if word == activationword:
                    break
            for i in range(len(indexes)):
                query.pop(0)
            if query == []:
                playsound('./audio/jackSon_on.mp3')
                playsound("./audio/" + get_greeting())
                continue

        # queryProcessing()

        # List Commands
        if query[0] == 'open':
            query.pop(0)
            result = open_platform(query[0])
            if result != '':
                speak(result)
        
        # Open a website
        if query[0] == 'go' and query[1] == 'to':
            speak("Opening...")
            query = ' '.join(query[2:])
            webbrowser.get("edge").open_new(query)

        if query[0] == 'look' and query[1] == 'up':
            query = query[2:]
            # look_up(query)
            print("not done")

        if query[0] == 'say':
            speech = ' '.join(query[1:])
            speak(speech)

        if query[0] == 'volume':
            mod_volume(query)

        if query[0] == 'kanye':
            quote = get_kanye_quote()
            speak(quote)

        if query[0] == 'start' and query[1] == 'spotify':
            start_spotify(spot_access_token)

        if query[0] == 'spotify':
            print("access token saved in script: " + spot_access_token)
            print("expire date of said token")
            print(spot_expire_date)
            current_time_in_ms = int(datetime.now().timestamp() * 1000)
            if spot_access_token == '' or spot_expire_date < current_time_in_ms:
                print("token doesn't exist or expired, creating new session")
                instance_info = get_spot_instance()
                if instance_info != '':
                    spot_access_token = instance_info[0]
                    spot_expire_date = instance_info[1]
                    print("using newly created token for spotify api")
                    result = spotify_api(spot_access_token, query[1])
                    print(result)
                else:
                    print("error creating new session")
            else:
                print("using current access token for spotify api")
                result = spotify_api(spot_access_token, query[1])
                print(result)

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
        
        if query[0] == 'record':
            text = ' '.join(query[1:])
            result = gen_voice_response(text)
            speak(result)

        if query[0] == 'listen':
            playsound('./audio/boof.mp3')

        if query[0] == 'exit':
            playsound('./audio/jackSon_off.mp3')
            # speak("Goodbye")
            break
                        
            #if query[0] == 'insight':
             #   query.pop(0) # remove insight
              #  query = ' '.join(query)
               # speech = query_openai(query)
                #speak("Ok")
                #speak(speech)