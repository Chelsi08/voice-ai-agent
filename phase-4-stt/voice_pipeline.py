import whisper
import sounddevice as sd
import numpy as np
import requests
from openai import OpenAI
from dotenv import load_dotenv
import os
import playsound
import soundfile as sf


load_dotenv()  # load the env file

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  # LLM key
MURF_API_KEY = os.getenv("MURF_API_KEY")  # TTS key

# LLM client — through OpenRouter
llm_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# Load the whisper model once, it will save in memory for the rest of the conversation
print("Loading Whisper model...")
whisper_model = whisper.load_model("base")
print("Ready! 🎤")

# TTS function — take the text, make an audio through murf and then save it in a file
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
            "text": text,
            "format": "WAV"  # WAV format maango
        }
    )
    if response.status_code == 200:
        with open("output.wav", "wb") as f:
            f.write(response.content)
        # WAV file directly play karo
        data, samplerate = sf.read("output.wav")
        sd.play(data, samplerate)
        sd.wait()  # audio khatam hone tak ruko
    else:
        print(f"TTS Error: {response.status_code} — {response.text}")

# STT function — take the audio through microphone, convert it into text with Whisper, and then return
def record_and_transcribe():
    print("\n🎤 Recording... Speak now! (5 seconds)")
    sample_rate = 16000  # Whisper wants 16000Hz
    duration = 5  # seconds

    audio = sd.rec(
        int(duration * sample_rate),  # total samples
        samplerate=sample_rate,
        channels=1,  # mono audio
        dtype=np.float32  # Whisper wants float32 
    )
    sd.wait()  # wait till the recording ends
    print("Transcribing...")

    audio_squeezed = np.squeeze(audio)  # fix the shape
    result = whisper_model.transcribe(audio_squeezed)  # speech to text
    return result['text']  # send the text back to the user

# Conversation history — to give memory to the llm
conversation_history = []

print("\nVoice AI Agent ready! Say something...")
print("-" * 40)

while True:
    # Step 1 — take users voice and convert it into text
    user_input = record_and_transcribe()
    print(f"You said: {user_input}")

    # If quit then end the ocnversation
    if "quit" in user_input.lower():
        print("Goodbye!")
        break

    # user message into the history
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        # Step 2 — take answer from LLM
        response = llm_client.chat.completions.create(
            model="stepfun/step-3.5-flash:free",
            messages=conversation_history,
            stream=True  # word by word answer
        )

        ai_reply = ""
        print("AI: ", end="", flush=True)

        for chunk in response:  # every chunk has one word
            if chunk.choices[0].delta.content:
                word = chunk.choices[0].delta.content
                print(word, end="", flush=True)  # word by word print
                ai_reply += word  # collect the answer

        print("\n")

        # send the AI answer to the history
        conversation_history.append({
            "role": "assistant",
            "content": ai_reply
        })

        # Step 3 — send LLM answer to tts
        text_to_speech(ai_reply)

    except Exception as e:
        print(f"Error: {e}")
        conversation_history.pop()  # remove failed message from history
        continue

print(f"Response status: {response.status_code}")
print(f"Response headers: {response.headers}")
print(f"Content length: {len(response.content)}")