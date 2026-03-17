from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()   #loads .env file 

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  #to get the key from env file and store it in a variable

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", #tells to go to openrouter server instead of OpenAI
    api_key=OPENROUTER_API_KEY  #identity proof 
)

response = client.chat.completions.create(
    model="stepfun/step-3.5-flash:free", #model which we are using, llm model of stepfun 
    messages=[   #list of message, role tells who sent the message, content is actual message 
        {"role": "user", "content": "Hello! Can you introduce yourself in one sentence?"}  
    ]
)

print(response.choices[0].message.content) #print the reponse, choice because it is list and there can be multiple options, [0] means first response


