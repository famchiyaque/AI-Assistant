# from functions.elevenlabs import gen_voice_response

# gen_voice_response("got it")

activationword = 'jackson'

def testing(query):
    if activationword in query:
        indexes = []
        for word in query:
            print("word ", word, "index ", query.index(word))
            indexes.append(query.index(word))
            if word == activationword:
                break
        for i in range(len(indexes)):
            query.pop(0)
        
        print("query after popping jackSon: ", query)

query = ['hey', 'jackson', 'spotify', 'play', 'hey', 'jackson', 'spotify', 'play']

print(query)

testing(query)