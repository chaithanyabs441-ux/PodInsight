```markdown
# 🎙️ PodInsight - AI Podcast Q&A Bot

Ask questions about the **Elon Musk × Nikhil Kamath** podcast and get AI-powered answers with exact YouTube timestamps!

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📺 Demo

**Example Query:** "What is first-principles thinking?"

**Bot Response:** AI-generated answer + YouTube opens at exact timestamp where Elon discusses it.

---

## ✨ Features

- 🤖 **AI-Powered Answers**: Uses Groq API (Llama 3.1 8B) for natural, conversational responses
- 🎯 **Exact Timestamps**: Automatically opens YouTube at the precise moment topics are discussed
- 🔊 **Full Transcription**: Converts 2+ hours of podcast to searchable text using OpenAI Whisper
- 🔍 **Semantic Search**: FAISS-powered search finds relevant moments instantly
- 💬 **Natural Chat**: Feels like talking to a friend who watched the podcast
- 👋 **Greeting Detection**: Responds warmly to casual greetings
- 📊 **400+ Searchable Segments**: 30-second overlapping segments for precise results

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Speech-to-Text | OpenAI Whisper (base) | Transcribe podcast audio |
| Embeddings | TF-IDF Vectorization | Convert text to vectors |
| Search Engine | FAISS (Facebook) | Fast similarity search |
| AI Model | Llama 3.1 8B (Groq API) | Generate natural answers |
| Backend | Flask (Python) | Web server & API |
| Frontend | HTML, CSS, JavaScript | User interface |
| Audio Processing | FFmpeg | Audio format conversion |

---

## 📁 Project Structure

```
PodInsight/
├── app.py                    # Main Flask application
├── build_index.py            # FAISS search index builder
├── transcribe_podcast.py     # Whisper transcription script
├── run_all.py                # One-click launcher
├── templates/
│   └── index.html           # Chat interface
├── audio/
│   └── podcast_audio.mp3    # Downloaded podcast (not in repo)
├── data/
│   ├── transcription_full.json  # Full transcript
│   ├── segments.json           # 400+ searchable segments
│   └── podcast_index.faiss     # FAISS search index
├── ffmpeg.exe               # FFmpeg binary (Windows)
├── ffplay.exe               # FFmpeg player (Windows)
├── ffprobe.exe              # FFmpeg probe (Windows)
├── requirements.txt         # Python dependencies
├── .env                     # API keys (not in repo)
└── README.md               # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- FFmpeg (included for Windows)
- Groq API key (free - [get one here](https://console.groq.com/keys))
- Git (for cloning)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/chaithanyabs441-ux/PodInsight.git
cd PodInsight

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file with your Groq API key
echo GROQ_API_KEY=gsk_your_key_here > .env

# 6. Download podcast audio
# Go to https://ytmp3.nu/
# Paste: https://www.youtube.com/watch?v=Rni7Fz7208c
# Save as: audio/podcast_audio.mp3

# 7. Run the setup (first time only - takes 30-60 minutes)
python run_all.py

# 8. For subsequent runs:
python app.py

# 9. Open browser
http://localhost:5000
```

---

## 💡 Usage

### Example Questions:
- "What is first-principles thinking?"
- "What does Elon say about AI?"
- "How should entrepreneurs deal with government?"
- "What advice does Elon give about taking risks?"
- "What is collective consciousness?"
- Just say "Hi" to start a conversation!

### How It Works:
1. Type your question in the chat
2. Bot searches 400+ podcast segments
3. Llama 3.1 generates a natural answer
4. YouTube opens at the exact timestamp
5. Click the timestamp link to re-watch

---

## 🔄 Workflow

```
🎤 Podcast Audio (MP3)
    ↓ [Whisper Transcription]
📝 Full Transcript (2+ hours)
    ↓ [Split into 30-sec chunks]
📊 400+ Segments with Timestamps
    ↓ [TF-IDF Vectorization]
🔢 Embedding Vectors
    ↓ [FAISS Index]
🔍 Searchable Database

    🤔 User Question
        ↓ [Same embedding process]
    🔢 Query Vector
        ↓ [FAISS Search]
    📍 Top 3 Matches
        ↓ [Groq LLM]
    💬 Natural Answer + Timestamp
        ↓
    📺 YouTube Opens at Exact Moment
```

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| Transcription Time | 30-60 minutes (CPU) |
| Search Speed | <100ms per query |
| AI Response Time | 2-3 seconds |
| Segments Indexed | 400+ |
| Podcast Duration | 1 hour 54 minutes |
| Model Size | Whisper base (~142MB) |

---

## ⚠️ Limitations

### Technical Limitations

| Limitation | Description | Workaround |
|------------|-------------|------------|
| **Single Podcast** | Currently configured for one specific podcast | Modify VIDEO_ID and re-transcribe for others |
| **Manual Audio Download** | YouTube blocks automated downloads (HTTP 403) | Use ytmp3.nu or similar converter |
| **Python Version** | Requires Python 3.9+ | Upgrade Python if needed |
| **Whisper Accuracy** | Base model struggles with Indian accents | Use larger Whisper model (medium/large) |
| **API Dependency** | Requires internet for Groq API | No offline mode available |
| **Rate Limits** | Groq free tier: 30 requests/minute | Cache frequent queries |
| **Large File Size** | Audio + models ~500MB | Not suitable for low-storage devices |
| **Windows Only (FFmpeg)** | FFmpeg binaries are Windows-specific | Install FFmpeg separately on Mac/Linux |

### Functional Limitations

| Limitation | Description |
|------------|-------------|
| **No Speaker Diarization** | Cannot identify who said what (Elon vs Nikhil) |
| **No Follow-up Questions** | Each query is independent, no conversation memory |
| **Timestamp Precision** | May be off by 10-20 seconds |
| **Open-ended Questions** | "What's interesting?" returns vague answers |
| **Language Support** | English only |

### Known Issues

1. **HTTP 403 on Download**: YouTube's anti-bot protection blocks automated downloads
2. **Transcription Errors**: Technical terms or fast speech may be misheard
3. **AI Hallucination**: Groq may occasionally add information not in the podcast
4. **Browser Compatibility**: Best experienced on Chrome/Firefox

---

## 🔮 Future Improvements

- [ ] Multi-podcast support with URL input
- [ ] Speaker diarization (who said what)
- [ ] Local LLM fallback (Ollama)
- [ ] Conversation memory for follow-up questions
- [ ] Mobile-responsive design
- [ ] Export chat as PDF
- [ ] Voice input support
- [ ] Multi-language support
- [ ] Real-time transcription for live podcasts
- [ ] Docker containerization

---

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | `pip install -r requirements.txt` |
| "Audio file not found" | Download podcast to `audio/podcast_audio.mp3` |
| "Groq API error" | Check `.env` file has correct API key |
| "FAISS index not found" | Run `python build_index.py` |
| "Port 5000 in use" | Change port in `app.py` last line |
| "FFmpeg not found" | Ensure `ffmpeg.exe` is in project folder |
| "Whisper running slow" | Use GPU or smaller model |

---

## 🔑 Environment Variables

Create a `.env` file with:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Never commit `.env` to GitHub!** It's already in `.gitignore`.

---

## 📝 Development Notes

### Why FFmpeg is Included Locally
Instead of system-wide installation, FFmpeg binaries are included for portability. No PATH configuration needed on Windows.

### Why Manual Audio Download
yt-dlp returns HTTP 403 errors. Manual download via web converter is more reliable for this specific use case.

### Model Selection
Started with `llama3-8b-8192` (deprecated), switched to `llama-3.1-8b-instant` (current).

### Prompt Engineering
The system prompt explicitly defines personality and provides examples of good vs bad responses to prevent robotic answers.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Credits

- **Podcast**: Elon Musk × Nikhil Kamath | People by WTF Ep. 16
- **Transcription**: OpenAI Whisper
- **AI Model**: Groq (Llama 3.1)
- **Search**: FAISS by Facebook Research
- **Inspiration**: Building AI-powered tools for content accessibility

---

## 📧 Contact

- GitHub: [@chaithanyabs441-ux](https://github.com/chaithanyabs441-ux)
- Project Link: [https://github.com/chaithanyabs441-ux/PodInsight](https://github.com/chaithanyabs441-ux/PodInsight)

---

<p align="center">
  <b>Built with ❤️ for podcast lovers</b>
</p>
```
