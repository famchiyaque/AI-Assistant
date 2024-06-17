# Python program to show 
# how to convert text to speech 
import pyttsx3 

# Initialize the converter 
voice = pyttsx3.init() 

# Set properties before adding 
# Things to say 

voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"

voice.setProperty('voice', voice_id)
# Sets speed percent 
# Can be more than 100 
voice.setProperty('rate', 150) 
# Set volume 0-1 
voice.setProperty('volume', 0.7) 

# Queue the entered text 
# There will be a pause between 
# each one like a pause in 
# a sentence 
voice.say("Que honda Fer, sabes que el unico que puede cambiar tu futuro eres tu") 
voice.say("No te sientas mal por tu pasado, mejor sientete emocionado del futuro") 

# Empties the say() queue 
# Program will not continue 
# until all speech is done talking 
voice.runAndWait()
