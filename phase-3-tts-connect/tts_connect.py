import requests
import os
from dotenv import load_dotenv

load_dotenv()

MURF_API_KEY = os.getenv("MURF_API_KEY")

def text_to_speech(text):
    response = requests.post(
        "https://in.api.murf.ai/v1/speech/stream",
        headers={
            "Content-Type": "application/json",
            "api-key": MURF_API_KEY
        },
        json={
            "voice_id": "Nikhil",
            "style": "Conversational",
            "model": "FALCON",
            "text": text
        }
    )
    
    if response.status_code == 200:
        # save the audio file
        with open("output.mp3", "wb") as f:
            f.write(response.content)
        print("Audio saved — output.mp3")
    else:
        print(f"Error: {response.status_code} — {response.text}")

# demo text agent will generate voice for 
text_to_speech("Hello! I am your voice AI agent. How can I help you today?")
