# Voice AI Agent 🎙️

> A production-grade voice AI agent built from scratch — combining Speech-to-Text, RAG, Persistent Memory, Emotion Detection, and Text-to-Speech into one complete end-to-end pipeline.

**No tutorials followed. No copy-paste. Built phase by phase with full understanding of every component.**

---

## 🚀 Demo Flow

```
You speak  →  Whisper (STT)  →  SQLite Memory  →  ChromaDB RAG  →  LLM  →  Emotion Detection  →  Murf AI (TTS)  →  You hear a reply
```

A user speaks → the agent listens, remembers who they are, retrieves relevant knowledge, generates a contextual reply, detects the emotional tone, and speaks back — all in one loop.

---

## 🏗️ System Architecture

```
User Speaks
     │
     ▼
┌─────────────────────┐
│  Whisper STT        │  — Local speech recognition (OpenAI Whisper)
│  runs on-device     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  SQLite Memory      │  — Who is this user? What was said before?
│  Persistent store   │     Cross-session memory, not just context window
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  ChromaDB RAG       │  — Semantic retrieval from vector database
│  Embeddings + Search│     Fetches only what's relevant to this query
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  LLM via OpenRouter │  — Generates reply with full context:
│  (reasoning layer)  │     memory + retrieved knowledge + conversation history
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Emotion Detection  │  — Classifies emotional tone of the reply
│                     │     (neutral / happy / empathetic / urgent etc.)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Murf AI TTS        │  — Speaks the reply in the detected emotional tone
│  (Falcon voice)     │     Not just robotic playback — contextual expression
└─────────┬───────────┘
          │
          ▼
     User Hears
   Natural Response
```

---

## ✅ Build Phases

Each phase was built, tested, and understood before moving to the next. No black boxes.

| Phase | What Was Built | Status |
|-------|---------------|--------|
| Phase 0 | Project structure, environment setup, API key management | ✅ Complete |
| Phase 1 | LLM API integration, conversation history, streaming, error handling | ✅ Complete |
| Phase 2 | RAG pipeline — ChromaDB vector store, embeddings, semantic search | ✅ Complete |
| Phase 3 | TTS with Murf AI + emotion detection layer | ✅ Complete |
| Phase 4 | STT with Whisper — local, offline speech recognition | ✅ Complete |
| Phase 5 | Persistent memory with SQLite — cross-session user context | ✅ Complete |
| Phase 6 | Full integration — all components wired into one agent loop | ✅ Complete |

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Language | Python 3.10+ | Ecosystem for AI/ML |
| LLM | OpenRouter API | Multi-model flexibility |
| STT | OpenAI Whisper | Local, no latency, no cost per call |
| TTS | Murf AI (Falcon) | Emotional voice synthesis |
| Vector DB | ChromaDB | Fast local semantic search |
| Memory | SQLite | Lightweight persistent store |
| Embeddings | Sentence Transformers | Semantic similarity for RAG |
| Deployment | AWS EC2 (planned) | Cloud hosting |

---

## 📂 Project Structure

```
voice-ai-agent/
│
├── phase-1-llm/          # LLM API + streaming + conversation history
├── phase-2-rag/          # ChromaDB setup + embedding pipeline + retrieval
├── phase-3-tts/          # Murf AI integration + emotion classifier
├── phase-4-stt/          # Whisper integration + microphone input
├── phase-5-memory/       # SQLite schema + read/write memory layer
├── phase-6-full-agent/   # Complete integrated pipeline
│   └── agent.py          # Main entry point
│
├── docs/                 # Architecture notes and phase learnings
├── .env.example          # API key template
└── requirements.txt
```

---

## ⚡ Quick Start

```bash
# 1. Clone
git clone https://github.com/Chelsi08/voice-ai-agent.git
cd voice-ai-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set API keys
cp .env.example .env
# Add your keys:
# OPENROUTER_API_KEY=your_key
# MURF_API_KEY=your_key

# 4. Run the full agent
cd phase-6-full-agent
python agent.py
```

> **Note:** Whisper runs locally — no API key needed. Make sure a microphone is connected.

---

## 🧠 What I Learned Building This

This wasn't a tutorial project. Each phase required independently solving real engineering problems:

- **Embeddings & Vector Search** — understanding how text is converted to vectors, stored, and retrieved by semantic similarity (not keyword match)
- **RAG architecture** — why retrieval-augmented generation outperforms pure LLM memory for factual accuracy
- **Persistent memory vs context window** — the difference between short-term (conversation history) and long-term (SQLite) memory, and when to use each
- **Emotion-aware TTS** — how to classify emotional tone from LLM output and map it to voice parameters
- **System integration** — connecting 5+ independent components with different I/O formats into one reliable loop
- **Streaming LLM responses** — handling token-by-token output for real-time feel

---

## 🔮 What's Next

- [ ] AWS EC2 deployment with Docker
- [ ] Web interface (FastAPI + simple frontend)
- [ ] Support for multiple knowledge bases (switch domains)
- [ ] Latency optimisation — target < 2s end-to-end response
- [ ] Evaluation metrics — track response quality over time

---

## 📄 License

MIT — use freely, attribution appreciated.

---

*Built by [Chelsi Patel](https://linkedin.com/in/chelsi-patel-26b944251) — CS + AI/ML graduate, VIT Bhopal*
