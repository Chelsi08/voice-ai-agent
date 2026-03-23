import chromadb
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# LLM client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)

# ChromaDB setup
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="my_knowledge")

# documents referred as knowledge base 
documents = [
    "Chelsi is an intern at an R&D company in India.",
    "Chelsi is building a voice AI agent with STT, LLM, TTS, RAG and memory.",
    "The voice AI agent uses ChromaDB as vector database.",
    "Chelsi is learning Python and machine learning concepts.",
    "The project is hosted on GitHub at github.com/Chelsi08/voice-ai-agent."
]

collection.add(
    documents=documents,
    ids=["doc1", "doc2", "doc3", "doc4", "doc5"]
)

print("Knowledge base ready!")
print("-" * 40)

# User's question
user_question = input("You:")

# Step 1 — get relevant document from ChromaDB
results = collection.query(
    query_texts=[user_question],
    n_results=3
)

relevant_docs = results['documents'][0]  # top 3 documents

# Step 2 — Join the documents in one string
context = "\n".join(relevant_docs)

# Step 3 — send to LLM with context
response = client.chat.completions.create(
    model="stepfun/step-3.5-flash:free",
    messages=[
        {
            "role": "system",
            "content": f"Answer the question using only this context:\n{context}"
        },
        {
            "role": "user",
            "content": user_question
        }
    ]
)

print(f"\nAI: {response.choices[0].message.content}")