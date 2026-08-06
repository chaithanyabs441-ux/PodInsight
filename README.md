# 🎙️ PodInsight – AI-Powered Podcast Search & Timestamp Assistant

PodInsight is an intelligent Retrieval-Augmented Generation (RAG) application that transforms long-form podcasts into an interactive knowledge base. Instead of manually searching through hours of content, users can ask natural language questions and receive AI-generated answers backed by the podcast itself—along with a direct YouTube timestamp to the exact moment the topic is discussed.

The project combines speech recognition, semantic search, vector similarity, and large language models to create a fast, conversational podcast exploration experience.

---

## 🚀 What Makes PodInsight Different?

Unlike traditional chatbots that generate answers from general knowledge, PodInsight retrieves the most relevant transcript segments before generating a response. Every answer is grounded in the podcast and can be verified instantly by jumping to the exact timestamp in the original video.

### Key Features

- 🎤 Converts long-form podcasts into searchable knowledge using OpenAI Whisper
- 🧠 Semantic search powered by Sentence Transformers and FAISS
- 🤖 Natural conversational responses generated using Llama 3.1 via Groq
- ⏱️ Automatic YouTube timestamp navigation
- 🔍 Understands meaning instead of simple keyword matching
- 💬 Clean chat interface with example prompts and greeting detection
- ⚡ Fast retrieval and response generation

---

## 🏗️ System Architecture

```
               Offline Processing

Podcast Video
      │
      ▼
Audio Extraction
      │
      ▼
OpenAI Whisper
      │
      ▼
Transcript + Timestamps
      │
      ▼
Sentence Transformers
      │
      ▼
Vector Embeddings
      │
      ▼
FAISS Index


                Runtime

User Question
      │
      ▼
Flask API
      │
      ▼
Semantic Search (FAISS)
      │
      ▼
Relevant Transcript Segments
      │
      ▼
Groq Llama 3.1
      │
      ▼
Natural Language Answer
      │
      ▼
Timestamp + YouTube Navigation
```

---

## 💻 Technology Stack

| Layer | Technology |
|--------|------------|
| Speech Recognition | OpenAI Whisper |
| Semantic Embeddings | Sentence Transformers (all-MiniLM-L6-v2) |
| Vector Search | FAISS |
| Large Language Model | Llama 3.1 8B (Groq API) |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Audio Processing | FFmpeg |
| Language | Python |

---

## 🎯 Example

**Question**

> *What is first-principles thinking?*

**PodInsight**

- Retrieves the most relevant transcript section
- Generates a concise answer using Llama 3.1
- Returns the exact timestamp
- Opens YouTube directly at that moment

No more manually searching through a 2-hour podcast.

---

## 📌 How It Works

1. Download the podcast audio.
2. Transcribe the audio using OpenAI Whisper.
3. Split the transcript into timestamped segments.
4. Convert each segment into semantic embeddings.
5. Store embeddings in a FAISS vector index.
6. Convert the user's question into an embedding.
7. Retrieve the most relevant transcript segments.
8. Generate a grounded answer using Llama 3.1.
9. Redirect the user to the exact timestamp in the original YouTube video.

---

## 🎯 Use Cases

- Podcast semantic search
- Educational content exploration
- Interview and lecture navigation
- Knowledge retrieval from long-form videos
- AI-powered learning assistants

---

> **PodInsight demonstrates how Retrieval-Augmented Generation (RAG) can be applied to long-form multimedia content, enabling users to interact with podcasts conversationally while maintaining traceability through timestamped source references.**
