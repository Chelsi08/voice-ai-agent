import sqlite3
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

llm_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# Database setup
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

# Memory functions
def save_memory(key, value):
    cursor.execute(
        "INSERT OR REPLACE INTO user_memory (key, value) VALUES (?, ?)",
        (key, value)
    )
    conn.commit()

def get_all_memory():   #get all the memory from db
    cursor.execute("SELECT key, value FROM user_memory")
    rows = cursor.fetchall()  #get all rows together
    if rows:
        return "\n".join([f"{key}: {value}" for key, value in rows])  #convert list into a string
    return "No memory yet."

def extract_and_save_memory(user_message):
    try:
        extraction_response = llm_client.chat.completions.create(
            model="stepfun/step-3.5-flash:free",
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
        pass  # ignore any error 

# Conversation
conversation_history = []

print("Memory-enabled AI Agent ready!")
print("-" * 40)

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        break

    # Extract memory from user message
    extract_and_save_memory(user_input)

    # Give old memory to LLM
    memory = get_all_memory()

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = llm_client.chat.completions.create(
            model="stepfun/step-3.5-flash:free",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a helpful assistant. Here is what you know about the user:\n{memory}"
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

        conversation_history.append({
            "role": "assistant",
            "content": ai_reply
        })

    except Exception as e:
        print(f"Error: {e}")
        conversation_history.pop()
        continue