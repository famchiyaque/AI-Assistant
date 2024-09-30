import speech_recognition as sr


# List all microphone devices
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f"Microphone with index {index}: {name}")



def parseCommand():
    listener = sr.Recognizer()
    print("Listening for a command")

    with sr.Microphone(device_index=2) as source:
        listener.adjust_for_ambient_noise(source, duration= 1)
        listener.pause_threshold = 3
        input_speech = listener.listen(source, timeout = None, phrase_time_limit = None)
        print("on to try catch")

    try: 
        print("Recognizing speech... ")
        query = listener.recognize_google(input_speech)
        print(f"The input speech was: {query}" )
    
    except Exception as exception:
        print("I did not quite catch that")
        print(exception)

        return 'None'
    
    return query

print(parseCommand().lower().split())