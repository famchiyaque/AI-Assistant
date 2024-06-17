import speech_recognition as sr
import openai
import os
import pyttsx3

# Set your OpenAI API key here
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Initialize the recognizer and microphone
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Function to recognize speech
def recognize_speech():
    with microphone as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio_data = recognizer.listen(source)  # Listen for speech input

    try:
        # Use Google Web Speech API to recognize the speech
        user_input = recognizer.recognize_google(audio_data)
        print("You said: " + user_input)
        return user_input
    except sr.UnknownValueError:
        print("Google Web Speech API could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Web Speech API; {0}".format(e))

# Function to generate response using ChatGPT
def get_chatgpt_response(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None
    )
    return response.choices[0].text.strip()

# Function to speak the response
def speak_response(response):
    voice = pyttsx3.init()
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"
    voice.setProperty('voice', voice_id)
    voice.say(response)
    voice.runAndWait()

# Main function
if __name__ == "__main__":
    while True:
        user_input = recognize_speech()  # Get user's speech input
        if user_input.lower() == "exit":  # Exit the program if the user says "exit"
            break

        chatgpt_prompt = "User: " + user_input  # Construct the prompt for ChatGPT
        chatgpt_response = get_chatgpt_response(chatgpt_prompt)  # Get ChatGPT response
        print("ChatGPT: " + chatgpt_response)
        
        speak_response(chatgpt_response)  # Speak the response