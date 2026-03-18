from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()   #loads .env file 

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")  #to get the key from env file and store it in a variable

client = OpenAI(
    base_url="https://openrouter.ai/api/v1", #tells to go to openrouter server instead of OpenAI
    api_key=OPENROUTER_API_KEY  #identity proof 
)

conversation_history = []  #empty list - to store the conversation (memory)

while True :   #infinite loop until user writes quit
    user_input = input("You: ") #till then take the input from user

    if user_input.lower() == "quit":  #if user writes quit, end the conversation
        break

    conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    response = client.chat.completions.create(
    model="stepfun/step-3.5-flash:free", #model which we are using, llm model of stepfun 
    messages= conversation_history #send the whole history not just a single message
    )
    
    ai_reply = response.choices[0].message.content  #get the answer from AI
    
    conversation_history.append({   #Store AI's answer in history as well 
    "role": "assistant",
    "content" : ai_reply
    })
    
    print(f"AI: {ai_reply}\n") #print the ai reply on screen


