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
| Phase 3 | Connect LLM output to TTS + emotion detection | 🔄 In Progress |
| Phase 4 | STT integration | ⏳ Planned |
| Phase 5 | Memory system | ⏳ Planned |
| Phase 6 | Full agent + deployment | ⏳ Planned |

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| LLM | OpenRouter API |
| Vector Database | ChromaDB |
| TTS | TBD — ElevenLabs / Murf AI / Cartesia (testing in progress) |
| STT | TBD — evaluating options (Whisper / Google STT) |
| Deployment | AWS EC2 |

---

## How to Run

1. Clone this repo
2. Add your API keys in `.env`
3. Follow each phase folder in order

---

## License

MIT