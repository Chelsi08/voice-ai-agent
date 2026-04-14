from flask import Flask, render_template, request, jsonify
import sqlite3
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import requests
import base64

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MURF_API_KEY = os.getenv("MURF_API_KEY")

app = Flask(__name__)

llm_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# Database setup
conn = sqlite3.connect("memory.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE,
        value TEXT NOT NULL
    )
""")
conn.commit()

conversation_history = []

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
    except:
        pass

# ─── Routes ─────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    # Memory
    extract_and_save_memory(user_message)
    memory = get_all_memory()

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    try:
        # LLM
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
            ] + conversation_history
        )

        ai_reply = response.choices[0].message.content

        # Emotion nikalo
        if "EMOTION:" in ai_reply:
            parts = ai_reply.split("EMOTION:")
            ai_reply = parts[0].strip()
            emotion = parts[1].strip()
        else:
            emotion = "Conversational"

        conversation_history.append({
            "role": "assistant",
            "content": ai_reply
        })

        # TTS — Murf se audio lo
        murf_response = requests.post(
            "https://in.api.murf.ai/v1/speech/stream",
            headers={
                "Content-Type": "application/json",
                "api-key": MURF_API_KEY
            },
            json={
                "voice_id": "Nikhil",
                "style": emotion,
                "model": "FALCON",
                "text": ai_reply
            }
        )

        # Audio ko base64 mein convert karo — browser ko bhejne ke liye
        audio_base64 = base64.b64encode(murf_response.content).decode("utf-8")

        return jsonify({
            "reply": ai_reply,
            "emotion": emotion,
            "audio": audio_base64
        })

    except Exception as e:
        conversation_history.pop()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)