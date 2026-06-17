# Voice Study Assistant 🎙️

A voice-activated AI study assistant built for placement preparation. Speak to it, it listens, thinks, and talks back — like a personal tutor running entirely on your machine.

---

## Demo

> Say **"Hey Buddy"** → Ask anything → Get a spoken response

```
You:       "Hey Buddy"
Assistant: "Yeah?"
You:       "Quiz me on SQL"
Assistant: "Here's your first question — what does GROUP BY do?"
```

---

## What It Does

- Wakes up on the phrase **"Hey Buddy"**
- Listens to your question via microphone
- Sends it to a local LLM (Ollama) with a study-focused system prompt
- Speaks the response back using macOS native `say` command
- Remembers the last 20 messages in the session (context window)
- Opens websites by voice command
- Has built-in study shortcuts — quiz me, interview me, revise SQL, etc.

---

## Tech Stack

| Component | Tool |
|---|---|
| Speech-to-Text | Google Speech Recognition via `speech_recognition` |
| LLM Backend | Ollama (local) — `qwen2.5:1.5b` |
| Text-to-Speech | macOS native `say` command |
| API Interface | OpenAI-compatible client pointed at Ollama |
| Language | Python 3.14 |

---

## Project Structure

```
voice-study-assistant/
│
├── Study assistant.py     # Main application
└── README.md
```

---

## How It Works

### 1. Wake Word Detection
The program runs in an infinite loop, listening with a short timeout. When it hears **"hey buddy"**, it activates and listens for a full command.

### 2. Speech Recognition
Uses Google's free STT API via the `speech_recognition` library. Microphone audio is captured using `PyAudio`, adjusted for ambient noise, then converted to text.

### 3. LLM Call
The transcribed text is appended to a `conversation_history` list (last 20 messages) and sent to Ollama running locally at `http://localhost:11434`. The model used is `qwen2.5:1.5b`.

A detailed **system prompt** instructs the model to:
- Respond like a placement tutor
- Use analogies over textbook definitions
- Keep responses short and spoken-friendly
- Handle study commands like quiz, interview, revise

### 4. Text-to-Speech
Response is cleaned (markdown symbols stripped) and passed to macOS `say` command via `os.system()`. No external TTS library needed.

### 5. Command Handler
Before sending to the LLM, commands are checked for shortcuts:
- `"quiz me"` → triggers MCQ mode
- `"interview me"` → triggers mock interview
- `"revise sql/dbms/dsa"` → triggers quick revision
- `"open youtube/github/leetcode"` → opens browser

---

## Voice Commands

| You Say | What Happens |
|---|---|
| `hey buddy` | Activates assistant |
| `quiz me` | Starts MCQ session |
| `next` | Next question |
| `explain` | Deeper explanation |
| `interview me` | Mock placement interview |
| `revise sql` | Quick SQL revision |
| `revise dbms` | Quick DBMS revision |
| `revise dsa` | Quick DSA revision |
| `open youtube` | Opens YouTube |
| `open github` | Opens GitHub |
| `open leetcode` | Opens LeetCode |
| `quit` / `exit` / `bye` | Closes assistant |

---

## Setup & Installation

### Prerequisites
- macOS (uses built-in `say` command for TTS)
- Python 3.10+
- [Homebrew](https://brew.sh)
- [Ollama](https://ollama.com)

### Step 1 — Clone the repo
```bash
git clone https://github.com/abduvk/voice-study-assistant.git
cd voice-study-assistant
```

### Step 2 — Create virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install openai speechrecognition pyaudio
```

If `pyaudio` fails:
```bash
brew install portaudio
pip install pyaudio
```

### Step 4 — Install and start Ollama
```bash
brew install ollama
ollama pull qwen2.5:1.5b
```

### Step 5 — Start Ollama server (keep this running)
```bash
ollama serve
```

### Step 6 — Run the assistant (new terminal tab)
```bash
python "Study assistant.py"
```

---

## Why Ollama Instead of OpenAI API

This project runs **100% locally** — no API key, no billing, no internet required for the LLM. Ollama exposes an OpenAI-compatible API at `localhost:11434`, so the same OpenAI Python client works with zero code change.

---

## Author

**Maqdoom Abdul Hannan**  
Final Year B.Tech CSE — REVA University, Bengaluru  
GitHub: [@abduvk](https://github.com/abduvk)
