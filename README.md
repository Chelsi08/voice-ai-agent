# Voice AI Agent 🎙️

A voice AI agent built from scratch — combining Speech-to-Text, Large Language Models, RAG, Memory, and Text-to-Speech into one complete pipeline.

> Built phase by phase with full understanding of every component. No copy-paste, no shortcuts.

---

## What This Does

A user speaks → agent listens → understands → thinks → replies with emotion in natural voice.

---

## Architecture
```
User Speaks
     │
     ▼
STT (Speech to Text)        — converts voice to text
     │
     ▼
Memory Check                — what do we know about this user?
     │
     ▼
RAG (Retrieval)             — fetches relevant knowledge
     │
     ▼
LLM (Large Language Model)  — understands and generates reply
     │
     ▼
Emotion Detection           — detects emotion of reply
     │
     ▼
TTS (Text to Speech)        — speaks reply with emotion
     │
     ▼
User Hears Response
```

---

## Progress

| Phase | What | Status |
|---|---|---|
| Phase 0 | Repo setup, structure | ✅ Done |
| Phase 1 | LLM API call, conversation history, streaming, error handling | ✅ Done |
| Phase 2 | RAG + ChromaDB vector database | ✅ Done |
| Phase 3 | TTS + emotion detection with Murf AI | ✅ Done |
| Phase 4 | STT with Whisper | ✅ Done |
| Phase 5 | Persistent memory with SQLite | ✅ Done |
| Phase 6 | Full voice agent — all components integrated | ✅ Done |

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM | OpenRouter API |
| STT | Whisper (OpenAI) — runs locally |
| TTS | Murf AI (Falcon) |
| Vector Database | ChromaDB |
| Long-term Memory | SQLite |
| Deployment | AWS EC2 (planned) |

---

## How It Works

1. Whisper listens to user via microphone — converts voice to text
2. SQLite memory is checked — agent knows who the user is
3. ChromaDB fetches relevant knowledge from vector database
4. LLM generates a reply and detects the emotion
5. Murf AI speaks the reply in the detected emotion
6. Loop continues — persistent memory across sessions

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/Chelsi08/voice-ai-agent.git

# Go to phase 6
cd phase-6-full-agent

# Add your API keys in .env
OPENROUTER_API_KEY=your_key
MURF_API_KEY=your_key

# Run the agent
python agent.py
```

---

## Key Learnings

- How LLMs work and how to call them via API
- What RAG is and how vector databases store meaning
- How STT and TTS pipelines are built
- How persistent memory works with SQLite
- How to connect all components into one working system

---

## License

MIT

