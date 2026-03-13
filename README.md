# Voice AI Agent 🎙️
A voice AI agent — combining 
Speech-to-Text, Large Language Models, and 
Text-to-Speech into one complete pipeline.

## What This Does
A user speaks → agent listens → understands → 
thinks → replies with emotion in natural voice.

## Architecture
```
User Speaks
     │
     ▼
STT (Speech to Text)     — converts voice to text
     │
     ▼
RAG (Retrieval)          — fetches relevant knowledge
     │
     ▼
LLM (Large Language Model) — understands and generates reply
     │
     ▼
Emotion Detection        — detects emotion of reply
     │
     ▼
TTS (Text to Speech)     — speaks reply with emotion
     │
     ▼
User Hears Response
```

## Phases
| Phase | What We Build |
|---|---|
| Phase 1 | First LLM API call |
| Phase 2 | RAG + Vector Database |
| Phase 3 | Connect LLM to TTS |
| Phase 4 | Add STT |
| Phase 5 | Add Memory |
| Phase 6 | Full Agent |

## Technologies Used
- Python
- Google Gemini API
- ChromaDB (Vector Database)
- Murf AI (TTS)
- Deepgram (STT)

## How to Run
1. Clone this repo
2. Add your API keys in `.env`
3. Follow each phase folder in order