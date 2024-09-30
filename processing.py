from functions.spotify_player import spotify_player
from functions.wiki import wiki_search
from functions.wolfram import search_wolframalpha
from functions.greetings import get_greeting
from functions.spotify_apis import spotify_api, get_spot_instance
from functions.volume import mod_volume





def queryProcessing(query):
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

        if query[0] == 'exit':
            speak("Goodbye")
            break
            
        if query[0] == 'listen':
            playsound('./audio/boof.mp3')
            # speak("I know right. Get that man some boof")
            
            #if query[0] == 'insight':
             #   query.pop(0) # remove insight
              #  query = ' '.join(query)
               # speech = query_openai(query)
                #speak("Ok")
                #speak(speech)
