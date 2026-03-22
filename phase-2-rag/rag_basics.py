import chromadb

# make a instance of chromadb : it will run the database locally
client = chromadb.Client()

#make a folder named my knowledge, here collection is referred as folder in database
collection = client.create_collection(name="my_knowledge")

# sample sentences that will be stored in knowledge base
documents = [
    "Chelsi is an intern at an R&D company in India.",
    "Chelsi is building a voice AI agent with STT, LLM, TTS, RAG and memory.",
    "The voice AI agent uses ChromaDB as vector database.",
    "Chelsi is learning Python and machine learning concepts.",
    "The project is hosted on GitHub at github.com/Chelsi08/voice-ai-agent."
]

# adding documents to the collection
collection.add(
    documents=documents,       # actual text
    ids=["doc1", "doc2", "doc3", "doc4", "doc5"]  # every document has its unique id
)

print("Documents stored successfully!")

# Lets search 
query = "What is Chelsi building?"

results = collection.query(
    query_texts=[query],   # to search
    n_results=3            # return top 2 results
)

print(f"\nQuery: {query}")
print(f"Results: {results['documents']}")