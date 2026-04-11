import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
import requests
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

llm_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

print("Loading Whisper model...")
whisper_model = whisper.load_model("base")

conn = sqlite3.connect("memory.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE,
        value TEXT NOT NULL
    )
""")
conn.commit()

# ─── Memory Functions ───────────────────────────────────

def save_memory(key, value):
    cursor.execute(
        "INSERT OR REPLACE INTO user_memory (key, value) VALUES (?, ?)",
        (key, value)
    )
    conn.commit()

def get_all_memory():
    cursor.execute("SELECT key, value FROM user_memory")
    rows = cursor.fetchall()
    if rows:
        return "\n".join([f"{key}: {value}" for key, value in rows])
    return "No memory yet."

def extract_and_save_memory(user_message):
    try:
        extraction_response = llm_client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
                {
                    "role": "system",
                    "content": """Extract important personal information from the message.
                    If found, reply ONLY with JSON like: {"key": "user_name", "value": "Chelsi"}
                    Keys can be: user_name, user_language, user_location, user_interest, user_age
                    If nothing important found, reply with: {"key": null, "value": null}"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        result = json.loads(extraction_response.choices[0].message.content)
        if result["key"] and result["value"]:
            save_memory(result["key"], result["value"])
            print(f"💾 Memory saved: {result['key']} = {result['value']}")
    except:
        pass

# ─── STT Function ───────────────────────────────────────

def record_and_transcribe():
    print("\n🎤 Listening... (5 seconds)")
    sample_rate = 16000
    duration = 5

    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype=np.float32
    )
    sd.wait()

    audio_squeezed = np.squeeze(audio)
    # Fix 1 — language specify karo, repeat words kam honge
    result = whisper_model.transcribe(audio_squeezed, language="en")
    text = result['text'].strip()

    # Fix 2 — empty transcription ignore karo
    if len(text) < 3:
        return ""

    return text

# ─── TTS Function ───────────────────────────────────────

def text_to_speech(text, emotion="Conversational"):
    response = requests.post(
        "https://in.api.murf.ai/v1/speech/stream",
        headers={
            "Content-Type": "application/json",
            "api-key": MURF_API_KEY
        },
        json={
            "voice_id": "Nikhil",
            "style": emotion,
            "model": "FALCON",
            "text": text
        }
    )
    if response.status_code == 200:
        with open("output.wav", "wb") as f:
            f.write(response.content)
        data, samplerate = sf.read("output.wav")
        sd.play(data, samplerate)
        sd.wait()
    else:
        print(f"TTS Error: {response.status_code}")

# ─── Main Agent Loop ────────────────────────────────────

conversation_history = []

print("🤖 Voice AI Agent ready!")
print("-" * 40)

while True:
    # Step 1 — STT
    user_input = record_and_transcribe()

    # Fix 2 — empty hai toh dobara suno
    if not user_input:
        print("Nothing heard, listening again...")
        continue

    print(f"You said: {user_input}")

    if "quit" in user_input.lower():
        print("Goodbye!")
        break

    # Step 2 — Memory extract karo
    extract_and_save_memory(user_input)

    # Step 3 — Memory load karo
    memory = get_all_memory()

    # Step 4 — History update karo
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        # Fix 3 — Emotion aur reply ek hi LLM call mein
        response = llm_client.chat.completions.create(
            model="openai/gpt-oss-120b:free",
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a helpful voice assistant. 
Here is what you know about the user:\n{memory}

At the end of your response, on a new line write exactly:
EMOTION: [one word from: Excited, Sad, Angry, Conversational]"""
                }
            ] + conversation_history,
            stream=True
        )

        ai_reply = ""
        print("AI: ", end="", flush=True)

        for chunk in response:
            if chunk.choices[0].delta.content:
                word = chunk.choices[0].delta.content
                print(word, end="", flush=True)
                ai_reply += word

        print("\n")

        # Fix 3 — Emotion reply se nikalo
        if "EMOTION:" in ai_reply:
            parts = ai_reply.split("EMOTION:")
            ai_reply = parts[0].strip()  # actual reply
            emotion = parts[1].strip()   # emotion
        else:
            emotion = "Conversational"

        print(f"Emotion: {emotion}")

        conversation_history.append({
            "role": "assistant",
            "content": ai_reply
        })

        # Step 5 — TTS
        text_to_speech(ai_reply, emotion)

    except Exception as e:
        print(f"Error: {e}")
        conversation_history.pop()
        continue