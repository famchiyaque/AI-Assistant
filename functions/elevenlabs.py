# Import necessary libraries
import requests  # Used for making HTTP requests
import json  # Used for working with JSON data
import sys
import os

# Add the project level to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import from config
from config import XI_LABS_API_KEY

# Define constants for the script
CHUNK_SIZE = 1024  # Size of chunks to read/write at a time
VOICE_ID = "bIHbv24MWmeRgasZH58o"  # voice of will
OUTPUT_PATH = "./audio/output.mp3"  # Path to save the output audio file
# temp = "./audio/greeting_4.mp3"

# Construct the URL for the Text-to-Speech API request
tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"

# Set up headers for the API request, including the API key for authentication
headers = {
    "Accept": "application/json",
    "xi-api-key": XI_LABS_API_KEY
}

def gen_voice_response(text):
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True
        }
    }
    # Make the POST request to the TTS API with headers and data, enabling streaming response
    response = requests.post(tts_url, headers=headers, json=data, stream=True)

    # Check if the request was successful
    if response.ok:
        # Open the output file in write-binary mode
        # os.makedirs(temp, exist_ok=True)
        with open(OUTPUT_PATH, "wb") as f:
            # Read the response in chunks and write to the file
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(chunk)
        # Inform the user of success
        print("Audio stream saved successfully.")
        return "audio stream saved successfully"
    else:
        # Print the error message if the request was not successful
        print(response.text)
        print("else entered, something broke")
        return "something broke with the api"

# gen_voice_response("i know right. get that man some boof")