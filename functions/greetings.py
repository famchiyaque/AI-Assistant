import random

audio_files = [
    "greeting_1.mp3", "greeting_2.mp3", "greeting_3.mp3", "greeting_4.mp3"
]

def get_greeting():
    num = random.randint(1, 4)
    if (num == 1):
        return audio_files[0]
    elif (num == 2):
        return audio_files[1]
    elif (num == 3):
        return audio_files[2]
    elif (num == 4):
        return audio_files[3]
    else:
        print("no valid number")
        return num