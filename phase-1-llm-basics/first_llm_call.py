from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

response = client.chat.completions.create(
    model="stepfun/step-3.5-flash:free",
    messages=[
        {"role": "user", "content": "Hello! Can you introduce yourself in one sentence?"}
    ]
)

print(response.choices[0].message.content)
