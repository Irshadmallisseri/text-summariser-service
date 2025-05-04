
# 🧠 AI Summariser API

A production-ready FastAPI application for:

- ✅ Text Summarization using Hugging Face's `facebook/bart-large-cnn`
- ✅ Audio Transcription using OpenAI Whisper (with GPU support)
- ✅ Logging, .env configuration, and modular structure

---

## 🚀 Features

- 📄 Summarize long-form text via API
- 🔊 Transcribe audio files (`.mp3`, `.wav`, `.flac`, `.m4a`)
- ⚙️ GPU-accelerated inference (CUDA)
- 📑 Dynamic input/output length management
- 📁 Rotating log file support
- 🔐 .env config for models and limits

---

## 📁 Project Structure

```
AISummariser/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── logging_config.py        # Centralized logger
│   ├── middleware/
│   │   └── request_logger.py    # Logs all API requests
│   ├── routes/
│   │   ├── summarize.py
│   │   └── transcribe.py
│   ├── utils/
│   │   ├── summarizer.py
│   │   └── whisper_transcriber.py
├── logs/
│   └── app.log                  # Rotating log file
├── .env                         # Model config
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/aisummariser.git
cd aisummariser
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API

```bash
uvicorn app.main:app --reload
```

---

## 📦 API Endpoints

### ➤ `POST /api/summarize-text`
**Body:**
```json
{
  "text": "Your long-form text here..."
}
```

### ➤ `POST /api/transcribe-audio`
**Form:**
- `file`: Upload an audio file (`.mp3`, `.wav`, `.flac`, `.m4a`)

---

## 📄 Environment Variables (`.env`)

```
MODEL_NAME=facebook/bart-large-cnn
MAX_INPUT_LENGTH=512
ABSOLUTE_MAX_SUMMARY_LENGTH=300
```

---

## 📝 Logging

- Logs stored in `logs/app.log`.
- Request/response, errors, and inference timing all logged using `logging`.

---

## 🛠️ Requirements

- Python 3.10+
- CUDA-enabled GPU (for Whisper)
- FFmpeg in `app/../ffmpeg/` directory

---

## 📫 Contact

Made by Irshad – feel free to fork, modify, and extend.


---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
